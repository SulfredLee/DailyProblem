#ifndef MULTICAST_H
#define MULTICAST_H
#include <string>
#include <vector>

#include "DefaultMutex.h"

class Multicast
{
 public:
    enum class MCStatus {SUCCESS, ERROR, READ};
 public:
    Multicast();
    virtual ~Multicast();

    MCStatus InitComponent(const std::string& ifAddress, const short ifPort);
    // Set time to live
    MCStatus SetTTL(int ttl);

    // Client
    // Join the multicast group to receive datagrams.
    MCStatus JoinGroup(const std::string& grpAddress);
    // Leave the multicast group
    MCStatus LeaveGroup(const std::string& grpAddress);
    // Receive data from the multicasting group server.
    MCStatus SelectRead(long uSec=0, long sec=0);
    MCStatus Recv(std::vector<char>& receiveBuffer, std::string& fromAddress, short& fromPort, int& byteRecv);

    // Server
    // Send a message to the multicasting address with specified port.
    MCStatus Send(const std::string& toAddress, char const * const sendMsg, const int msgLength);
 private:
    int m_socket;
    std::string m_ifAddress;
    short m_ifPort;
    bool m_isClient;
    DefaultMutex m_sendLock;
 private:
    MCStatus Start();
    void Stop();
};

#endif
