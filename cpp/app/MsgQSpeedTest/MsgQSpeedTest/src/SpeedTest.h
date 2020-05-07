#ifndef SPEED_TEST_H
#define SPEED_TEST_H
#include <string>
#include <atomic>
#include <memory>
#include <vector>

#include "DumpMsg.h"
#include "MsgQLockFree_Linux.h"
#include "MsgQLockFree_LinkList_Std.h"
// #include "MsgQLockFree_Complete_LinkList_Std.h"
#include "MsgStackLockFree_LinkList_Std.h"
#include "MsgQOneLock_RingBuf_Linux.h"
#include "MsgQTwoLock_RingBuf_Linux.h"
#include "MsgQOneLock_RingBuf_Std.h"
#include "MsgQTwoLock_RingBuf_Std.h"
#include "MsgQTwoLock_LinkList_Linux.h"
#include "MsgQOneLock_LinkList_Linux.h"
#include "MsgQTwoLock_LinkList_Std.h"
#include "MsgQOneLock_LinkList_Std.h"
#include "MsgQOneLock_Queue_Linux.h"
#include "MsgQOneLock_Queue_Std.h"
#include "CountTimer.h"
#include "LinuxCond.h"

class SpeedTest
{
 public:
    SpeedTest();
    ~SpeedTest();

    bool InitComponent(const std::string msgQName, int inThreadNum, int outThreadNum, int msgNumber);
    void RunTest();
    std::string GetResult();
    uint64_t GetResultTimeNSec();
    int GetCannotAddMsgCount();
 private:
    std::shared_ptr<MsgQBase<DumpMsg> > CreateMsgQ(const std::string msgQName);
    static void* StagingFunProxy(void* obj);
    void StagingFun();
    void PushingMsg();
    static void* GettingMsgProxy(void* obj);
    void GettingMsg();
    void WaitAllThreads();
 private:
    std::string m_msgQName;
    int m_inThreadNum;
    int m_outThreadNum;
    int m_msgNumberThread;
    int m_msgNumberTotal;
    std::atomic<bool> m_startTest;
    std::atomic<int> m_totalMsgGot;
    std::atomic<int> m_msgCannotAddCount;
    std::shared_ptr<MsgQBase<DumpMsg> > m_msgQ;
    std::vector<pthread_t> m_outThreads;
    std::vector<pthread_t> m_inThreads;
    CountTimer m_timer;
    LinuxCond m_cond;
};

#endif
