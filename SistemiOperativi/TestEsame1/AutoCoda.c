#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>

#define THREADS 20
int posti = 10;
pthread_mutex_t mutex;
pthread_cond_t cond;

void *automobile(void *arg) {
    char park[5];
    int id = (int) arg;
    srand(time(NULL) + id);

    if (id % 2 == 0) {
        strcpy(park, "NORD");
    } else {
        strcpy(park, "SUD");
    }

    pthread_mutex_lock(&mutex);
    printf("Auto %i arriva al parcheggio da %s\n", id, park);

    if (posti < 1) {
        printf("Auto %i in coda NORD\n", id, park);
        pthread_cond_wait(&cond, &mutex);
    }

    printf("Auto %i entra nel parcheggio da NORD\n", id, park);

    posti--;
    pthread_mutex_unlock(&mutex);

    sleep(rand() % 10 + 1);

    pthread_mutex_lock(&mutex);
    posti++;
    printf("Auto %i esce dal parcheggio\n\nCi sono %i posti disponibili nel parcheggio\n\n", id, posti);
    pthread_cond_signal(&cond);
    pthread_mutex_unlock(&mutex);
}

int main() {
    pthread_mutex_init(&mutex, NULL);
    pthread_cond_init(&cond, NULL);
    pthread_t threads[THREADS];
    int i;

    for (i = 0; i < THREADS; i++) {
        pthread_create(&threads[i], NULL, automobile, (int *) i);
        usleep(500000);
    }

    for (i = 0; i < THREADS; i++) pthread_join(threads[i], NULL);
}