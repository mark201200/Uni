#include <stdio.h>
#include <string.h>

int rimuovi_stringa(char *a, char *b) {
    int i, j, ret = 0;
    int lena = strlen(a);
    int lenb = strlen(b);
    for (i = 0; (i < lena) && (ret == 0); i++) {
        ret = 1;
        for (j = 0; (j < lenb) && (ret == 1); j++) {
            if (a[i + j] != b[j]) ret = 0;
        }
    }

    if (ret) {
        int start = i - 1;
        int end = start + j - 1;
        int ii = 0;
        for (i = 0; i < lena; i++) {
            if (i < start || i > end) {
                a[ii] = a[i];
                ii++;
            }
        }
        a[ii] = '\0';
    }
    return ret;
}

int main() {
    char a[] = "programmazione dei calcolatori";
    char b[] = "azione";
    int i = rimuovi_stringa(a, b);
    printf("\n%d\n%s", i, a);
}