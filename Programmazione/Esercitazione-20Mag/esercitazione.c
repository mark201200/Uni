#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void f(int *x, int i){
    *(x+x[i])=2*(*(x+i));
}

int main() {
 int a[10]={0,1,2,3,4,5,6,7,8,9};
 f(a,5);
 printf("%d",a[5]);
}