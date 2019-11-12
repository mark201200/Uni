#include <stdio.h>
#include <string.h>

int my_strlen(char string[]){
    int i=0,len=0;
    while(string[i]!='\0'){
        i++;
        len++;
    }
    return len;
}

int my_strcmp(char string[], char string1[]){
    int i;
    if(my_strlen(string)!=my_strlen(string1))
        return -1;
    else{
        for(i=0;i<my_strlen(string);i++){
            if(string[i]!=string1[i])
                return -1;
        }
        return 0;
    }
}

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
    int i;
    bubbleSort(list, my_strlen(list));
    bubbleSort(list1, my_strlen(list1));
    for (i = 0; i < my_strlen(list); i++)
        printf("%c", list[i]);

    printf("\n");

    for (i = 0; i < my_strlen(list1); i++)
        printf("%c", list1[i]);

    if(my_strcmp(list,list1)==0)
        printf("Anagramma!");
}

//TODO: creare il mio strcmp