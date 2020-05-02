#include "TCPCast_C.h"
#include "DefaultMutex_C.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <errno.h>
#include <arpa/inet.h>

// private
typedef struct TCPCast_C
{
    int m_socket;
    char m_ifAddress[16];
    short m_ifPort;
    int m_isClient;
    int m_numClients;
    struct DefaultMutex_C* m_pSendLock;
}TCPCast_C;

// public
struct TCPCast_C* createTCPCast_C()
{
    TCPCast_C* pTCPCast = (TCPCast_C*)malloc(sizeof(TCPCast_C));
    memset(pTCPCast, 0, sizeof(TCPCast_C));
    return pTCPCast;
}

void freeTCPCast_C(struct TCPCast_C** pTCPCast)
{
    if (*pTCPCast)
    {
        TCPCast_C_Stop(*pTCPCast);
        free(*pTCPCast);
        *pTCPCast = NULL;
    }
}

enum TCPStatus TCPCast_C_InitComponent(struct TCPCast_C* pTCPCast, char const * const ifAddress, int ifAddressLen, short ifPort, int isClient, const int numClients)
{
    if (!pTCPCast)
        return ERROR;
    if (ifAddressLen < 16 && ifAddress)
        strcpy(pTCPCast->m_ifAddress, ifAddress);
    else
        return ERROR;
    pTCPCast->m_isClient = isClient;
    if (pTCPCast->m_isClient)
    {
        pTCPCast->m_ifPort = 0;
        pTCPCast->m_numClients = 0;
    }
    else
    {
        pTCPCast->m_ifPort = ifPort;
        pTCPCast->m_numClients = numClients;
    }
    return TCPCast_C_Start(pTCPCast);
}

enum TCPStatus TCPCast_C_Start(struct TCPCast_C* pTCPCast)
{
    if (!pTCPCast)
        return ERROR;
    // create TCP socket
    if ((pTCPCast->m_socket = socket(AF_INET, SOCK_STREAM, IPPROTO_IP)) < 0)
    {
        fprintf(stderr, "[%s:%d] errono %s\n", __FUNCTION__, __LINE__, strerror(errno));
        return ERROR;
    }
    // set address and port for local address
    struct sockaddr_in local_addr;
    local_addr.sin_family = AF_INET;
    local_addr.sin_port = htons(pTCPCast->m_ifPort);
    local_addr.sin_addr.s_addr = strcmp(pTCPCast->m_ifAddress, "") == 0 ? htonl(INADDR_ANY) : inet_addr(pTCPCast->m_ifAddress);
    if (!pTCPCast->m_isClient) // do binding if the socket need to listen incoming message
    {
        // bind local address
        if (bind(pTCPCast->m_socket, (struct sockaddr *)&local_addr, sizeof(local_addr)) < 0)
        {
            fprintf(stderr, "[%s:%d] errono %s\n", __FUNCTION__, __LINE__, strerror(errno));
            return ERROR;
        }
        // get ready the server
        listen(pTCPCast->m_socket, pTCPCast->m_numClients);
    }
    // set receive buffer size
    int recevBufSize = 1024 * 256; // 256 kByte
    setsockopt(pTCPCast->m_socket, SOL_SOCKET, SO_RCVBUF, (char *)&recevBufSize, sizeof(recevBufSize));
    return SUCCESS;
}

void TCPCast_C_Stop(struct TCPCast_C* pTCPCast)
{
    if (!pTCPCast)
        return;
    shutdown(pTCPCast->m_socket, 0x00);
}

enum TCPStatus TCPCast_C_Connect(struct TCPCast_C* pTCPCast, char const * const toAddress, int toAddressLen, const short toPort)
{
    if (!pTCPCast || !toAddress || toAddressLen <= 0)
        return ERROR;
    struct sockaddr_in toInfo;
    memset(&toInfo, 0, sizeof(struct sockaddr_in));
    toInfo.sin_family = PF_INET;
    toInfo.sin_addr.s_addr = inet_addr(toAddress);
    toInfo.sin_port = htons(toPort);

    int err = connect(pTCPCast->m_socket, (struct sockaddr*)&toInfo, sizeof(struct sockaddr_in));
    if (err == -1)
    {
        fprintf(stderr, "[%s:%d] errono %s\n", __FUNCTION__, __LINE__, strerror(errno));
        return ERROR;
    }
    return SUCCESS;
}

enum TCPStatus TCPCast_C_ClientSend(struct TCPCast_C* pTCPCast, char const * const sendMsg, const int msgLength)
{
    if (!pTCPCast)
        return ERROR;
    if (!sendMsg || msgLength <= 0)
        return SUCCESS;
    if (send(pTCPCast->m_socket, sendMsg, msgLength, 0) != msgLength)
    {
        fprintf(stderr, "[%s:%d] errono %s\n", __FUNCTION__, __LINE__, strerror(errno));
        return ERROR;
    }
    return SUCCESS;
}

enum TCPStatus TCPCast_C_ClientRecv(struct TCPCast_C* pTCPCast, char* receiveBuffer, int receiveBufferLen, int* byteRecv)
{
    if (!pTCPCast || !receiveBuffer || receiveBufferLen <= 0 || !byteRecv)
        return ERROR;
    if ((*byteRecv = recv(pTCPCast->m_socket, receiveBuffer, receiveBufferLen, MSG_WAITALL)) < 0)
    {
        fprintf(stderr, "[%s:%d] errono %s\n", __FUNCTION__, __LINE__, strerror(errno));
        return ERROR;
    }
    return SUCCESS;
}

int TCPCast_C_Accept(struct TCPCast_C* pTCPCast)
{
    if (!pTCPCast)
        return -1;
    struct sockaddr_in clientInfo;
    int infoLength = sizeof(clientInfo);
    memset(&clientInfo, 0, infoLength);
    int clientHandle = accept(pTCPCast->m_socket, (struct sockaddr*)&clientInfo, (socklen_t*)&infoLength);

    fprintf(stdout, "Received client %s:%d", inet_ntoa(clientInfo.sin_addr), (int)ntohs(clientInfo.sin_port));
    return clientHandle;
}

enum TCPStatus TCPCast_C_ServerSend(struct TCPCast_C* pTCPCast, int clientHandle, char const * const sendMsg, const int msgLength)
{
    if (!pTCPCast)
        return ERROR;
    if (!sendMsg || msgLength <= 0)
        return SUCCESS;
    Lock_DefaultMutex_C(pTCPCast->m_pSendLock);

    if (send(clientHandle, sendMsg, msgLength, 0) != msgLength)
    {
        fprintf(stderr, "[%s:%d] errono %s\n", __FUNCTION__, __LINE__, strerror(errno));
        Unlocak_DefaultMutex_C(pTCPCast->m_pSendLock);
        return ERROR;
    }
    Unlocak_DefaultMutex_C(pTCPCast->m_pSendLock);
    return SUCCESS;
}

enum TCPStatus TCPCast_C_ServerRecv(struct TCPCast_C* pTCPCast, int clientHandle, char* receiveBuffer, int receiveBufferLen, int* byteRecv)
{
    if (!pTCPCast || !receiveBuffer || receiveBufferLen <= 0 || !byteRecv)
        return ERROR;
    if ((*byteRecv = recv(clientHandle, receiveBuffer, receiveBufferLen, MSG_WAITALL)) < 0)
    {
        fprintf(stderr, "[%s:%d] errono %s\n", __FUNCTION__, __LINE__, strerror(errno));
        return ERROR;
    }
    return SUCCESS;
}
