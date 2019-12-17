#include <stdio.h>

/*Data una stringa di sole parentesi es. "()()((()))" trovare per una parentesi (indice) l'indice della parentesi abbinata*/

int parentesi(char *p, int n, int j) {
    int x = 1, c = 0, i = 1;
    char f = ')';
    if (p[j] == ')') {
        x = -1;
        f--;
    } else if (p[j] != '(') return -1;

    while (j >= 0 && j < n) {
        j = j + x;
        if (p[j] == f && c == 0) return j;
        if (p[j] == f && c != 0) c--;
        else c++;
    }
    return -1;
}

int main() {
    char pare[] = "(()()((()))(())(())(((((())))))()()())";
    int s = (sizeof(pare) / sizeof(char)) - 1;
    int i = 8;
    for (i = 0; i < s; i++) {
        int res = parentesi(pare, s, i);
        printf("%d %d\n", i, res);
    }
}