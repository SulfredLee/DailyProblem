#include <iostream>
#include <string.h>

#include "UDPCast.h"
#include "Logger.h"

std::string serverIP = "192.168.1.208";
std::string clientIP = "192.168.1.208";
short serverPort = 7788;
short clientPort = 8899;
void ServerWorker()
{
    std::vector<char> sendData;
    std::vector<char> recvData;
    UDPCast udpServer;
    if (udpServer.InitComponent(serverIP, serverPort, false) == UDPCast::UDPStatus::SUCCESS)
    {
        int count = 0;
        sendData.resize(4);
        recvData.resize(4);
        while (true)
        {
            std::string clientAddress;
            short clientPort;
            int byteRecv = 0;
            UDPCast::UDPStatus retStatus = udpServer.Recv(clientAddress, clientPort, recvData, byteRecv);
            if (retStatus == UDPCast::UDPStatus::SUCCESS && byteRecv > 0)
            {
                int countRecv = -1;
                memcpy(&countRecv, &recvData[0], sizeof(int));
                LOGMSG_MSG_C("Received count: %d byteRecv: %d\n", countRecv, byteRecv);
            }

            memcpy(&sendData[0], &count, sizeof(int));
            retStatus = udpServer.Send(clientAddress, clientPort, &sendData[0], sizeof(int));
            if (retStatus == UDPCast::UDPStatus::SUCCESS)
            {
                LOGMSG_MSG_C("Send success! count: %d\n", count);
            }
            else
            {
                LOGMSG_ERR_C("Send fail!\n");
            }
            count++;
        }
    }
    else
    {
        LOGMSG_ERR_C("Cannot InitComponent\n");
    }
}
void ClientWorker()
{
    std::vector<char> sendData;
    std::vector<char> recvData;
    UDPCast udpClient;

    if (udpClient.InitComponent(clientIP, clientPort, true) == UDPCast::UDPStatus::SUCCESS)
    {
        sendData.resize(4);
        recvData.resize(4);
        int count = 2000;
        while (true)
        {
            memcpy(&sendData[0], &count, sizeof(int));
            UDPCast::UDPStatus retStatus = udpClient.Send(serverIP, serverPort, &sendData[0], sizeof(int));
            if (retStatus == UDPCast::UDPStatus::SUCCESS)
            {
                LOGMSG_MSG_C("Send success! count: %d\n", count);
            }
            else
            {
                LOGMSG_ERR_C("Send fail!\n");
            }
            count++;

            int byteRecv = 0;
            retStatus = udpClient.Recv(serverIP, serverPort, recvData, byteRecv);
            if (retStatus == UDPCast::UDPStatus::SUCCESS && byteRecv > 0)
            {
                int countRecv;
                memcpy(&countRecv, &recvData[0], sizeof(int));
                LOGMSG_MSG_C("Received count: %d\n", countRecv);
            }
            usleep(1000000); // 1 sec
        }
    }
}
int main(int argc, char *argv[])
{
    std::thread serverTH(ServerWorker);
    serverTH.detach();
    std::this_thread::sleep_for(std::chrono::seconds(1));
    std::thread clientTH(ClientWorker);
    clientTH.detach();

    std::this_thread::sleep_for(std::chrono::seconds(5));
    return 0;
}
