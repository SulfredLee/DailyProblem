#include <iostream>
#include <string.h>
#include <thread>
#include <chrono>
#include <atomic>

#include "MCastArbitrator.h"
#include "Logger.h"
#include "LinuxThread.h"

// usgae: ./MCastArbitrator

std::string MCastAddress = "225.1.32.28";
short MCastPort = 6000;
std::string SenderIP = "192.168.1.208";
class Sender : public LinuxThread
{
public:
    Sender() { m_running = true; }
    ~Sender() { stopThread(); m_running = false; joinThread(); }

    bool InitComponent(int instance) { m_instance = instance; startThread(); return true; }
    void ChangeStatusForTest() { MCArbi.ChangeStatus(MCastArbitrator::MCArbiStatus::SECONDARY); }
private:
    // override
    void *Main()
    {
        std::vector<char> sendData;

        if (MCArbi.InitComponent(SenderIP, MCastPort, 32, m_instance) == MCastArbitrator::MCArbiStatus::SUCCESS)
        {
            MCArbi.JoinGroup(MCastAddress);
            sendData.resize(4);
            int count = 0;
            while(m_running.load())
            {
                memcpy(&sendData[0], &count, sizeof(int));
                MCastArbitrator::MCArbiStatus retStatus = MCArbi.Send(&sendData[0], sizeof(int));
                if (retStatus == MCastArbitrator::MCArbiStatus::SUCCESS)
                {
                    LOGMSG_MSG("Send success! count: %d instance: %d\n", count, m_instance);
                }
                else
                {
                    // LOGMSG_ERR("Send fail! instance: %d\n", m_instance);
                }
                count++;
                usleep(1000000); // 1 sec
            }
        }
        return NULL;
    }
public:
    int m_instance;
private:
    std::atomic<bool> m_running;
    MCastArbitrator MCArbi;
};
int main(int argc, char *argv[])
{
    Sender *sender001 = new Sender(); sender001->InitComponent(1);
    std::this_thread::sleep_for(std::chrono::seconds(1));
    Sender *sender002 = new Sender(); sender002->InitComponent(2);

    int count = 1;
    int lastDie = 2;
    while (true)
    {
        if (count % 5 == 0)
        {
            if (lastDie == 2)
            {
                sender001->ChangeStatusForTest();
                lastDie = 1;
            }
            else
            {
                sender002->ChangeStatusForTest();
                lastDie = 2;
            }
            count = 0;
        }
        count++;
        std::this_thread::sleep_for(std::chrono::seconds(1));
    }
    return 0;
}
