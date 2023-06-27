#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>

#define numStudenti 10
pthread_mutex_t mutex; //mutex usato per proteggere il numero di docenti
pthread_cond_t cond;
int numDocenti = 5;

void* thread(void * tid){
    int id = (int) tid;
    pthread_mutex_lock(&mutex);

    if (numDocenti == 0){
        printf("Studente %i in attesa\n",id);
        pthread_cond_wait(&cond,&mutex);
    }

    numDocenti--;
    printf("Studente %i chiamato dal docente per sostenere l'esame\nDocenti rimasti:%i\n",id,numDocenti);
    pthread_mutex_unlock(&mutex);
    sleep(10);
    pthread_mutex_lock(&mutex);
    printf("Studente %i conclude l'esame\n",id);
    numDocenti++;
    pthread_cond_signal(&cond);
    pthread_mutex_unlock(&mutex);
}

int main(){
    int i;
    pthread_t threads[numStudenti];
    pthread_cond_init(&cond,NULL);
    pthread_mutex_init(&mutex,NULL);

    for(i=0;i<numStudenti;i++){
        printf("Studente %i arriva\n",i);
        if (pthread_create(&threads[i],NULL,thread,(void*)i) != 0) printf("Errore!");
        sleep(1);
    }

    for(i=0;i<numStudenti;i++){
        pthread_join(threads[i],NULL);
    }

    pthread_mutex_destroy(&mutex);

}