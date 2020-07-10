#include "FunServer.h"
#include "Logger.h"
#include <string.h>
#include <stdlib.h> // rand
#include <time.h>
#include "TCPCast.h"
#include "UDPCast.h"

FunServer::FunServer()
{
}

FunServer::~FunServer()
{
}

bool FunServer::InitComponent(std::string tcpIP, short tcpPort, std::string udpIP, short udpPort, int maxMessageCount)
{
    // handle TCP config
    m_tcpIP = tcpIP; m_tcpPort = tcpPort;
    // handle UDP config
    m_udpIP = udpIP; m_udpPort = udpPort;
    // other
    m_maxMessageCount = maxMessageCount;

    LOGMSG_MSG_S() << "TCP server IP: " << m_tcpIP << " Port: " << m_tcpPort << "\n";
    LOGMSG_MSG_S() << "UDP server IP: " << m_udpIP << " Port: " << m_udpPort << "\n";
    LOGMSG_MSG_S() << "maxMessageCount: " << m_maxMessageCount << "\n";

    return true;
}

int FunServer::Start()
{
    // Start TCP server
    m_tcpTH = std::make_unique<std::thread>(&FunServer::TCPWorker, this);
    m_tcpTH->detach();
    // Start UDP server
    m_udpTH = std::make_unique<std::thread>(&FunServer::UDPWorker, this);

    std::this_thread::sleep_for(std::chrono::milliseconds(500));
    LOGMSG_MSG("Server Started\n");

    return 0;
}

void FunServer::TCPWorker()
{
    LOGMSG_MSG("Start Thread\n");
    srand(time(NULL));

    std::vector<char> sendData;
    TCPCast tcpServer;
    if (tcpServer.InitComponent(m_tcpIP, m_tcpPort, false) == TCPCast::TCPStatus::SUCCESS)
    {
        int count = 0;
        sendData.resize(4);
        int clientHandle = tcpServer.Accept(); // waiting for client
        while (count < m_maxMessageCount)
        {
            // assign data
            memcpy(&sendData[0], &count, sizeof(int));
            // send to client
            TCPCast::TCPStatus retStatus = tcpServer.ServerSend(clientHandle, &sendData[0], sizeof(int));
            if (retStatus == TCPCast::TCPStatus::SUCCESS)
            {
                LOGMSG_MSG("Send success! count: %d\n", count);
            }
            else
            {
                LOGMSG_ERR("Send fail!\n");
            }
            count++;
            std::this_thread::sleep_for(std::chrono::milliseconds(rand() % 500 + 1)); // sleep with a rand duration
        }
    }
    else
    {
        LOGMSG_ERR("Cannot InitComponent\n");
    }
    LOGMSG_MSG("End Thread. TCP DONE\n");
}

void FunServer::UDPWorker()
{
    LOGMSG_MSG("Start Thread\n");
    std::vector<char> sendData;
    std::vector<char> recvData;
    UDPCast udpServer;
    if (udpServer.InitComponent(m_udpIP, m_udpPort, false) == UDPCast::UDPStatus::SUCCESS)
    {
        sendData.resize(4);
        recvData.resize(4);
        std::string clientAddress;
        short clientPort;
        int byteRecv = 0;
        UDPCast::UDPStatus retStatus = udpServer.Recv(clientAddress, clientPort, recvData, byteRecv); // wait for client
        if (retStatus == UDPCast::UDPStatus::SUCCESS && byteRecv > 0)
        {
            int countRecv = -1;
            memcpy(&countRecv, &recvData[0], sizeof(int));
            LOGMSG_MSG("Received client: %d byteRecv: %d\n", countRecv, byteRecv);
        }

        // send data to client
        int count = 0;
        while (count < m_maxMessageCount)
        {
            memcpy(&sendData[0], &count, sizeof(int));
            retStatus = udpServer.Send(clientAddress, clientPort, &sendData[0], sizeof(int));
            if (retStatus == UDPCast::UDPStatus::SUCCESS)
            {
                LOGMSG_MSG("Send success! count: %d\n", count);
            }
            else
            {
                LOGMSG_ERR("Send fail!\n");
            }
            count++;
            std::this_thread::sleep_for(std::chrono::milliseconds(rand() % 500 + 1)); // sleep with a rand duration
        }
    }
    else
    {
        LOGMSG_ERR("Cannot InitComponent\n");
    }
    LOGMSG_MSG("End Thread. UDP DONE\n");
}
