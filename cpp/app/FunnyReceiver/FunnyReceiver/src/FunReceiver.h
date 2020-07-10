#ifndef FUN_RECEIVER_H
#define FUN_RECEIVER_H
#include <string>
#include <mutex>
#include <queue>
#include <memory>
#include <thread>

class FunReceiver
{
 public:
    FunReceiver();
    ~FunReceiver();

    bool InitComponent(std::string tcpIP, short tcpPort, std::string udpIP, short udpPort, std::string udpClientIP, short udpClientPort, int maxMessageCount);
    int Start();
    int GetLatestCount();
 private:
    void TCPWorker();
    void UDPWorker();
    void PushAndPrint(const int& num, bool isTCP);
 private:
    // server config
    std::string m_tcpIP;
    short m_tcpPort;
    std::string m_udpIP;
    short m_udpPort;
    // client config
    std::string m_udpClientIP;
    short m_udpClientPort;

    int m_maxMessageCount;
    int m_latestCount;

    std::mutex m_mutex;
    std::queue<int> m_tcpQ;
    std::queue<int> m_udpQ;

    std::unique_ptr<std::thread> m_tcpTH;
    std::unique_ptr<std::thread> m_udpTH;
};

#endif
