#include <sys/socket.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#include "MultiCast_C.h"
#include "DefaultMutex_C.h"

// private
typedef struct MCast_C
{
    int m_socket;
    char m_ifAddress[16];
    short m_ifPort;
    int m_isClient;
    struct DefaultMutex_C* m_pSendLock;
}MCast_C;

// public
struct MCast_C* createMCast_C()
{
    MCast_C* pMCast = (MCast_C*)malloc(sizeof(MCast_C));
    memset(pMCast, 0, sizeof(MCast_C));
    return pMCast;
}

void freeMCast_C(struct MCast_C** pMCast)
{
    if (*pMCast)
    {
        MCast_C_Stop(*pMCast);
        free(*pMCast);
        *pMCast = NULL;
    }
}

enum MCStatus MCast_C_InitComponent(struct MCast_C* pMCast, char const * const ifAddress, int ifAddressLen, short ifPort)
{
    if (!pMCast)
        return ERROR;
    if (ifAddressLen < 16 && ifAddress)
        strcpy(pMCast->m_ifAddress, ifAddress);
    else
        return ERROR;
    pMCast->m_ifPort = ifPort;
    return MCast_C_Start(pMCast);
}

enum MCStatus MCast_C_Start(struct MCast_C* pMCast)
{
    if (!pMCast)
        return ERROR;
    // create UDP socket
    if ((pMCast->m_socket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)) < 0)
    {
        fprintf(stderr, "[%s:%d] errono %s\n", __FUNCTION__, __LINE__, strerror(errno));
        return ERROR;
    }
    // set address and port for local address
    struct sockaddr_in local_addr;
    local_addr.sin_family = AF_INET;
    local_addr.sin_port = htons(pMCast->m_ifPort);
    local_addr.sin_addr.s_addr = strcmp(pMCast->m_ifAddress, "") == 0 ? htonl(INADDR_ANY) : inet_addr(pMCast->m_ifAddress);
    setsockopt(pMCast->m_socket, IPPROTO_IP, IP_MULTICAST_IF, (char *)&local_addr.sin_addr.s_addr, sizeof(local_addr.sin_addr.s_addr));
    // allow multiple sockets to use the same PORT number
    u_int yes=1;
    if (setsockopt(pMCast->m_socket, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(yes)) < 0)
    {
        fprintf(stderr, "[%s:%d] errono %s\n", __FUNCTION__, __LINE__, strerror(errno));
        return ERROR;
    }
    // bind local address
    if (bind(pMCast->m_socket, (struct sockaddr *)&local_addr, sizeof(local_addr)) < 0)
    {
        fprintf(stderr, "[%s:%d] errono %s\n", __FUNCTION__, __LINE__, strerror(errno));
        return ERROR;
    }
    // set receive buffer size
    int recevBufSize = 1024 * 256; // 256 kByte
    setsockopt(pMCast->m_socket, SOL_SOCKET, SO_RCVBUF, (char *)&recevBufSize, sizeof(recevBufSize));

    MCast_C_SetTTL(pMCast, 35);
    return SUCCESS;
}

void MCast_C_Stop(struct MCast_C* pMCast)
{
    if (!pMCast)
        return;
    shutdown(pMCast->m_socket, 0x00);
}

enum MCStatus MCast_C_JoinGroup(struct MCast_C* pMCast, char const * const grpAddress, int grpAddressLen)
{
    if (!pMCast)
        return ERROR;
    if (!grpAddress)
        return SUCCESS;
    if (strcmp(grpAddress, "") == 0)
    {
        return SUCCESS;
    }

    struct ip_mreq mreq;
    mreq.imr_multiaddr.s_addr=inet_addr(grpAddress);
    if (strcmp(grpAddress, "") == 0)
    {
        mreq.imr_interface.s_addr=htonl(INADDR_ANY);
    }
    else
    {
        mreq.imr_interface.s_addr=inet_addr(pMCast->m_ifAddress);
    }
    if (setsockopt(pMCast->m_socket, IPPROTO_IP, IP_ADD_MEMBERSHIP, &mreq, sizeof(mreq)) < 0)
    {
        fprintf(stderr, "[%s:%d] errono %s\n", __FUNCTION__, __LINE__, strerror(errno));
        return ERROR;
    }
    return SUCCESS;
}

