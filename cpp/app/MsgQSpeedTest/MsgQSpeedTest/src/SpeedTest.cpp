#include <thread>

#include "SpeedTest.h"
#include "Logger.h"

SpeedTest::SpeedTest()
{
    LOGMSG_CLASS_NAME("SpeedTest");
    m_startTest = false;
}

SpeedTest::~SpeedTest()
{
}

bool SpeedTest::InitComponent(const std::string msgQName, int inThreadNum, int outThreadNum, int msgNumber)
{
    m_msgQName = msgQName;
    m_msgQ = CreateMsgQ(m_msgQName);
    m_inThreadNum = inThreadNum;
    m_outThreadNum = outThreadNum;
    m_msgNumberThread = msgNumber / m_inThreadNum;
    m_msgNumberTotal = msgNumber;
    m_totalMsgGot = 0;
    m_msgCannotAddCount = 0;

    // prepare get threads
    for (int i = 0; i < outThreadNum; i++)
    {
        pthread_t thread;
        m_outThreads.push_back(thread);
        pthread_create(&m_outThreads.back(), NULL, SpeedTest::GettingMsgProxy, (void*)this);
    }
    // prepare push threads
    for (int i = 0; i < inThreadNum; i++)
    {
        pthread_t thread;
        m_inThreads.push_back(thread);
        pthread_create(&m_inThreads.back(), NULL, SpeedTest::StagingFunProxy, (void*)this);
    }
    std::this_thread::sleep_for(std::chrono::milliseconds(1000));
    return true;
}

void SpeedTest::RunTest()
{
    // start timer
    m_timer.Start();
    // start test
    m_startTest = true;
    while (m_cond.WaitWithTime(5 * 1000) == ETIMEDOUT) // wait 5 second
    {
        LOGMSG_MSG("MsgQ has: %d\n", m_msgQ->GetMsgNum());
        int totalMsgGot = m_totalMsgGot;
        LOGMSG_MSG("total got message: %d\n", totalMsgGot);
    }
    WaitAllThreads();
}

std::string SpeedTest::GetResult()
{
    std::stringstream ss;
    ss << "MsQName: " << m_msgQName
       << " ThreadIN: " << m_inThreadNum
       << " ThreadOUT: " << m_outThreadNum
       << " MsgNumber: " << m_msgNumberTotal
       << " Used Time (sec): " << m_timer.GetSecond()
       << " Used Time (msec): " << m_timer.GetMSecond()
       << " Used Time (nsec): " << m_timer.GetNSecond()
       << " Cannot add msg count: " << m_msgCannotAddCount;
    return ss.str();
}

int SpeedTest::GetCannotAddMsgCount()
{
    return m_msgCannotAddCount.load();
}

uint64_t SpeedTest::GetResultTimeNSec()
{
    return m_timer.GetNSecond();
}

