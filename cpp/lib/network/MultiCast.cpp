#include <iostream>

#include <sys/socket.h>
#include <errno.h>
#include <string.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#include <iostream>

#include "MultiCast.h"
#include "Logger.h"

Multicast::Multicast()
{
}

Multicast::~Multicast()
{
    Stop();
}

Multicast::MCStatus Multicast::InitComponent(const std::string& ifAddress, const short ifPort)
{
    m_ifAddress = ifAddress;
    m_ifPort = ifPort;
    return Start();
}

Multicast::MCStatus Multicast::Start()
{
    // create UDP socket
    if ((m_socket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)) < 0)
    {
        LOGMSG_ERR("errono: %s\n", strerror(errno));
        return MCStatus::ERROR;
    }
    // set address and port for local address
    struct sockaddr_in local_addr;
    local_addr.sin_family = AF_INET;
    local_addr.sin_port = htons(m_ifPort);
    local_addr.sin_addr.s_addr = m_ifAddress == "" ? htonl(INADDR_ANY) : inet_addr(m_ifAddress.c_str());
    setsockopt(m_socket, IPPROTO_IP, IP_MULTICAST_IF, (char *)&local_addr.sin_addr.s_addr, sizeof(local_addr.sin_addr.s_addr));
    // allow multiple sockets to use the same PORT number
    u_int yes=1;
    if (setsockopt(m_socket, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(yes)) < 0)
    {
        LOGMSG_ERR("errono: %s\n", strerror(errno));
        return MCStatus::ERROR;
    }
    // bind local address
    if (bind(m_socket, (struct sockaddr *)&local_addr, sizeof(local_addr)) < 0)
    {
        LOGMSG_ERR("errono: %s\n", strerror(errno));
        return MCStatus::ERROR;
    }
    // set receive buffer size
    int recevBufSize = 1024 * 256; // 256 kByte
    setsockopt(m_socket, SOL_SOCKET, SO_RCVBUF, (char *)&recevBufSize, sizeof(recevBufSize));

    SetTTL(35);
    return MCStatus::SUCCESS;
}

void Multicast::Stop()
{
    shutdown(m_socket, 0x00);
}

Multicast::MCStatus Multicast::JoinGroup(const std::string& grpAddress)
{
    if (grpAddress == "")
    {
        return MCStatus::SUCCESS;
    }

    struct ip_mreq mreq;
    mreq.imr_multiaddr.s_addr=inet_addr(grpAddress.c_str());
    if (m_ifAddress == "")
    {
        mreq.imr_interface.s_addr=htonl(INADDR_ANY);
    }
    else
    {
        mreq.imr_interface.s_addr=inet_addr(m_ifAddress.c_str());
    }
    if (setsockopt(m_socket, IPPROTO_IP, IP_ADD_MEMBERSHIP, &mreq, sizeof(mreq)) < 0)
    {
        LOGMSG_ERR("errono: %s\n", strerror(errno));
        return MCStatus::ERROR;
    }
    return MCStatus::SUCCESS;
}

Multicast::MCStatus Multicast::LeaveGroup(const std::string& grpAddress)
{
    if (grpAddress == "")
    {
        return MCStatus::SUCCESS;
    }

    struct ip_mreq mreq;
    mreq.imr_multiaddr.s_addr = inet_addr(grpAddress.c_str());
    mreq.imr_interface.s_addr = inet_addr(grpAddress.c_str());
    if (setsockopt(m_socket, IPPROTO_IP, IP_DROP_MEMBERSHIP, (char *)&mreq, sizeof(mreq)) == -1)
    {
        LOGMSG_ERR("errono: %s\n", strerror(errno));
        return MCStatus::ERROR;
    }
    return MCStatus::SUCCESS;
}

Multicast::MCStatus Multicast::SelectRead(long usec, long sec)
{
    fd_set fdread;
    int ret;

    struct timeval tm, *ptm;
    tm.tv_sec = sec;
    tm.tv_usec = usec;
    FD_ZERO(&fdread);
    FD_SET(m_socket, &fdread);
    if (usec < 0 || sec < 0)
        ptm = NULL;
    else
        ptm = &tm;
    if ((ret = select(m_socket + 1, &fdread, NULL, NULL, ptm)) >= 0)
    {
        if (ret != 0 && FD_ISSET(m_socket, &fdread))
        {
            return MCStatus::READ;
        }
        else // if timeout and ret == 0
        {
            return MCStatus::SUCCESS;
        }
    }
    else
    {
        LOGMSG_ERR("errono: %s ret: %d\n", strerror(errno), ret);
        return MCStatus::ERROR;
    }
}

Multicast::MCStatus Multicast::Recv(std::vector<char>& receiveBuffer, std::string& fromAddress, short& fromPort, int& byteRecv)
{
    struct sockaddr_in remoteInfo;
    int infoLength = sizeof(remoteInfo);
    memset(&remoteInfo, 0, infoLength);
    byteRecv = recvfrom(m_socket, &receiveBuffer[0], receiveBuffer.size(), 0, (sockaddr*)&remoteInfo, (socklen_t*)&infoLength);
    if (byteRecv <= 0)
    {
        LOGMSG_ERR("errono: %s byteRecv: %d\n", strerror(errno), byteRecv);
        return MCStatus::ERROR;
    }
    fromAddress = inet_ntoa(remoteInfo.sin_addr);
    fromPort = ntohs(remoteInfo.sin_port);

    return MCStatus::SUCCESS;
}

Multicast::MCStatus Multicast::SetTTL(int ttl)
{
    if (setsockopt(m_socket, IPPROTO_IP, IP_MULTICAST_TTL, (char *)&ttl, sizeof(ttl)) < 0)
    {
        LOGMSG_ERR("errono: %s ttl: %d\n", strerror(errno), ttl);
        return MCStatus::ERROR;
    }
    return MCStatus::SUCCESS;
}

Multicast::MCStatus Multicast::Send(const std::string& toAddress, char const * const sendMsg, const int msgLength)
{
    struct sockaddr_in group_addr;

    group_addr.sin_family = AF_INET;
    group_addr.sin_addr.s_addr = inet_addr(toAddress.c_str());
    group_addr.sin_port = htons(m_ifPort);

    DefaultLock lock(m_sendLock);

    if (sendto(m_socket, sendMsg, msgLength, 0, (sockaddr*)&group_addr, sizeof(group_addr)) != msgLength)
    {
        LOGMSG_ERR("errono: %s\n", strerror(errno));
        return MCStatus::ERROR;
    }
    return MCStatus::SUCCESS;
}
