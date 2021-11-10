#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <fcntl.h>
#include <time.h>

struct message {
    int wid;
    int msg;
};

int main(int argc, char *argv[]) {
    srand(time(NULL));
    struct message msg;
    int numero;
    char pname[15];
    sprintf(pname, "./w%sf", argv[1]);
    int pipe = open(pname,O_WRONLY);
    msg.wid = (int) argv[1] - '0';
    while (1) {
        numero = (rand() % 100) + 1;
        msg.msg = numero;
        write(pipe,&msg,sizeof(msg));
        printf("pid %d worker %s: mandato %d\n",getpid(),argv[1], numero);
        sleep(1);
    }
}
