#include "MCastArbitrator.h"
#include "Logger.h"

#include <unistd.h>
#include <string.h>

#define ARBIGROUP "225.1.20.159"
#define ARBIFINGERPRINT 0xFFEE00EF

MCastArbitrator::MCastArbitrator()
{
    m_runSend = false;
    m_runReceive = false;
}

MCastArbitrator::~MCastArbitrator()
{
    bool isNeedJoin = m_runSend;
    m_runSend = false;
    if (isNeedJoin)
    {
        m_sendThread.join();
    }

    isNeedJoin = m_runReceive;
    m_runReceive = false;
    if (isNeedJoin)
    {
        m_receiveThread.join();
    }

    m_ArbiSocSender.LeaveGroup(ARBIGROUP);
    m_ArbiSocReceiver.LeaveGroup(ARBIGROUP);
}

MCastArbitrator::MCArbiStatus MCastArbitrator::InitComponent(const std::string& ifAddress, const short ifPort, const short arbitratorID, const short instance)
{
    m_ifAddress = ifAddress;
    m_ifPort = ifPort;
    m_arbitratorID = arbitratorID;
    m_instance = instance;
    m_status = MCArbiStatus::SECONDARY;
    m_dataFingerPrint = ARBIFINGERPRINT;
    gettimeofday(&m_latestTimeSeeFingerPrint, NULL);

    if (m_ArbiSocSender.InitComponent(m_ifAddress, m_ifPort) != Multicast::MCStatus::SUCCESS)
    {
        return MCArbiStatus::ERROR;
    }
    m_ArbiSocSender.JoinGroup(ARBIGROUP);
    if (m_ArbiSocReceiver.InitComponent("", m_ifPort) != Multicast::MCStatus::SUCCESS)
    {
        return MCArbiStatus::ERROR;
    }
    m_ArbiSocReceiver.JoinGroup(ARBIGROUP);
    if (m_NormalSoc.InitComponent(m_ifAddress, m_ifPort) != Multicast::MCStatus::SUCCESS)
    {
        return MCArbiStatus::ERROR;
    }

    m_runSend = true;
    m_runReceive = true;
    m_sendThread = std::thread(&MCastArbitrator::SendArbitration, this);
    m_receiveThread = std::thread(&MCastArbitrator::ReceiveArbitration, this);
    return MCArbiStatus::SUCCESS;
}

void MCastArbitrator::SendArbitration()
{
    LOGMSG_MSG("Start thread\n");
    // set fingerprint
    std::vector<char> fingerPrintData;
    int totalLen = sizeof(int) + sizeof(short) * 2;
    fingerPrintData.resize(totalLen);
    int offSet = 0;
    memcpy(&fingerPrintData[offSet], &m_dataFingerPrint, sizeof(int));
    offSet += sizeof(int);
    memcpy(&fingerPrintData[offSet], &m_arbitratorID, sizeof(short));
    offSet += sizeof(short);
    memcpy(&fingerPrintData[offSet], &m_instance, sizeof(short));

    while(m_runSend)
    {
        switch(m_status)
        {
            case MCArbiStatus::PRIMARY:
            case MCArbiStatus::RAISEHAND:
                m_ArbiSocSender.Send(ARBIGROUP, &fingerPrintData[0], totalLen);
                break;
            case MCArbiStatus::SECONDARY:
            default:
                break;
        }
        usleep(250000); // wait for 250 milliseconds
    }
    LOGMSG_MSG("End thread\n");
}

