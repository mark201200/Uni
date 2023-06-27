/** 
	Sistemi operativi e reti (SOR)
	Appello 4 - A.A. 2013/2014
	@author Pietro Frasca
	@version 1.00 16-01-2016

	Realizzate un programma multi-thread in C, completo di commento, che svolga quanto segue: il thread main crea due thread figli T1 e T2. Entrambi i thread figli eseguono un ciclo indeterminato durante il quale, ad ogni iterazione, generano un numero intero casuale compreso tra 1 e 10 che comunicano al padre. Il thread padre, per ogni coppia di numeri che riceve dai thread figli ne confronta il valore e nel caso in cui sia maggiore il numero estratto da T1 incrementa di 1 la variabile S1, nel caso in cui invece sia maggiore il numero estratto da T2 incrementa di 1 la variabile S2; se i numeri estratti dai due thread T1 e T2 sono uguali decrementa di 1 entrambe le variabili S1 e S2. Quando il thread padre verifica che il valore di S1 o di S2 ha superato il valore 41, visualizza sullo schermo il valore delle due variabili e il programma termina. La sequenza temporale delle operazioni eseguite dai thread deve essere:
	1) T1 estrae un numero e lo comunica al thread padre;
	2) T2 estrae un numero e lo comunica al thread padre;
	3) il thread padre esegue le operazioni sopra descritte;
	e così via.
*/
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>

pthread_mutex_t M; /* mutex per mutua esclusione */
pthread_cond_t C; /* variabile condizione per sincronizzazione */
int turno=0; /* variabile condivisa per sincronizzazione */
int x[2]={0,0};
const int X=10;
const int MAX=41;

void *th_code(void *arg){
    int id=(int)arg; // identificatore thread
    srand(time(NULL)+id);
    while (1) {
        pthread_mutex_lock(&M);
        while (turno!=id) { pthread_cond_wait(&C,&M);}

        x[id]=rand()%X+1;
        printf("thread %d x=%d \n",id,x[id]);
        turno++;
        usleep(100000);
        pthread_cond_signal(&C);
        pthread_mutex_unlock(&M);

    }
}

int main () {
    int i,id=2;
    int S[2]={0,0};
    pthread_t th[2];
    pthread_mutex_init (&M,NULL);
    pthread_cond_init(&C,NULL);

    for(i=0; i<2;i++) {
        if (pthread_create(&th[i],NULL,th_code,(int *)i) !=0) {
            fprintf (stderr, "errore create thread  \n");
            exit(1);
        }
    }
    while (!(S[0]>MAX || S[1]>MAX)) {
        pthread_mutex_lock(&M);
        while(id!=turno) {pthread_cond_wait(&C,&M);}
        if (x[0]>x[1])
            S[0]++;
        else if (x[0]<x[1])
            S[1]++;
        else {
            S[0]--;
            S[1]--;
        }
        printf("main: x1=%d, x2=%d, S1=%d, S2=%d \n\n",x[0],x[1],S[0],S[1]);
        turno=0;
        pthread_cond_signal(&C);
        pthread_mutex_unlock(&M);
    }
}

