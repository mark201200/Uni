#include <stdio.h>
#include <string.h>
void rimuovi_char(char *a,int index){       //rimuovere carattere all'indice index
    int i=0;
    int len=strlen(a);
    if(index>len) return;                   //se l'indice è più grande della lunghezza qualcosa non va
    for(i=index;i<len;i++){
        a[i]=a[i+1];                        //parto da index e sposto tutti i caratteri indietro di uno.
    }                                       //sovrascrivendo quindi il carattere da rimuovere
}
//costo: n
//memoria: costante
void rimuovi_non_ordinati(char *a){
    int i=0;
    char grande =a[0];                      //la lettera più "grande"
    while(a[i]!='\0'){                      //finchè non raggiungo la fine della stringa
        if(a[i]>=grande){                   //se la lettera che vedo viene dopo di quella in "grande"
            grande=a[i];
            i++;
        }
        else if(a[i]<grande){               //se la lettera che vedo viene prima
            rimuovi_char(a,i);              //rimuovo la lettera
        }
    }
}

int main(){
            char a[] = "ddabeceffgfh";
            rimuovi_non_ordinati(a);
            printf("%s",a);
}