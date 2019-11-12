#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *my_strcat(char s1[], char s2[]) {
    printf("\n%d\n", strlen(s1));
    printf("\n%d\n", strlen(s2));
    char *c = malloc((strlen(s1) + strlen(s2)) * sizeof(char));
    memset(c, 0, sizeof(c));
    memcpy(c, s1, strlen(s1));
    printf("\n%d\n", strlen(c));
//    memcpy(c ,s2,strlen(s2));
    printf("\n%d\n", strlen(c));
    return c;
}

void main() {
    char a[] = "ciao";
    char b[] = "fra!telloooo";
    char *c = my_strcat(a, b);
    printf("%s", c);
}