#include <stdio.h>
#include <string.h>

int rimuovi_stringa(char *a, char *b) {
    int i, j, ret = 0;
    int lena = strlen(a);
    int lenb = strlen(b); //lunghezza delle 2 stringhe
    for (i = 0; (i < lena) && (ret == 0); i++) {        //se ret è 1 e sono qui vuol dire che ho trovato la substring
        ret = 1;                                        //metto ret a 1
        for (j = 0; (j < lenb) && (ret == 1); j++) {
            if (a[i + j] != b[j]) ret = 0;              //se c'è un'incongruenza ret va a 0 e vado avanti di lettera
        }
    }

    if (ret) {                                          //se ho trovato la substring
        int start = i - 1;
        int end = start + j - 1;                        //inizio e fine della zona da cancellare
        int ii = 0;
        for (i = 0; i < lena; i++) {
            if (i < start || i > end) {                 //se la lettera non è da cancellare, la rimetto in a
                a[ii] = a[i];
                ii++;
            }
        }
        a[ii] = '\0';                                   //termino la stringa
    }
    return ret;
}

int main() {
    char a[] = "programmazione dei calcolatori";
    char b[] = "azione";
    int i = rimuovi_stringa(a, b);
    printf("\n%d\n%s", i, a);
}