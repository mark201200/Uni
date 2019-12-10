#include <stdio.h>
#include <stdlib.h>

int ricbin(int a[], int n, int f){
	if(f<a[0] || f>a[n]) return -1;
	int p=0,u=n,m;
	while(p<=u){
		m=(p+u)/2;
		if(a[m]==f)	return m;	//Se lo trovo direttamente, tutto ok.
		if(a[m]<f)	p=m+1;		//Se l'elemento è più piccolo di quello che cerco, dico che il primo elemento è m(la metà) + 1
		else 		u=m-1;		//Se l'elemento è più grande, dico che l'ultimo elemento è m - 1
	}
	return -1;
}




int main(){
	int array[] = {0,1,2,3,4,5,6,7,8,9};
	int size = sizeof(array)/sizeof(int);
	printf("%d ",ricbin(array,size-1,2));
}
