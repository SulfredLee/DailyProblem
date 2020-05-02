#ifndef MCASTARBITRATOR_H
#define MCASTARBITRATOR_H
#include <string>
#include <atomic>
#include <thread>
#include <set>

#include "MultiCast.h"
#include "DefaultMutex.h"

#include <time.h>

#include <sys/time.h>
class MCastArbitrator
{
 public:
    enum class MCArbiStatus {SUCCESS, ERROR, READ, PRIMARY, SECONDARY, RAISEHAND};
 public:
    MCastArbitrator();
    ~MCastArbitrator();

    MCArbiStatus InitComponent(const std::string& ifAddress, const short ifPort, const short arbitratorID, const short instance);

    void JoinGroup(const std::string& address);
    void LeaveGroup(const std::string& address);

    MCArbiStatus Send(char const * const sendMsg, const int msgLength);
    void ChangeStatus(MCArbiStatus inStatus); // for testing
 private:
    std::string m_ifAddress;
    short m_ifPort;
    short m_arbitratorID;
    short m_instance;
    std::atomic<bool> m_runSend;
    std::atomic<bool> m_runReceive;
    std::thread m_sendThread;
    std::thread m_receiveThread;
    std::atomic<MCArbiStatus> m_status;
    std::atomic<MCArbiStatus> m_preStatus;
    Multicast m_ArbiSocSender;
    Multicast m_ArbiSocReceiver;
    Multicast m_NormalSoc;
    int m_dataFingerPrint;
    std::set<std::string> m_outputGroups;
    timeval m_latestTimeSeeFingerPrint;
    DefaultMutex m_sendLock;
 private:
    void SendArbitration();
    void ReceiveArbitration();
    void PrintStatus();
    std::string GetStatusString();
    bool IsLongTimeNoUpdate();
    void SwitchStatus_LongTimeNoUpdate();
    MCArbiStatus ConvertStatus(Multicast::MCStatus inStatus);
};
#endif
