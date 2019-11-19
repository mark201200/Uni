#include <stdio.h>
#include <string.h>
//sorta un array di stringhe

void bubbleSort(char *list[], int len) {
    int temp;
    int i = 0, j;
    int swapped = 1;
    while (swapped == 1) {
        swapped = 0;
        for (j = 0; j < len - 1 - i; j++) {
            //Entro nella condizione lunghezza-1 * lunghezza-1-i volte, nel caso peggiore. quindi, visto che il
            //-1 e il -1-n non ci interessano, l'ordine di grandezza è lunghezza^2
            if (strcmp(list[][],)) {
                temp = list[j];
                list[j] = list[j + 1];
                list[j + 1] = temp;
                swapped = 1;
            }
        }
        i++;
    }
}

void main() {
    char a[10][50] = {"c", "ca", "cac", "cacc", "cacca"};
    int i;
    bubbleSort(a, sizeof(a) / sizeof(int));
    for (i = 0; i < (sizeof(a) / sizeof(int)); i++)
        printf("\n%d", a[i]);
}
