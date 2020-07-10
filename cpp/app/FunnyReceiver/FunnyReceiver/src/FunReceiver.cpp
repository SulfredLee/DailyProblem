#include "FunReceiver.h"
#include "TCPCast.h"
#include "UDPCast.h"
#include <string.h>
#include "Logger.h"

FunReceiver::FunReceiver()
{
    m_latestCount = 0;
}

FunReceiver::~FunReceiver()
{
}

bool FunReceiver::InitComponent(std::string tcpIP, short tcpPort, std::string udpIP, short udpPort, std::string udpClientIP, short udpClientPort, int maxMessageCount)
{
    // handle TCP config
    m_tcpIP = tcpIP; m_tcpPort = tcpPort;
    // handle UDP config
    m_udpIP = udpIP; m_udpPort = udpPort;
    m_udpClientIP = udpClientIP; m_udpClientPort = udpClientPort;

    m_maxMessageCount = maxMessageCount;

    LOGMSG_MSG("TCP server IP: %s Port: %d\n", m_tcpIP.c_str(), (int)m_tcpPort);
    LOGMSG_MSG("UDP server IP: %s Port: %d\n", m_udpIP.c_str(), (int)m_udpPort);
    LOGMSG_MSG("UDP client IP: %s Port: %d\n", m_udpClientIP.c_str(), (int)m_udpClientPort);
    LOGMSG_MSG("maxMessageCount: %d\n", m_maxMessageCount);

    return true;
}

int FunReceiver::Start()
{
    // start tcp receiver
    m_tcpTH = std::make_unique<std::thread>(&FunReceiver::TCPWorker, this);
    m_tcpTH->detach();
    // start udp receiver
    m_udpTH = std::make_unique<std::thread>(&FunReceiver::UDPWorker, this);
    m_udpTH->detach();

    std::this_thread::sleep_for(std::chrono::milliseconds(500));
    LOGMSG_MSG("Receiver Started\n");

    return 0;
}

int FunReceiver::GetLatestCount()
{
    std::lock_guard<std::mutex> lock(m_mutex);
    return m_latestCount;
}

void FunReceiver::TCPWorker()
{
    LOGMSG_MSG("Start Thread\n");
    std::vector<char> recvData;
    TCPCast tcpClient;
    if (tcpClient.InitComponent(m_tcpIP, 0, true) == TCPCast::TCPStatus::SUCCESS)
    {
        recvData.resize(4);
        if (tcpClient.Connect(m_tcpIP, m_tcpPort) == TCPCast::TCPStatus::SUCCESS)
        {
            while (true)
            {
                int byteRecv = 0;
                TCPCast::TCPStatus retStatus = tcpClient.ClientRecv(recvData, byteRecv);
                if (retStatus == TCPCast::TCPStatus::SUCCESS && byteRecv > 0)
                {
                    int countRecv;
                    memcpy(&countRecv, &recvData[0], sizeof(int));
                    PushAndPrint(countRecv, true);
                    LOGMSG_DBG("Received count: %d\n", countRecv);
                }
            }
        }
    }
    LOGMSG_MSG("End Thread\n");
}

void FunReceiver::UDPWorker()
{
    LOGMSG_MSG("Start Thread\n");
    std::vector<char> sendData;
    std::vector<char> recvData;
    UDPCast udpClient;

    if (udpClient.InitComponent(m_udpClientIP, m_udpClientPort, true) == UDPCast::UDPStatus::SUCCESS)
    {
        sendData.resize(4);
        recvData.resize(4);

        int clientID = 9394;
        memcpy(&sendData[0], &clientID, sizeof(int));
        UDPCast::UDPStatus retStatus = udpClient.Send(m_udpIP, m_udpPort, &sendData[0], sizeof(int));
        if (retStatus == UDPCast::UDPStatus::SUCCESS)
        {
            LOGMSG_MSG("Send success! clientID: %d\n", clientID);
        }
        else
        {
            LOGMSG_ERR("Send fail!\n");
        }

        while (true)
        {
            int byteRecv = 0;
            retStatus = udpClient.Recv(m_udpIP, m_udpPort, recvData, byteRecv);
            if (retStatus == UDPCast::UDPStatus::SUCCESS && byteRecv > 0)
            {
                int countRecv;
                memcpy(&countRecv, &recvData[0], sizeof(int));
                PushAndPrint(countRecv, false);
                LOGMSG_DBG("Received count: %d\n", countRecv);
            }
        }
    }
    else
    {
        LOGMSG_ERR("Cannot InitComponent\n");
    }
    LOGMSG_MSG("End Thread\n");
}

void FunReceiver::PushAndPrint(const int& num, bool isTCP)
{
    std::lock_guard<std::mutex> lock(m_mutex);
    if (isTCP)
        m_tcpQ.push(num);
    else
        m_udpQ.push(num);

    while (!m_tcpQ.empty() && !m_udpQ.empty() && m_tcpQ.front() == m_udpQ.front()) // only print when both sources are ready
    {
        LOGMSG_MSG("Received count: %d\n", m_tcpQ.front());
        m_tcpQ.pop();
        m_udpQ.pop();
        m_latestCount++;
    }
}
