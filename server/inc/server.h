#ifndef SERVER_H
#define SERVER_H

#include <arpa/inet.h>
#include <malloc.h>
#include <pthread.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

extern int playersCount;

struct AcceptedSocket;

struct playerInfo;

struct AcceptedSocket *acceptIncomingConnection(int serverSocketFD);

struct sockaddr_in *createIPv4Address(char *ip, int port);

int createTCPIPv4Socket();

void closeSockets();

void receiveAndPrintData(void *args);

void receiveAndPrintNewThread(struct AcceptedSocket *pSocket, int playerNum);

void acceptingConnections(int serverSocketFD);

#endif