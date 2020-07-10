#ifndef FUN_SERVER_H
#define FUN_SERVER_H
#include <string>
#include <thread>
#include <chrono>
#include <memory>


class FunServer
{
 public:
    FunServer();
    ~FunServer();

    bool InitComponent(std::string tcpIP, short tcpPort, std::string udpIP, short udpPort, int maxMessageCount);
    int Start();
 private:
    void TCPWorker();
    void UDPWorker();
 private:
    std::string m_tcpIP;
    short m_tcpPort;
    std::string m_udpIP;
    short m_udpPort;
    int m_maxMessageCount;

    std::unique_ptr<std::thread> m_tcpTH;
    std::unique_ptr<std::thread> m_udpTH;
};

#endif
