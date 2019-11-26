#include <stdio.h>

//Esercizio: Trova il punto più in alto a sinistra.
typedef struct {
    char nome;
    int x;
    int y;
} punto;

punto altoSX(punto p[], int s) {
    int i, r = 0;
    for (i = r + 1; i < s; i++) {
        if (p[i].x < p[r].x && p[i].y > p[r].y)
            r = i;
    }
    return p[r];
}

int main() {
    punto p[] = {{'A', 1,  2},
                 {'B', 3,  6},
                 {'C', 5,  6},
                 {'D', -5, 1}};
    int size = sizeof(p) / sizeof(punto);
    punto result = altoSX(p, size);
    printf("%d %d", result.x, result.y);
}