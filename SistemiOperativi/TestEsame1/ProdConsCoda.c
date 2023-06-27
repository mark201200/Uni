#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <signal.h>
#include <mqueue.h>

mqd_t queueProd, queueCons;

struct mq_attr attr;

void produttore(){
    queueProd = mq_open("/queue",O_CREAT|O_WRONLY,0660,&attr);
    int n = 0;
    srand(time(NULL));
    while(1){
        n=rand()%10+1;
        printf("Produttore: mando il numero %i\n",n);
        mq_send(queueProd,&n,sizeof(n),0);
        usleep(500000);
    }
}

int main(){
    attr.mq_flags = 0;
    attr.mq_maxmsg = 10;
    attr.mq_msgsize = sizeof (int);
    attr.mq_curmsgs = 0;

    pid_t pid = fork();
    if(pid == 0) produttore();

    int received=0;

    queueProd = mq_open("/queue",O_CREAT|O_RDONLY,0660,&attr);
    while(received != 10){
        mq_receive(queueProd,&received, sizeof(int), NULL);
        printf("Consumatore: Ricevo il numero %i\n",received);
    }
    printf("Consumatore: Esco!");

    mq_close(queueProd);
    mq_close(queueCons);
    mq_unlink("/queue");

    kill(pid ,SIGKILL);
    wait(NULL);
    exit(0);
}
