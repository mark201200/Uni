#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <fcntl.h>
#include <errno.h>
#include <mqueue.h>
#include <sys/stat.h>

#pragma clang diagnostic push
#pragma ide diagnostic ignored "EndlessLoop"
struct message {
    int wid;
    int msg;
};

int main() {
    pid_t w1 = fork();
    if (w1 == 0) execl("./worker", "./worker", "1", NULL);
    pid_t w2 = fork();
    if (w2 == 0) execl("./worker", "./worker", "2", NULL);
    int res1 = mkfifo("./w1f", 0666);
    mkfifo("./w2f", 0666);
    int w1p = open("w1p", O_RDONLY);
    int w2p = open("w2p", O_RDONLY);
    struct message w1_msg, w2_msg;
    while (1) {
        int res = read(w1p, &w1_msg, sizeof(w1_msg));
        read(w2p, &w2_msg, sizeof(w2_msg));
        printf("Pid: %d Ricevuto %d da 1 e %d da 2.\n", getpid(), w1_msg.msg, w2_msg.msg);
        sleep(1);
    }
}

#pragma clang diagnostic pop