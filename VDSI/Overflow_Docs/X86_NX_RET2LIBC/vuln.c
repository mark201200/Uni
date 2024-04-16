//gcc vuln.c -o vuln -no-pie -m32 
#include <stdio.h>

void foo(char *arg){
	char buf[8];
	memcpy(buf, arg ,strlen(arg));
	printf("%s",buf);
}

int main(int argc, char *argv[])
{
	foo(argv[1]);
}
