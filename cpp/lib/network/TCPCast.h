#ifndef TCPCAST_H
#define TCPCAST_H
#include <string>
#include <vector>

#include "DefaultMutex.h"

class TCPCast
{
 public:
    enum class TCPStatus {SUCCESS, ERROR, READ};
 public:
    TCPCast();
    virtual ~TCPCast();

    TCPStatus InitComponent(const std::string& ifAddress, const short ifPort, bool isClient, const int numClients = 5);

    // Client
    // Connect to TCP Server
    TCPStatus Connect(const std::string& toAddress, const short toPort);
    TCPStatus ClientSend(char const * const sendMsg, const int msgLength);
    TCPStatus ClientRecv(std::vector<char>& receiveBuffer, int& byteRecv);

    // Server
    // Wait for clients and return client handle
    int Accept();
    TCPStatus ServerSend(int clientHandle, char const * const sendMsg, const int msgLength);
    TCPStatus ServerRecv(int clientHandle, std::vector<char>& receiveBuffer, int& byteRecv);
 private:
    int m_socket;
    std::string m_ifAddress;
    short m_ifPort;
    bool m_isClient;
    int m_numClients;
    DefaultMutex m_sendLock;
 private:
    TCPStatus Start();
    void Stop();
 private:
};
#endif
