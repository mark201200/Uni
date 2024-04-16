// gcc -fno-stack-protector -z execstack vuln.c -o vuln -m32 -no-pie
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
int bof(char *str)
{
	char buffer[12];
	strcpy(buffer,str);
	return 1;
}
int main(int argc, char **argv)
{
	bof(argv[1]);
	printf("Returned Properly\n");
	return 1;
}
