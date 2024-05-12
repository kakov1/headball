#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <malloc.h>

struct sockaddr_in *createIPv4Address(char *ip, int port);

int createTCPIPv4Socket();