void MCastArbitrator::ReceiveArbitration()
{
    std::vector<char> receivedData(1024);
    std::string fromAddress;
    short fromPort;
    int byteRecv;

    LOGMSG_MSG("Start thread\n");
    while(m_runReceive)
    {
        if (m_ArbiSocReceiver.SelectRead(500000, 0) == Multicast::MCStatus::READ) // wait for 500 milliseconds
        {
            if (m_ArbiSocReceiver.Recv(receivedData, fromAddress, fromPort, byteRecv) == Multicast::MCStatus::SUCCESS)
            {
                int dataType;
                short arbitratorID;
                short instance;
                int offSet = 0;
                if (byteRecv >= 8)
                {
                    memcpy(&dataType, &receivedData[offSet], sizeof(int));
                    offSet += sizeof(int);
                    memcpy(&arbitratorID, &receivedData[offSet], sizeof(short));
                    offSet += sizeof(short);
                    memcpy(&instance, &receivedData[offSet], sizeof(short));

                    if (dataType == m_dataFingerPrint)
                    {
                        if (arbitratorID == m_arbitratorID && instance == m_instance) // get self instance
                        {
                            if (m_status == MCArbiStatus::RAISEHAND)
                            {
                                m_status = MCArbiStatus::PRIMARY;
                            }
                        }
                        else // get other instance
                        {
                            m_status = MCArbiStatus::SECONDARY;
                        }
                        gettimeofday(&m_latestTimeSeeFingerPrint, NULL);
                    }
                }
                else // get irrelevent data
                {
                    if (IsLongTimeNoUpdate())
                    {
                        SwitchStatus_LongTimeNoUpdate();
                    }
                }
            }
        }
        else
        {
            SwitchStatus_LongTimeNoUpdate();
        }
        PrintStatus();
    }
    LOGMSG_MSG("End thread\n");
}

void MCastArbitrator::JoinGroup(const std::string& address)
{
    m_outputGroups.insert(address);
}

void MCastArbitrator::LeaveGroup(const std::string& address)
{
    m_outputGroups.erase(address);
}

void MCastArbitrator::PrintStatus()
{
    if (m_preStatus.load() != m_status.load())
    {
        m_preStatus = m_status.load();
        LOGMSG_MSG("Status updated %s\n", GetStatusString().c_str());
    }
}

std::string MCastArbitrator::GetStatusString()
{
    std::string status = "";
    switch(m_status)
    {
        case MCArbiStatus::PRIMARY:
            status = "Primary";
            break;
        case MCArbiStatus::RAISEHAND:
            status = "Raise hand";
            break;
        case MCArbiStatus::SECONDARY:
            status = "Secondary";
            break;
        default:
            status = "Unknown";
            break;
    }
    return status;
}

bool MCastArbitrator::IsLongTimeNoUpdate()
{
    timeval curTime;
    gettimeofday(&curTime, NULL);
    timeval diff;
    timersub(&curTime, &m_latestTimeSeeFingerPrint, &diff);
    int timeDiff = diff.tv_sec * 1000 + diff.tv_usec / 1000; // in milliseconds
    return timeDiff >= 500 ? true : false;
}

void MCastArbitrator::SwitchStatus_LongTimeNoUpdate()
{
    LOGMSG_MSG("IN\n");
    switch(m_status)
    {
        case MCArbiStatus::PRIMARY:
        case MCArbiStatus::RAISEHAND:
            m_status = MCArbiStatus::SECONDARY;
            break;
        case MCArbiStatus::SECONDARY:
            m_status = MCArbiStatus::RAISEHAND;
            break;
        default:
            break;
    }
}

MCastArbitrator::MCArbiStatus MCastArbitrator::Send(char const * const sendMsg, const int msgLength)
{
    MCArbiStatus ret = MCArbiStatus::ERROR;
    if (m_status == MCArbiStatus::PRIMARY)
    {
        DefaultLock lock(m_sendLock);
        for (auto it = m_outputGroups.begin(); it != m_outputGroups.end(); it++)
        {
            ret = ConvertStatus(m_NormalSoc.Send(*it, sendMsg, msgLength));
            if (ret != MCArbiStatus::SUCCESS)
            {
                return ret;
            }
        }
    }
    else
    {
        ret = MCArbiStatus::SECONDARY;
    }
    return ret;
}

void MCastArbitrator::ChangeStatus(MCastArbitrator::MCArbiStatus inStatus)
{
    m_preStatus = m_status.load();
    m_status = inStatus;
}

MCastArbitrator::MCArbiStatus MCastArbitrator::ConvertStatus(Multicast::MCStatus inStatus)
{
    switch(inStatus)
    {
        case Multicast::MCStatus::READ:
            return MCArbiStatus::READ;
            break;
        case Multicast::MCStatus::ERROR:
            return MCArbiStatus::ERROR;
            break;
        case Multicast::MCStatus::SUCCESS:
            return MCArbiStatus::SUCCESS;
            break;
        default:
            return MCArbiStatus::ERROR;
            break;
    }
}
