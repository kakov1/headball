#include "serverUtil.h"
#include <stdbool.h>
#include <unistd.h>
#include <pthread.h>

struct AcceptedSocket
{
    int AcceptedSocketFD;
    struct sockaddr_in address;
    int error;
    bool acceptedSuccesfully;
};

struct playerInfo {
    int socketFD;
    int playerNum;
};

struct AcceptedSocket acceptedSockets[10];
int playersCount = 0;

struct AcceptedSocket *acceptIncomingConnection(int serverSocketFD)
{

    struct sockaddr_in clientAddress;
    int clientAddressSize = sizeof(struct sockaddr);
    int clientSocketFD = accept(serverSocketFD, (struct sockaddr *)&clientAddress, &clientAddressSize);

    struct AcceptedSocket *acceptedSocket = malloc(sizeof(struct AcceptedSocket));
    acceptedSocket->address = clientAddress;
    acceptedSocket->AcceptedSocketFD = clientSocketFD;
    acceptedSocket->acceptedSuccesfully = clientSocketFD > 0;

    if (!acceptedSocket->acceptedSuccesfully)
    {
        acceptedSocket->error = clientSocketFD;
    }

    return acceptedSocket;
}

void closeSockets() {
    for (int i = 0; i < playersCount; i++) {
        close(acceptedSockets[i].AcceptedSocketFD);
    }
}

void sendReceivedMessageToClients(char *buffer, int socketFD)
{

    for (int i = 0; i < playersCount; i++)
    {
        if (acceptedSockets[i].AcceptedSocketFD != socketFD)
        {
            int sendingResult = send(acceptedSockets[i].AcceptedSocketFD,
                                     buffer, strlen(buffer), 0);
            if (sendingResult < 0)
            {
                printf("something went wrong with sending\n");
            }
        }
    }
}

void receiveAndPrintData(void* args)
{
    struct playerInfo* player = (struct playerInfo* )args;

    char buffer[1024];

    while (true)
    {

        ssize_t amountReceived = recv(player->socketFD, buffer, 1024, 0);

        if (amountReceived > 0)
        {
            buffer[amountReceived] = 0;

            sendReceivedMessageToClients(buffer, player->socketFD);
        }
        if (amountReceived < 0)
        {
            send(acceptedSockets[playersCount - player->playerNum].AcceptedSocketFD,
                 &playersCount, sizeof(int), 0);
            closeSockets();
            playersCount = 0;
            break;
        }
    }
    close(player->socketFD);
}

void receiveAndPrintNewThread(struct AcceptedSocket *pSocket, int playerNum)
{
    struct playerInfo* args = malloc(sizeof(struct playerInfo));
    args->socketFD = pSocket->AcceptedSocketFD;
    args->playerNum = playerNum;
    
    pthread_t id;
    pthread_create(&id, NULL, (void *)receiveAndPrintData, (void *)args);
}

void acceptingConnections(int serverSocketFD)
{

    while (true)
    {   if (playersCount <2) {
            struct AcceptedSocket *clientSocket = acceptIncomingConnection(serverSocketFD);
            acceptedSockets[playersCount++] = *clientSocket;

            send(clientSocket->AcceptedSocketFD, &playersCount, sizeof(int), 0);

            if (playersCount == 2) {
                send(acceptedSockets[0].AcceptedSocketFD, &playersCount,
                    sizeof(int), 0);
            }

            receiveAndPrintNewThread(clientSocket, playersCount);

            free(clientSocket);
        }
    }
}

int main()
{
    int serverSocketFD = createTCPIPv4Socket();
    struct sockaddr_in *serverAddress = createIPv4Address("127.0.0.1", 2000);

    int result = bind(serverSocketFD, (struct sockaddr *)serverAddress, sizeof(*serverAddress));

    if (result == 0)
    {
        printf("socket was bound successfully\n");
    }
    else
    {
        printf("something went wrong with bounding socket\n");
        return 1;
    }

    int listenResult = listen(serverSocketFD, 10);

    if (listenResult != 0)
    {
        printf("something went wrong with listening\n");
        return 1;
    }

    acceptingConnections(serverSocketFD);

    if (playersCount < 0) {
        shutdown(serverSocketFD, SHUT_RDWR);
    }

    return 0;
}
