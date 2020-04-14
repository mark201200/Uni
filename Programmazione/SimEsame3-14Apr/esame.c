#include <stdio.h>
#include <stdlib.h>

struct nodo {
    int valore;
    struct nodo *succ;
    struct nodo *prec;
};
typedef struct nodo nodo;

nodo *ListaMediano(nodo *a) {
    nodo* n1 = a;
    nodo* n2 = a;

    while(n2->succ != NULL && n2->succ->succ != NULL){
        n1=n1->succ;
        n2=n2->succ->succ;
    }

    return n1;
}


void aggiungiEnd(nodo *nodo1, int val) {
    nodo *add = malloc(sizeof(nodo));
    if (add == NULL) exit(EXIT_FAILURE);

    nodo *iter = nodo1;                //il nodo che useremo per iterare
    while (iter->succ != NULL)          //finchè il nodo che ho preso non ha un nodo successivo, vado avanti
        iter = iter->succ;

    add->prec = iter;
    add->succ = NULL;
    add->valore = val;
    iter->succ = add;
}

int main() {
    int i;
    nodo *head = malloc(sizeof(nodo));
    head->prec = NULL;
    head->succ = NULL;
    for (i = 1; i <= 99; i++)
        aggiungiEnd(head, i);

    int a = ListaMediano(head)->valore;

    printf("\n\n%d",a);
}

