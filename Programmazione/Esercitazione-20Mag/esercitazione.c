#include <stdio.h>
#include <stdlib.h>

typedef struct nodo_t {
    int val;
    struct nodo_t *prec;
    struct nodo_t *succ;
} nodo_t;

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

int ind_set(nodo_t *a[], int I[], int n) {
    int i, ret=1;
    nodo_t *cur;
    for (i = 0; i < n; i++) {
        if (I[i] == 1) {
            cur = a[i];
            while ((cur != NULL) && (ret == 1)) {
                if (I[cur->val]==1)
                    ret=0;
                cur = cur->succ;
            }
        }
    }
    if (ret) return 1;
    else return 0;
}

int main() {
    int n = 4;
    int i[] = {1, 0, 1, 0};
    nodo_t *a[4];
    a[0] = creaHead(2);
    aggiungiEnd(a[0], 3);

    a[1] = creaHead(3);

    a[2] = creaHead(1);
    aggiungiEnd(a[2], 3);
    aggiungiEnd(a[2], 0);

    a[3] = creaHead(2);
    printf("%d", ind_set(a, i, n));
}