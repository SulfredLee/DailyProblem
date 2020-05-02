#include "TCPCast.h"
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

TCPCast::TCPCast()
{
}

TCPCast::~TCPCast()
{
    Stop();
}

TCPCast::TCPStatus TCPCast::InitComponent(const std::string& ifAddress, const short ifPort, bool isClient, const int numClients)
{
    m_ifAddress = ifAddress;
    m_isClient = isClient;
    if (m_isClient)
    {
        m_ifPort = 0;
        m_numClients = 0;
    }
    else
    {
        m_ifPort = ifPort;
        m_numClients = numClients;
    }
    return Start();
}

TCPCast::TCPStatus TCPCast::Start()
{
    // create TCP socket
    if ((m_socket = socket(AF_INET, SOCK_STREAM, IPPROTO_IP)) < 0)
    {
        LOGMSG_ERR("errono: %s\n", strerror(errno));
        return TCPStatus::ERROR;
    }
    // set address and port for local address
    struct sockaddr_in local_addr;
    local_addr.sin_family = AF_INET;
    local_addr.sin_port = htons(m_ifPort);
    local_addr.sin_addr.s_addr = m_ifAddress == "" ? htonl(INADDR_ANY) : inet_addr(m_ifAddress.c_str());
    if (!m_isClient) // do binding if the socket need to listen incoming message
    {
        // bind local address
        if (bind(m_socket, (struct sockaddr *)&local_addr, sizeof(local_addr)) < 0)
        {
            LOGMSG_ERR("errono: %s\n", strerror(errno));
            return TCPStatus::ERROR;
        }
        // get ready the server
        listen(m_socket, m_numClients);
    }
    // set receive buffer size
    int recevBufSize = 1024 * 256; // 256 kByte
    setsockopt(m_socket, SOL_SOCKET, SO_RCVBUF, (char *)&recevBufSize, sizeof(recevBufSize));
    return TCPStatus::SUCCESS;
}

void TCPCast::Stop()
{
    shutdown(m_socket, 0x00);
}

TCPCast::TCPStatus TCPCast::Connect(const std::string& toAddress, const short toPort)
{
    struct sockaddr_in toInfo;
    memset(&toInfo, 0, sizeof(sockaddr_in));
    toInfo.sin_family = PF_INET;
    toInfo.sin_addr.s_addr = inet_addr(toAddress.c_str());
    toInfo.sin_port = htons(toPort);

    int err = connect(m_socket, (struct sockaddr*)&toInfo, sizeof(sockaddr_in));
    if (err == -1)
    {
        LOGMSG_ERR("errono: %s\n", strerror(errno));
        return TCPStatus::ERROR;
    }
    return TCPStatus::SUCCESS;
}

TCPCast::TCPStatus TCPCast::ClientSend(char const * const sendMsg, const int msgLength)
{
    if (send(m_socket, sendMsg, msgLength, 0) != msgLength)
    {
        LOGMSG_ERR("errono: %s\n", strerror(errno));
        return TCPStatus::ERROR;
    }
    return TCPStatus::SUCCESS;
}

TCPCast::TCPStatus TCPCast::ClientRecv(std::vector<char>& receiveBuffer, int& byteRecv)
{
    if ((byteRecv = recv(m_socket, &receiveBuffer[0], receiveBuffer.size(), MSG_WAITALL)) < 0)
    {
        LOGMSG_ERR("errono: %s\n", strerror(errno));
        return TCPStatus::ERROR;
    }
    return TCPStatus::SUCCESS;
}

int TCPCast::Accept()
{
    struct sockaddr_in clientInfo;
    int infoLength = sizeof(clientInfo);
    memset(&clientInfo, 0, infoLength);
    int clientHandle = accept(m_socket, (struct sockaddr*)&clientInfo, (socklen_t*)&infoLength);

    LOGMSG_MSG("Received client %s:%d\n", inet_ntoa(clientInfo.sin_addr), (int)ntohs(clientInfo.sin_port));
    return clientHandle;
}

TCPCast::TCPStatus TCPCast::ServerSend(int clientHandle, char const * const sendMsg, const int msgLength)
{
    DefaultLock lock(m_sendLock);

    if (send(clientHandle, sendMsg, msgLength, 0) != msgLength)
    {
        LOGMSG_ERR("errono: %s\n", strerror(errno));
        return TCPStatus::ERROR;
    }
    return TCPStatus::SUCCESS;
}

TCPCast::TCPStatus TCPCast::ServerRecv(int clientHandle, std::vector<char>& receiveBuffer, int& byteRecv)
{
    if ((byteRecv = recv(clientHandle, &receiveBuffer[0], receiveBuffer.size(), MSG_WAITALL)) < 0)
    {
        LOGMSG_ERR("errono: %s\n", strerror(errno));
        return TCPStatus::ERROR;
    }
    return TCPStatus::SUCCESS;
}
