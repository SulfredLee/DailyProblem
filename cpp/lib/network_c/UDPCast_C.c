#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <errno.h>
#include <arpa/inet.h>

#include "UDPCast_C.h"
#include "DefaultMutex_C.h"

// private
typedef struct UDPCast_C
{
    int m_socket;
    char m_ifAddress[16];
    short m_ifPort;
    int m_isClient;
    struct DefaultMutex_C* m_pSendLock;
}UDPCast_C;

// public
UDPCast_C* createUDPCast_C()
{
    UDPCast_C* pUDPCast = (UDPCast_C*)malloc(sizeof(UDPCast_C));
    memset(pUDPCast, 0, sizeof(UDPCast_C));
    return pUDPCast;
}

void freeUDPCast_C(struct UDPCast_C** pUDPCast)
{
    if (*pUDPCast)
    {
        UDPCast_C_Stop(*pUDPCast);
        free(*pUDPCast);
        *pUDPCast = NULL;
    }
}

enum UDPStatus UDPCast_C_InitComponent(struct UDPCast_C* pUDPCast, char const * const ifAddress, int ifAddressLen, short ifPort, int isClient)
{
    if (!pUDPCast)
        return ERROR;
    if (ifAddressLen < 16 && ifAddress)
        strcpy(pUDPCast->m_ifAddress, ifAddress);
    else
        return ERROR;
    pUDPCast->m_ifPort = ifPort;
    pUDPCast->m_isClient = isClient;
    return UDPCast_C_Start(pUDPCast);
}
// Set time to live
enum UDPStatus UDPCast_C_SetTTL(struct UDPCast_C* pUDPCast, int ttl)
{
    if (!pUDPCast)
        return ERROR;
    if (setsockopt(pUDPCast->m_socket, IPPROTO_IP, IP_MULTICAST_TTL, (char *)&ttl, sizeof(ttl)) < 0)
    {
        fprintf(stderr, "[%s:%d] errono %s\n", __FUNCTION__, __LINE__, strerror(errno));
        return ERROR;
    }
    return SUCCESS;
}

// Client, Server
enum UDPStatus UDPCast_C_Send(struct UDPCast_C* pUDPCast, char const * const toAddress, int toAddressLen, short toPort, char const * const sendMsg, int msgLength)
{
    if (!pUDPCast || !toAddress || toAddressLen <= 0)
        return ERROR;
    if (!sendMsg || msgLength <= 0)
        return SUCCESS;
    struct sockaddr_in to_addr;

    to_addr.sin_family = AF_INET;
    to_addr.sin_addr.s_addr = inet_addr(toAddress);
    to_addr.sin_port = htons(toPort);

    Lock_DefaultMutex_C(pUDPCast->m_pSendLock);

    if (sendto(pUDPCast->m_socket, sendMsg, msgLength, 0, (struct sockaddr*)&to_addr, sizeof(to_addr)) != msgLength)
    {
        fprintf(stderr, "[%s:%d] errono %s\n", __FUNCTION__, __LINE__, strerror(errno));
        Unlocak_DefaultMutex_C(pUDPCast->m_pSendLock);
        return ERROR;
    }
    Unlocak_DefaultMutex_C(pUDPCast->m_pSendLock);
    return SUCCESS;
}

enum UDPStatus UDPCast_C_SelectRead(struct UDPCast_C* pUDPCast, long uSec, long sec)
{
    if (!pUDPCast)
        return ERROR;
    fd_set fdread;
    int ret;

    struct timeval tm, *ptm;
    tm.tv_sec = sec;
    tm.tv_usec = uSec;
    FD_ZERO(&fdread);
    FD_SET(pUDPCast->m_socket, &fdread);
    if (uSec < 0 || sec < 0)
        ptm = NULL;
    else
        ptm = &tm;
    if ((ret = select(pUDPCast->m_socket + 1, &fdread, NULL, NULL, ptm)) >= 0)
    {
        if (ret != 0 && FD_ISSET(pUDPCast->m_socket, &fdread))
        {
            return READ;
        }
        else // if timeout and ret == 0
        {
            return SUCCESS;
        }
    }
    else
    {
        fprintf(stderr, "[%s:%d] errono %s\n", __FUNCTION__, __LINE__, strerror(errno));
        return ERROR;
    }
}

enum UDPStatus UDPCast_C_Recv(struct UDPCast_C* pUDPCast, char* fromAddress, int* fromAddressLen, short* fromPort, char* receiveBuffer, int receiveBufferLen, int* byteRecv)
{
    if (!pUDPCast || !fromAddress || !fromAddressLen || !fromPort || !receiveBuffer || receiveBufferLen <= 0 || !byteRecv)
        return ERROR;
    struct sockaddr_in remoteInfo;
    int infoLength = sizeof(remoteInfo);
    memset(&remoteInfo, 0, infoLength);
    *byteRecv = recvfrom(pUDPCast->m_socket, receiveBuffer, receiveBufferLen, 0, (struct sockaddr*)&remoteInfo, (socklen_t*)&infoLength);
    if (byteRecv <= 0)
    {
        fprintf(stderr, "[%s:%d] errono %s\n", __FUNCTION__, __LINE__, strerror(errno));
        return ERROR;
    }
    fromAddress = (char*)malloc(16);
    strcpy(fromAddress, inet_ntoa(remoteInfo.sin_addr));
    *fromAddressLen = strlen(fromAddress);
    *fromPort = ntohs(remoteInfo.sin_port);
    return SUCCESS;
}

// private
enum UDPStatus UDPCast_C_Start(struct UDPCast_C* pUDPCast)
{
    if (!pUDPCast)
        return ERROR;
    // create UDP socket
    if ((pUDPCast->m_socket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)) < 0)
    {
        fprintf(stderr, "[%s:%d] errono %s\n", __FUNCTION__, __LINE__, strerror(errno));
        return ERROR;
    }
    // set address and port for local address
    struct sockaddr_in local_addr;
    memset(&local_addr, 0, sizeof(local_addr));
    local_addr.sin_family = AF_INET;
    local_addr.sin_port = htons(pUDPCast->m_ifPort);
    local_addr.sin_addr.s_addr = strcmp(pUDPCast->m_ifAddress, "") == 0 ? htonl(INADDR_ANY) : inet_addr(pUDPCast->m_ifAddress);
    if (pUDPCast->m_isClient == 0) // do binding if the socket need to listen incoming message
    {
        // bind local address
        if (bind(pUDPCast->m_socket, (struct sockaddr *)&local_addr, sizeof(local_addr)) < 0)
        {
            fprintf(stderr, "[%s:%d] errono %s\n", __FUNCTION__, __LINE__, strerror(errno));
            return ERROR;
        }
    }
    // set receive buffer size
    int recevBufSize = 1024 * 256; // 256 kByte
    setsockopt(pUDPCast->m_socket, SOL_SOCKET, SO_RCVBUF, (char *)&recevBufSize, sizeof(recevBufSize));
    return SUCCESS;
}

void UDPCast_C_Stop(struct UDPCast_C* pUDPCast)
{
    if (!pUDPCast)
        return;
    shutdown(pUDPCast->m_socket, 0x00);
}
