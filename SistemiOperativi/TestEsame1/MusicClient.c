#include "stdio.h"
#include "stdlib.h"
#include "unistd.h"
#include "fcntl.h"
#include "mqueue.h"

#define SERVER_Q_NAME "/mq_server"
#define Q_PERM 0660
#define MAX_MSG 10

int main(){
    
    struct message{
        char nome[64];
        char autore[64];
    } songRequest;

    char lyrics[64];

    mqd_t qd_client, qd_server;
    
    struct mq_attr attr;
    attr.mq_flags = 0;
    attr.mq_maxmsg = MAX_MSG;
    attr.mq_msgsize = sizeof (lyrics);
    attr.mq_curmsgs = 0;
    

    qd_client = mq_open("/clientQ",O_CREAT|O_RDWR,Q_PERM,&attr);
    qd_server = mq_open(SERVER_Q_NAME,O_WRONLY);

    strcpy(songRequest.autore,"Autore di esempio");
    strcpy(songRequest.nome,"Nome di esempio");

    mq_send(qd_server, &songRequest, sizeof(songRequest),0);
    mq_receive(qd_client, (char*)&lyrics, sizeof(lyrics), NULL);

    printf("Testo ricevuto:\n%s",lyrics);

    mq_close(qd_client);
    mq_unlink("/clientQ");
}
