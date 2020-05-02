#include <iostream>
#include <string.h>
#include <thread>
#include <chrono>

#include "TCPCast.h"
#include "Logger.h"

std::string serverIP = "192.168.1.208";
short serverPort = 7788;
void ServerWorker()
{
    std::vector<char> sendData;
    std::vector<char> recvData;
    TCPCast tcpServer;
    if (tcpServer.InitComponent(serverIP, serverPort, false) == TCPCast::TCPStatus::SUCCESS)
    {
        int count = 0;
        sendData.resize(4);
        recvData.resize(4);
        int clientHandle = tcpServer.Accept(); // waiting for client
        while (true)
        {
            memcpy(&sendData[0], &count, sizeof(int));
            TCPCast::TCPStatus retStatus = tcpServer.ServerSend(clientHandle, &sendData[0], sizeof(int));
            if (retStatus == TCPCast::TCPStatus::SUCCESS)
            {
                LOGMSG_MSG_C("Send success! count: %d\n", count);
            }
            else
            {
                LOGMSG_ERR_C("Send fail!\n");
            }
            count++;

            int byteRecv = 0;
            retStatus = tcpServer.ServerRecv(clientHandle, recvData, byteRecv);
            if (retStatus == TCPCast::TCPStatus::SUCCESS && byteRecv > 0)
            {
                int countRecv = -1;
                memcpy(&countRecv, &recvData[0], sizeof(int));
                LOGMSG_MSG_C("Received count: %d byteRecv: %d\n", countRecv, byteRecv);
            }
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
    TCPCast tcpClient;
    if (tcpClient.InitComponent(serverIP, 0, true) == TCPCast::TCPStatus::SUCCESS)
    {
        sendData.resize(4);
        recvData.resize(4);
        if (tcpClient.Connect(serverIP, serverPort) == TCPCast::TCPStatus::SUCCESS)
        {
            int count = 2000;
            while (true)
            {
                int byteRecv = 0;
                TCPCast::TCPStatus retStatus = tcpClient.ClientRecv(recvData, byteRecv);
                if (retStatus == TCPCast::TCPStatus::SUCCESS && byteRecv > 0)
                {
                    int countRecv;
                    memcpy(&countRecv, &recvData[0], sizeof(int));
                    LOGMSG_MSG_C("Received count: %d\n", countRecv);
                }

                memcpy(&sendData[0], &count, sizeof(int));
                retStatus = tcpClient.ClientSend(&sendData[0], sizeof(int));
                if (retStatus == TCPCast::TCPStatus::SUCCESS)
                {
                    LOGMSG_MSG_C("Send success! count: %d\n", count);
                }
                else
                {
                    LOGMSG_ERR_C("Send fail!\n");
                }
                count++;
                usleep(1000000); // 1 sec
            }
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

    std::this_thread::sleep_for(std::chrono::seconds(10));
    return 0;
}
