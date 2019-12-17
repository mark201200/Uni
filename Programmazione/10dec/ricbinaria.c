#include <stdio.h>
#include <stdlib.h>

int ricbin(int a[], int n, int f){
	if(f<a[0] || f>a[n]) return -1;
	int p=0,u=n,m;
	while(p<=u){
		m=(p+u)/2;
		if(a[m]==f)	return m;	//Se lo trovo direttamente, tutto ok.
		if(a[m]<f)	p=m+1;		//Se l'elemento e piu piccolo di quello che cerco, dico che il primo elemento e m(la meta) + 1
		else 		u=m-1;		//Se l'elemento e piu grande, dico che l'ultimo elemento e m - 1
	}
	return -1;
}

int main(){
	int array[] = {0,1,2,3,4,5,6,7,8,9};
	int size = sizeof(array)/sizeof(int);
	printf("%d ",ricbin(array,size-1,2));
}