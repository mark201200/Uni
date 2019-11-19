#include <stdio.h>
#include <stdlib.h>

float *arraysum(float a[], float b[], int n) {
    int i;
    float *c = malloc(n * sizeof(float));
    for (i = 0; i < n; i++)
        c[i] = a[i] + b[i];
    return c;
}

int main() {
    int i;
    float a[] = {1, 2, 3, 4, 5};
    float b[] = {5, 4, 3, 2, 1};
    float *c = arraysum(a, b, sizeof(a) / sizeof(float));
    for (i = 0; i < (sizeof(a) / sizeof(float)); i++)
        printf("\n%.2f", c[i]);
}