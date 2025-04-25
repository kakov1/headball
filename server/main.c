#include "server.h"

int main() {
  int serverSocketFD = createTCPIPv4Socket();
  struct sockaddr_in *serverAddress = createIPv4Address("127.0.0.1", 2000);

  int result = bind(serverSocketFD, (struct sockaddr *)serverAddress,
                    sizeof(*serverAddress));

  if (result == 0) {
    printf("socket was bound successfully\n");
  } else {
    printf("something went wrong with bounding socket\n");
    return 1;
  }

  int listenResult = listen(serverSocketFD, 10);

  if (listenResult != 0) {
    printf("something went wrong with listening\n");
    return 1;
  }

  acceptingConnections(serverSocketFD);

  if (playersCount < 0) {
    shutdown(serverSocketFD, SHUT_RDWR);
  }

  return 0;
}