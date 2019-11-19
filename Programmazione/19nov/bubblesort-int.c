#include <stdio.h>

void bubbleSort(int list[], int len) {
    int temp;
    int i = 0, j;
    int swapped = 1;
    while (swapped == 1) {
        swapped = 0;
        for (j = 0; j < len - 1 - i; j++) {
            //Entro nella condizione lunghezza-1 * lunghezza-1-i volte, nel caso peggiore. quindi, visto che il
            //-1 e il -1-n non ci interessano, l'ordine di grandezza è lunghezza^2
            if (list[j] > list[j + 1]) {
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
    int a[] = {1, 0, 2, 9, 3, 8, 4, 7, 5, 6};
    int i;
    bubbleSort(a, sizeof(a) / sizeof(int));
    for (i = 0; i < (sizeof(a) / sizeof(int)); i++)
        printf("\n%d", a[i]);
}
