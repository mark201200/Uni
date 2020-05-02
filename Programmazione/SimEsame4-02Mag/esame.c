#include <stdio.h>
#include <stdlib.h>
#include <time.h>

typedef struct nodo_t {
    int val;
    struct nodo_t *prec;
    struct nodo_t *succ;
} nodo_t;

void swap(nodo_t *a[], int x, int y) { //scambia gli elementi in posizione x e y
    nodo_t *temp = a[x];
    a[x] = a[y];
    a[y] = temp;
}

int listlen(nodo_t *a) { //calcola il numero di elementi in una lista
    int i = 1;
    nodo_t *cur = a;
    while (cur->succ != NULL) {
        i++;
        cur = cur->succ;
    }
    return i;
}

nodo_t *creaHead(int v) {
    nodo_t *head = malloc(sizeof(nodo_t));
    if (head == NULL) exit(EXIT_FAILURE);

    head->val = v;                      // -> equivale a fare *head.val
    head->prec = NULL;                  //scrivendo head si ottiene l'indirizzo, scrivendo *head si ottengono i valori
    head->succ = NULL;

    return head;
}

/* Aggiunge un nodo alla fine della lista */
void aggiungiEnd(nodo_t *nodo, int val) {
    nodo_t *add = malloc(sizeof(nodo_t));
    if (add == NULL) exit(EXIT_FAILURE);

    nodo_t *iter = nodo;                //il nodo che useremo per iterare
    while (iter->succ != NULL)          //finchè il nodo che ho preso non ha un nodo successivo, vado avanti
        iter = iter->succ;

    add->prec = iter;
    add->succ = NULL;
    add->val = val;
    iter->succ = add;
}

int distr(nodo_t *a[], int sx, int dx) {
    srand(time(NULL));
    int pivot = (rand() % (dx - sx + 1)) + sx;
    int finale = sx;                            //l'elemento <= di pivot più a destra. sarà la posizione del pivot alla fine.
    int i = sx + 1;
    int j = dx;

    swap(a, pivot, sx);

    while (i <= j) {
        while (i <= j && listlen(a[i]) <=
                         listlen(a[sx])) {   //mando avanti i finchè a[i] è minore o uguale del pivot (che adesso è a sx)
            finale = i;                             //se a[i] è <= pivot assegno finale
            i++;
        }

        while (i <= j && listlen(a[j]) > listlen(a[sx]))
            j--;

        if (i <= j)
            swap(a, i, j);

    }

    swap(a, sx, finale);                            //rimetto il pivot al suo posto, cioè al confine tra i <= e i >

    return finale;
}

void quicksort(nodo_t *a[], int sx, int dx) {
    int pivot;
    if (sx <= dx) {
        pivot = distr(a, sx, dx);
        quicksort(a, sx, pivot - 1);
        quicksort(a, pivot + 1, dx);
    }
}

int main() {
    int i;
    nodo_t *a[4];
    a[0] = creaHead(10);
    aggiungiEnd(a[0], 1);
    aggiungiEnd(a[0], 1);
    a[1] = creaHead(11);
    aggiungiEnd(a[1], 1);
    aggiungiEnd(a[1], 1);
    aggiungiEnd(a[1], 1);
    aggiungiEnd(a[1], 1);
    aggiungiEnd(a[1], 1);
    aggiungiEnd(a[1], 1);
    aggiungiEnd(a[1], 1);
    aggiungiEnd(a[1], 1);
    a[2] = creaHead(12);
    aggiungiEnd(a[2], 1);
    aggiungiEnd(a[2], 1);
    a[3] = creaHead(13);
    aggiungiEnd(a[3], 1);
    aggiungiEnd(a[3], 1);
    aggiungiEnd(a[3], 1);
    int size = (sizeof(a) / sizeof(int)) - 1;
    quicksort(a, 0, size);

    printf("%d %d %d %d", listlen(a[0]), listlen(a[1]), listlen(a[2]), listlen(a[3]));

}