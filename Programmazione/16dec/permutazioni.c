#include <stdio.h>
//fucked.
void swap(char *str, int a, int b) {
    char swap = str[b];
    str[b] = str[a];
    str[a] = swap;
}

void permutaz(char *str, int start, int n) {
    if (start == n) {
        printf("%s\n", str);
    }

    int i;
    for (i = start; i < n-1; i++) {
        swap(str, i, i + 1);
        permutaz(str, start + 1, n);
        swap(str, i, i + 1);
    }
}

int main() {
    char str[] = "ABC";
    permutaz(str, 0, (sizeof(str) / sizeof(char))-1);
}