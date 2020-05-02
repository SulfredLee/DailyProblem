#include "UDPCast.h"
#include "Logger.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <errno.h>
#include <arpa/inet.h>

#include <iostream>

UDPCast::UDPCast()
{
}

UDPCast::~UDPCast()
{
    Stop();
}

UDPCast::UDPStatus UDPCast::InitComponent(const std::string& ifAddress, const short ifPort, bool isClient)
{
    m_ifAddress = ifAddress;
    m_ifPort = ifPort;
    m_isClient = isClient;
    return Start();
}

UDPCast::UDPStatus UDPCast::Start()
{
    // create UDP socket
    if ((m_socket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)) < 0)
    {
        LOGMSG_ERR("errono: %s\n", strerror(errno));
        return UDPStatus::ERROR;
    }
    // set address and port for local address
    struct sockaddr_in local_addr;
    memset(&local_addr, 0, sizeof(local_addr));
    local_addr.sin_family = AF_INET;
    local_addr.sin_port = htons(m_ifPort);
    local_addr.sin_addr.s_addr = m_ifAddress == "" ? htonl(INADDR_ANY) : inet_addr(m_ifAddress.c_str());
    if (!m_isClient) // do binding if the socket need to listen incoming message
    {
        // bind local address
        if (bind(m_socket, (struct sockaddr *)&local_addr, sizeof(local_addr)) < 0)
        {
            LOGMSG_ERR("errono: %s\n", strerror(errno));
            return UDPStatus::ERROR;
        }
    }
    // set receive buffer size
    int recevBufSize = 1024 * 256; // 256 kByte
    setsockopt(m_socket, SOL_SOCKET, SO_RCVBUF, (char *)&recevBufSize, sizeof(recevBufSize));
    return UDPStatus::SUCCESS;
}

void UDPCast::Stop()
{
    shutdown(m_socket, 0x00);
}

UDPCast::UDPStatus UDPCast::SetTTL(int ttl)
{
    if (setsockopt(m_socket, IPPROTO_IP, IP_MULTICAST_TTL, (char *)&ttl, sizeof(ttl)) < 0)
    {
        LOGMSG_ERR("errono: %s ttl: %d\n", strerror(errno), ttl);
        return UDPStatus::ERROR;
    }
    return UDPStatus::SUCCESS;
}

UDPCast::UDPStatus UDPCast::Send(std::string& toAddress, short& toPort, char const * const sendMsg, const int msgLength)
{
    struct sockaddr_in to_addr;

    to_addr.sin_family = AF_INET;
    to_addr.sin_addr.s_addr = inet_addr(toAddress.c_str());
    to_addr.sin_port = htons(toPort);

    DefaultLock lock(m_sendLock);

    if (sendto(m_socket, sendMsg, msgLength, 0, (sockaddr*)&to_addr, sizeof(to_addr)) != msgLength)
    {
        LOGMSG_ERR("errono: %s\n", strerror(errno));
        return UDPStatus::ERROR;
    }
    return UDPStatus::SUCCESS;
}

UDPCast::UDPStatus UDPCast::SelectRead(long uSec, long sec)
{
    fd_set fdread;
    int ret;

    struct timeval tm, *ptm;
    tm.tv_sec = sec;
    tm.tv_usec = uSec;
    FD_ZERO(&fdread);
    FD_SET(m_socket, &fdread);
    if (uSec < 0 || sec < 0)
        ptm = NULL;
    else
        ptm = &tm;
    if ((ret = select(m_socket + 1, &fdread, NULL, NULL, ptm)) >= 0)
    {
        if (ret != 0 && FD_ISSET(m_socket, &fdread))
        {
            return UDPStatus::READ;
        }
        else // if timeout and ret == 0
        {
            return UDPStatus::SUCCESS;
        }
    }
    else
    {
        LOGMSG_ERR("errono: %s ret: %d\n", strerror(errno), ret);
        return UDPStatus::ERROR;
    }
}

UDPCast::UDPStatus UDPCast::Recv(std::string& fromAddress, short& fromPort, std::vector<char>& receiveBuffer, int& byteRecv)
{
    struct sockaddr_in remoteInfo;
    int infoLength = sizeof(remoteInfo);
    memset(&remoteInfo, 0, infoLength);
    byteRecv = recvfrom(m_socket, &receiveBuffer[0], receiveBuffer.size(), 0, (sockaddr*)&remoteInfo, (socklen_t*)&infoLength);
    if (byteRecv <= 0)
    {
        LOGMSG_ERR("errono: %s byteRecv: %d\n", strerror(errno), byteRecv);
        return UDPStatus::ERROR;
    }
    fromAddress = inet_ntoa(remoteInfo.sin_addr);
    fromPort = ntohs(remoteInfo.sin_port);
    return UDPStatus::SUCCESS;
}

