#include <iostream>
#include <string.h>
#include <thread>
#include <chrono>

#include "MultiCast.h"
#include "Logger.h"

std::string MCastAddress = "225.1.32.28";
short MCastPort = 6000;
std::string SenderIP = "192.168.1.208";
std::string ReceiverIP = "";
void MCastSender()
{
    std::vector<char> sendData;
    Multicast MCast;

    if (MCast.InitComponent(SenderIP, MCastPort) == Multicast::MCStatus::SUCCESS)
    {
        sendData.resize(4);
        int count = 0;
        while(true)
        {
            memcpy(&sendData[0], &count, sizeof(int));
            Multicast::MCStatus retStatus = MCast.Send(MCastAddress, &sendData[0], sizeof(int));
            if (retStatus == Multicast::MCStatus::SUCCESS)
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
void MCastReceiver()
{
    std::vector<char> receivedData;
    std::string fromAddress;
    short fromPort;
    int byteRecv;
    Multicast MCast;

    if (MCast.InitComponent(ReceiverIP, MCastPort) == Multicast::MCStatus::SUCCESS)
    {
        MCast.JoinGroup(MCastAddress);

        receivedData.resize(1024);
        while(true)
        {
            if (MCast.SelectRead(500, 0) == Multicast::MCStatus::READ) // wait for 500 microsecond
            {
                if (MCast.Recv(receivedData, fromAddress, fromPort, byteRecv) == Multicast::MCStatus::SUCCESS)
                {
                    int count;
                    memcpy(&count, &receivedData[0], sizeof(int));
                    LOGMSG_MSG_C("Received from %s:%u count: %d\n", fromAddress.c_str(), fromPort, count);
                }
            }
        }
    }
}
int main(int argc, char *argv[])
{
    std::thread senderTH(MCastSender);
    senderTH.detach();
    std::this_thread::sleep_for(std::chrono::seconds(1));
    std::thread receiverTH(MCastReceiver);
    receiverTH.detach();

    std::this_thread::sleep_for(std::chrono::seconds(5));
    return 0;
}
