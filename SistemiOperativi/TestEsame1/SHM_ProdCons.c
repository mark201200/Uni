#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/types.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/stat.h>

#define SIZE 4096

void consumatore() {
    int shm_desc = shm_open("/SHM", O_RDONLY, 0666);
    void *shm_ptr = mmap(0, SIZE, PROT_READ, MAP_SHARED, shm_desc, 0);
    printf("Consumatore riceve:\n%s\n", (char *) shm_ptr);
    exit(0);
}

int main() {
    pid_t pid = fork();
    if (pid == 0) consumatore();

    int shm_desc = shm_open("/SHM", O_CREAT | O_RDWR, 0666);
    ftruncate(shm_desc, SIZE);
    void *shm_ptr = mmap(0, SIZE, PROT_WRITE, MAP_SHARED, shm_desc, 0);
    char *msg = "Messaggio!";
    sprintf(shm_ptr, "%s", msg);
    printf("Produttore manda messaggio.\n");
    shm_ptr += strlen(msg);
    wait(NULL);
    shm_unlink("/SHM");
}
