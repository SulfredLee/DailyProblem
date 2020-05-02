#ifndef UDPCAST_H
#define UDPCAST_H
#include <string>
#include <vector>

#include "DefaultMutex.h"

class UDPCast
{
 public:
    enum class UDPStatus {SUCCESS, ERROR, READ};
 public:
    UDPCast();
    virtual ~UDPCast();

    UDPStatus InitComponent(const std::string& ifAddress, const short ifPort, bool isClient);
    // Set time to live
    UDPStatus SetTTL(int ttl);

    // Client, Server
    UDPStatus Send(std::string& toAddress, short& toPort, char const * const sendMsg, const int msgLength);
    UDPStatus SelectRead(long uSec=0, long sec=0);
    UDPStatus Recv(std::string& fromAddress, short& fromPort, std::vector<char>& receiveBuffer, int& byteRecv);
 private:
    int m_socket;
    std::string m_ifAddress;
    short m_ifPort;
    bool m_isClient;
    DefaultMutex m_sendLock;
 private:
    UDPStatus Start();
    void Stop();
 private:
};
#endif
