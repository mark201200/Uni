#include <cstdio>
#include <cstring>
//sorta un array di stringhe
const int l1 = 10;
const int l2 = 50;

void bubbleSort(char list[l1][l2]) {
    char temp[l2];
    int i = 0, j;
    int swapped = 1;
    while (swapped == 1) {
        swapped = 0;
        for (j = 0; j < l1 - 1 - i; j++) {
            if (strcmp(list[j], list[j + 1]) == 1) {
                memcpy(temp, list[j], l2);
                memcpy(list[j], list[j + 1], l2);
                memcpy(list[j + 1], temp, l2);
                swapped = 1;
            }
        }
        i++;
    }
}

int main() {
    char a[l1][l2] = {"aa", "aj", "ai", "ab", "ac", "ad", "af", "ag", "ae", "ah"};
    int i, j = 0;
    bubbleSort(a);
    for (i = 0; i < l1; i++)
        printf("%s\n", a[i]);
}
