#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <malloc.h>
#include <stdbool.h>
#include <unistd.h>
#include <pthread.h>
#include "serverUtil.h"


void listenAndPrint(int socketFD) {
    char buffer[1024];
    
    while (true) {
        ssize_t amountReceived = recv(socketFD, buffer, 1024, 0);

        if (amountReceived > 0) {
            buffer[amountReceived] = 0;
            printf("Response was %s\n", buffer);

        }
        if (amountReceived == 0) {
            break;
        }
    }
    close(socketFD);
}


void listeningAndPrintNewThread(int socketFD) {
    pthread_t id;
    pthread_create(&id, NULL, (void *)listenAndPrint, (void* )(__intptr_t)socketFD);
}


int main() {

    int socketFD = createTCPIPv4Socket();
    
    struct sockaddr_in* socketAddress = createIPv4Address("127.0.0.1", 2000); 
    
    int result = connect(socketFD, (struct sockaddr* )socketAddress, sizeof(*socketAddress));

    if (result == 0) {
        printf("connection was succesful\n");
    }

    char* name = NULL;
    size_t nameSize = 0;
    printf("please enter your name?\n");
    ssize_t nameCount = getline(&name, &nameSize, stdin);
    name[nameCount-1] = 0;

    char* line = NULL;
    size_t lineSize = 0;
    printf("type and we will send...\n");

    listeningAndPrintNewThread(socketFD);

    char buffer[1024];

    while(true)
    {
        ssize_t charCount = getline(&line, &lineSize, stdin);
        line[charCount - 1] = 0;
        sprintf(buffer, "%s:%s", name, line);

        if(charCount>0)
        {
            if(strcmp(line,"exit")==0)
                break;
            ssize_t amountWasSent = send(socketFD, buffer, strlen(buffer), 0);
        }

    }
    close(socketFD);

    return 0;
}
