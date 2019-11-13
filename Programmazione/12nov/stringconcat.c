#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *my_strcat(char s1[], char s2[]) {
    char *c = malloc((strlen(s1) + strlen(s2)) * sizeof(char));
    memset(c, 0, sizeof(c));
    memcpy(c, s1, strlen(s1) + 1); //Aggiungo 1 alla lunghezza perchè devo includere anche il terminatore.
    memcpy(&c[strlen(s1)], s2, strlen(s2) + 1); //nell'array non aggiungo 1 perchè se no termino prima la stringa
    return c;
}

void main() {
    char a[] = "ciao";
    char b[] = "fra!telloooo";
    char *c = my_strcat(a, b);
    printf("%s ", c);
}