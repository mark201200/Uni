#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *my_strcat(char s1[], char s2[]) {
    char *c = malloc((strlen(s1) + strlen(s2)) * sizeof(char)); //sizeof è abbastanza inutile ma lo lascio.
    memset(c, 0, sizeof(c));
    memcpy(c, s1, strlen(s1) + 1); //Aggiungo 1 alla lunghezza perchè devo includere anche il terminatore.
    memcpy(&c[strlen(s1)], s2, strlen(s2) + 1); //nell'array non aggiungo 1 perchè se no termino prima la stringa
    return c;
}

int main() {
    char a[100];
    char b[100];
    printf("Inserisci la prima stringa!:\n");
    gets(a);
    printf("Inserisci la seconda stringa!:\n");
    gets(b);
    char *c = my_strcat(a, b);
    printf("Stringa risult%s ", c);
}