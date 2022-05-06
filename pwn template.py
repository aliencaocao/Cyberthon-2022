from pwn import *

context.binary = elf = ELF('vuln')
io = remote('chals.cyberthon22f.ctf.sg', 20201)

payload =
io.sendline(payload)
io.interactive()
