#include <stdio.h>
#include <string.h>

void swap(char *str, int a, int b) {
    char swap = str[b];
    str[b] = str[a];
    str[a] = swap;
}

void permutaz(char *str, int start, int n) {
    if (start == n)
        printf("%s\n", str);
    int i;
    for (i = start; i < n; i++) {
        swap(str, start, i);
        permutaz(str, start + 1, n);
        swap(str, start, i);
    }
}

int main() {
    char str[] = "ABCD";
    permutaz(str, 0, strlen(str));
}