enum MCStatus MCast_C_LeaveGroup(struct MCast_C* pMCast, char const * const grpAddress, int grpAddressLen)
{
    if (!pMCast)
        return ERROR;
    if (!grpAddress)
        return SUCCESS;
    if (strcmp(grpAddress, "") == 0)
    {
        return SUCCESS;
    }

    struct ip_mreq mreq;
    mreq.imr_multiaddr.s_addr = inet_addr(grpAddress);
    mreq.imr_interface.s_addr = inet_addr(grpAddress);
    if (setsockopt(pMCast->m_socket, IPPROTO_IP, IP_DROP_MEMBERSHIP, (char *)&mreq, sizeof(mreq)) == -1)
    {
        fprintf(stderr, "[%s:%d] errono %s\n", __FUNCTION__, __LINE__, strerror(errno));
        return ERROR;
    }
    return SUCCESS;
}

enum MCStatus MCast_C_SelectRead(struct MCast_C* pMCast, long uSec, long sec)
{
    if (!pMCast || uSec < 0 || sec < 0)
        return ERROR;
    fd_set fdread;
    int ret;

    struct timeval tm, *ptm;
    tm.tv_sec = sec;
    tm.tv_usec = uSec;
    FD_ZERO(&fdread);
    FD_SET(pMCast->m_socket, &fdread);
    if (uSec < 0 || sec < 0)
        ptm = NULL;
    else
        ptm = &tm;
    if ((ret = select(pMCast->m_socket + 1, &fdread, NULL, NULL, ptm)) >= 0)
    {
        if (ret != 0 && FD_ISSET(pMCast->m_socket, &fdread))
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

enum MCStatus MCast_C_Recv(struct MCast_C* pMCast, char* receiveBuffer, int receiveBufferLen, char* fromAddress, int* fromAddressLen, short* fromPort, int* byteRecv)
{
    if (!pMCast || !receiveBuffer || receiveBufferLen <= 0 || !fromAddress || !fromAddressLen || !fromPort || !byteRecv)
        return ERROR;
    struct sockaddr_in remoteInfo;
    int infoLength = sizeof(remoteInfo);
    memset(&remoteInfo, 0, infoLength);
    *byteRecv = recvfrom(pMCast->m_socket, receiveBuffer, receiveBufferLen, 0, (struct sockaddr*)&remoteInfo, (socklen_t*)&infoLength);
    if (byteRecv <= 0)
    {
        fprintf(stderr, "[%s:%d] errono %s\n", __FUNCTION__, __LINE__, strerror(errno));
        return ERROR;
    }
    fromAddress = inet_ntoa(remoteInfo.sin_addr);
    *fromPort = ntohs(remoteInfo.sin_port);

    return SUCCESS;
}

enum MCStatus MCast_C_SetTTL(struct MCast_C* pMCast, int ttl)
{
    if (!pMCast)
        return ERROR;
    if (setsockopt(pMCast->m_socket, IPPROTO_IP, IP_MULTICAST_TTL, (char *)&ttl, sizeof(ttl)) < 0)
    {
        fprintf(stderr, "[%s:%d] errono %s\n", __FUNCTION__, __LINE__, strerror(errno));
        return ERROR;
    }
    return SUCCESS;
}

enum MCStatus MCast_C_Send(struct MCast_C* pMCast, char* toAddress, int toAddressLen, char const * const sendMsg, const int msgLength)
{
    if (!pMCast || !toAddress)
        return ERROR;
    if (!sendMsg || msgLength <= 0)
        return SUCCESS;
    struct sockaddr_in group_addr;

    group_addr.sin_family = AF_INET;
    group_addr.sin_addr.s_addr = inet_addr(toAddress);
    group_addr.sin_port = htons(pMCast->m_ifPort);

    Lock_DefaultMutex_C(pMCast->m_pSendLock);

    if (sendto(pMCast->m_socket, sendMsg, msgLength, 0, (struct sockaddr*)&group_addr, sizeof(group_addr)) != msgLength)
    {
        fprintf(stderr, "[%s:%d] errono %s\n", __FUNCTION__, __LINE__, strerror(errno));
        Unlocak_DefaultMutex_C(pMCast->m_pSendLock);
        return ERROR;
    }
    return SUCCESS;
}
