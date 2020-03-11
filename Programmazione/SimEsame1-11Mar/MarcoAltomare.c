#include <stdio.h>
struct punto{
    int x, y;
};
typedef struct punto punto;

void DisegnaPunti(punto p[], int n){
    int i,j,x,f;
    int maxx=-1;
    int maxy=-1;
    for(i=0;i<n;i++){
        if(p[i].x>maxx) maxx=p[i].x;
        if(p[i].y>maxy) maxy=p[i].y;
    }
    for(i=0;i<=maxy;i++){
        for(j=0;j<=maxx;j++){
            f=0;
            for(x=0;x<n;x++)
                if(p[x].x==j&&p[x].y==i) f=1;
            if(f==1) printf("X");
            else printf("_");
        }
        printf("\n");
    }
}

int main(){
    punto p[5]= {
            {3, 1},
            {8, 0},
            {1, 2},
            {0, 1},
            {3, 0},
    };

    DisegnaPunti(p,5);

}