std::shared_ptr<MsgQBase<DumpMsg> > SpeedTest::CreateMsgQ(const std::string msgQName)
{
    if (msgQName == "MsgQLockFree_Linux")
        return std::make_shared<MsgQLockFree_Linux<DumpMsg> >();
    else if (msgQName == "MsgQLockFree_LinkList_Std")
        return std::make_shared<MsgQLockFree_LinkList_Std<DumpMsg> >();
    // else if (msgQName == "MsgQLockFree_Complete_LinkList_Std")
    //     return std::make_shared<MsgQLockFree_Complete_LinkList_Std<DumpMsg> >();
    else if (msgQName == "MsgStackLockFree_LinkList_Std")
        return std::make_shared<MsgStackLockFree_LinkList_Std<DumpMsg> >();
    else if (msgQName == "MsgQOneLock_RingBuf_Linux")
        return std::make_shared<MsgQOneLock_RingBuf_Linux<DumpMsg> >();
    else if (msgQName == "MsgQTwoLock_RingBuf_Linux")
        return std::make_shared<MsgQTwoLock_RingBuf_Linux<DumpMsg> >();
    else if (msgQName == "MsgQOneLock_RingBuf_Std")
        return std::make_shared<MsgQOneLock_RingBuf_Std<DumpMsg> >();
    else if (msgQName == "MsgQTwoLock_RingBuf_Std")
        return std::make_shared<MsgQTwoLock_RingBuf_Std<DumpMsg> >();
    else if (msgQName == "MsgQOneLock_LinkList_Linux")
        return std::make_shared<MsgQOneLock_LinkList_Linux<DumpMsg> >();
    else if (msgQName == "MsgQTwoLock_LinkList_Linux")
        return std::make_shared<MsgQTwoLock_LinkList_Linux<DumpMsg> >();
    else if (msgQName == "MsgQOneLock_LinkList_Std")
        return std::make_shared<MsgQOneLock_LinkList_Std<DumpMsg> >();
    else if (msgQName == "MsgQTwoLock_LinkList_Std")
        return std::make_shared<MsgQTwoLock_LinkList_Std<DumpMsg> >();
    else if (msgQName == "MsgQOneLock_Queue_Linux")
        return std::make_shared<MsgQOneLock_Queue_Linux<DumpMsg> >();
    else if (msgQName == "MsgQOneLock_Queue_Std")
        return std::make_shared<MsgQOneLock_Queue_Std<DumpMsg> >();
    else
        return std::make_shared<MsgQLockFree_Linux<DumpMsg> >();
}

void* SpeedTest::StagingFunProxy(void* obj)
{
    if (obj)
    {
        SpeedTest* objReal = (SpeedTest*)(obj);
        objReal->StagingFun();
    }
    return NULL;
}

void SpeedTest::StagingFun()
{
    while (!m_startTest)
    {
        std::this_thread::sleep_for(std::chrono::milliseconds(5));
    }

    PushingMsg();
}

void SpeedTest::PushingMsg()
{
    // LOGMSG_MSG("Thread Start\n");
    for (int i = 0; i < m_msgNumberThread; i++)
    {
        std::shared_ptr<DumpMsg> msg = std::make_shared<DumpMsg>();
        if (msg.get() == nullptr)
            LOGMSG_MSG("sulfred debug found nullptr\n");
        while (!m_msgQ->AddMsg(msg))
        {
            m_msgCannotAddCount += 1;
            std::this_thread::sleep_for(std::chrono::milliseconds(1));
            // LOGMSG_MSG("Cannot add to msgQ\n");
        }
    }
    // LOGMSG_MSG("Thread End\n");
}

void* SpeedTest::GettingMsgProxy(void* obj)
{
    if (obj)
    {
        SpeedTest* objReal = (SpeedTest*)(obj);
        objReal->GettingMsg();
    }
    return NULL;
}

void SpeedTest::GettingMsg()
{
    // LOGMSG_MSG("Thread Start\n");
    bool keepRunning = true;
    std::shared_ptr<DumpMsg> msg;
    while (keepRunning)
    {
        m_msgQ->GetMsg(msg);
        // debug
        if (msg.get() == nullptr)
            continue;
        if (!keepRunning)
            return;
        m_totalMsgGot++;
        if (m_totalMsgGot >= m_msgNumberTotal)
            keepRunning = false;
    }
    // stop timer
    m_timer.Stop();
    {
        // remove all getting threads
        for (int i = 0; i < 100; i++)
        {
            std::shared_ptr<DumpMsg> msg = std::make_shared<DumpMsg>();
            m_msgQ->AddMsg(msg);
        }
    }
    // LOGMSG_MSG_S() << "Send Signal m_totalMsgGot: " << m_totalMsgGot << " m_msgNumberTotal: " << m_msgNumberTotal << "\n";
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    m_cond.Signal();
    // LOGMSG_MSG("Thread End\n");
}

void SpeedTest::WaitAllThreads()
{
    for (size_t i = 0; i < m_outThreads.size(); i++)
    {
        pthread_join(m_outThreads[i], NULL);
    }
}
