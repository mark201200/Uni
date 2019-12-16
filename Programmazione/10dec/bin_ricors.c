#include <stdio.h>
#include <stdlib.h>

#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Wfor-loop-analysis"
int ricbin(int a[],int p, int u, int f){
    if(f<a[0] || f>a[u]) return -1;
    int m;
    while(p<=u){
        m=(p+u)/2;
        if(a[m]==f)	return m;		//Se lo trovo direttamente, tutto ok.
        if(a[m]<f)	return ricbin(a,m+1,u,f);	//Se l'elemento e' piu piccolo di quello che cerco, dico che il primo elemento e' m(la meta') + 1
        else 		return ricbin(a,p,m-1,f);	//Se l'elemento e' piu grande, dico che l'ultimo elemento e' m - 1
    }
    return -1;
}




int main(){
    int array[] = {0,1,2,3,4,5,6,7,8,9};
    int size = sizeof(array)/sizeof(int);
    printf("%d ",ricbin(array,0,size-1,2));
}

#pragma clang diagnostic pop

