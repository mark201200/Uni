#include <stdio.h>
#include <stdlib.h>

void seq(char number[3], int n) {
    if(n > 0) {
        number[3-n] = '0';
        seq(number, n - 1);
        number[3-n] = '1';
        seq(number, n - 1);
    }
    else {
        printf("%s \n", number);
    }
}

int main(){
char *number= malloc(4* sizeof(char));
seq(number,3);

}
