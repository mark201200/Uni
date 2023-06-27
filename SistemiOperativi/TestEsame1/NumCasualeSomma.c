#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>
#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Wvoid-pointer-to-int-cast"
#pragma clang diagnostic ignored "-Wint-to-pointer-cast"
/* 08-07-22
Realizzate un programma multi-thread in C, completo di commento, che svolga quanto segue:
Il thread main crea due thread figli T1 e T2. Entrambi i thread figli eseguono un ciclo indeterminato durante il quale, ad ogni
iterazione, generano un numero intero casuale compreso tra 0 e 5 che comunicano al padre. Il thread padre, per ogni coppia di
numeri che riceve dai thread figli ne fa la somma e nel caso essa sia un numero pari incrementa di 1 la variabile S1, nel caso
in cui la somma sia un numero dispari incrementa di 1 la variabile S2; se la somma vale 0 assegna sia a S1 che a S2 il valore
0. Quanto il thread padre verifica che il valore di S1 o di S2 ha superato il valore 11, visualizza sullo schermo il valore delle
due variabili e il programma termina. La sequenza temporale delle operazioni eseguite dai thread deve essere: 1) T1 estrae un
numero e lo comunica al thread padre; 2) T2 estrae un numero e lo comunica al thread padre; 3) il thread padre esegue le
operazioni sopra descritte; e così via.
 */
pthread_mutex_t mutex;
pthread_cond_t cond;
const int MAX = 11;
int x[2];
int s1 = 0;
int s2 = 0;
int turno = 0;

void * thread (void* id){
    int tid = (int) id;
    srand(time(NULL)+tid);
    while(1) {
        pthread_mutex_lock(&mutex);
        while (turno != tid) pthread_cond_wait(&cond, &mutex);
        x[tid] = rand() % 5;
        printf("Thread %i turno %i\n",tid ,turno);
        sleep(1);
        turno++;
        pthread_cond_signal(&cond);
        pthread_mutex_unlock(&mutex);
    }
}

int main(){
    int i;
    int somma = 0;
    pthread_t thread1;
    pthread_t thread2;
    pthread_mutex_init(&mutex,NULL);
    pthread_cond_init(&cond,NULL);


    pthread_create(&thread1,NULL,thread,(int*)0);
    pthread_create(&thread2,NULL,thread,(int*)1);

    while(s1<MAX && s2<MAX) {
        printf("\nmain turno %i\n",turno);
        pthread_mutex_lock(&mutex);
        while (turno != 2) pthread_cond_wait(&cond, &mutex);

        if (x[0] + x[1] == 0) {
            s1 = 0;
            s2 = 0;
        } else if ((x[0] + x[1]) % 2 == 0) s1++;
        else s2++;
        printf("Processo Main turno %i\n",turno);
        printf("x1: %i\nx2: %i\n",x[0],x[1]);
        printf("s1: %i\ns2: %i\n",s1,s2);

        turno = 0;

        pthread_cond_signal(&cond);
        pthread_mutex_unlock(&mutex);
        sleep(1);
    }

    printf("****FINE****\ns1: %i\ns2: %i",s1,s2);




}
#pragma clang diagnostic pop