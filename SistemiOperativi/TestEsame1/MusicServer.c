#include "stdio.h"
#include "stdlib.h"
#include "unistd.h"
#include "fcntl.h"
#include "mqueue.h"


#define Q_PERM 0660
#define MAX_MSG 10

int main(){
    struct message{
        char nome[64];
        char autore[64];
    } songRequest;

    char lyrics[64] = "Testo di esempio";

    mqd_t qd_client, qd_server;
    
    struct mq_attr attr;
    attr.mq_flags = 0;
    attr.mq_maxmsg = MAX_MSG;
    attr.mq_msgsize = sizeof (songRequest);
    attr.mq_curmsgs = 0;

    qd_server = mq_open("/mq_server",O_CREAT|O_RDONLY,Q_PERM,&attr);
    qd_client = mq_open("/clientQ",O_WRONLY);
    
    printf("Benvenuto! Server in attesa di richiesta...\n");
    
    mq_receive(qd_server, &songRequest, sizeof(songRequest), NULL);
    
    printf("Ricevuta richiesta!\nNome: %s\nAutore:%s\n",songRequest.nome,songRequest.autore);
   
    mq_send(qd_client, &lyrics, sizeof(lyrics),0);
    

    printf("Testo inviato. Arrivederci!\n");

    mq_close(qd_client);
    mq_unlink("/mq_server");
}
