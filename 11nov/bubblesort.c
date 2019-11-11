#include <stdio.h>
#include <string.h>

void bubbleSort(char list[], int len) {
    int temp;
    int i=0, j;
    int swapped = 1;

    while (swapped == 1) {
        swapped = 0;
        for (j = 0; j < len - 1 - i; j++) {
            //Entro nella condizione lunghezza-1 * lunghezza-1-i volte, nel caso peggiore. quindi, visto che il
            //-1 e il -1-n non ci interessano, l'ordine di grandezza è lunghezza^2
            if (list[j] > list[j + 1]) {
                printf("swappo %c e %c, posizione %d e %d \n",list[j],list[j + 1],j,j+1);
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
    char list[] = "abcdef";
    char list1[] = "abcdfe";
    int len = sizeof(list) / sizeof(list[0]) - 1;
    int i;
    bubbleSort(list, len);
    bubbleSort(list1, len);
    for (i = 0; i < len+1; i++)
        printf("%c", list[i]);

    printf("\n");

    for (i = 0; i < len+1; i++)
        printf("%c", list1[i]);

    if(strcmp(list,list1)==0)
        printf("Anagramma!");
}

//TODO: creare il mio strcmp