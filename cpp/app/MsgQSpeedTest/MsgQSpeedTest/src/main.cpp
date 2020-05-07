#include <iostream>
#include <vector>
#include <string>
#include <math.h>
#include <memory>
#include <atomic>

#include "SpeedTest.h"
#include "Logger.h"

template<class T>
uint64_t GetMean(const std::vector<T>& vec)
{
    T sum = 0;
    for (const auto& v : vec)
    {
        sum += v;
    }
    return sum / vec.size();
}
uint64_t GetVar(const std::vector<uint64_t>& vec)
{
    uint64_t sum = 0;
    uint64_t meanValue = GetMean(vec);
    for (const auto& v : vec)
    {
        if (v > meanValue)
            sum += (v - meanValue) * (v - meanValue);
        else
            sum += (meanValue - v) * (meanValue - v);
    }
    return std::sqrt(sum) / vec.size();
}
void PrintResult(std::string msgQName, int inThreadNum, int outThreadNum, int totalMsg, const std::vector<uint64_t>& vec, int totalTest, const std::vector<int>& vecCannotAddMsg)
{
    std::stringstream ss;
    ss << "MsQName: " << msgQName;
    LOGMSG_MSG_S_C() << ss.str() << "\n";
    ss.str("");
    ss << "ThreadIN: " << inThreadNum
       << " ThreadOUT: " << outThreadNum
       << " MsgNumber: " << totalMsg
       << " Total Test: " << totalTest;
    LOGMSG_MSG_S_C() << ss.str() << "\n";
    ss.str("");
    uint64_t meanValue = GetMean(vec);
    ss << "Used Time (sec): " << meanValue / 1000 / 1000
       << " Used Time (msec): " << meanValue / 1000
       << " Used Time (nsec): " << meanValue
       << " Variance (nsec): " << GetVar(vec)
       << " Cannot Add Msg: " << GetMean(vecCannotAddMsg);
    LOGMSG_MSG_S_C() << ss.str() << "\n";
}
void PrintResultRaw(std::string msgQName, int inThreadNum, int outThreadNum, int totalMsg, const std::vector<uint64_t>& vec, int totalTest, const std::vector<int>& vecCannotAddMsg)
{
    uint64_t meanValue = GetMean(vec);
    std::stringstream ss;
    ss << msgQName
       << "," << inThreadNum
       << "," << outThreadNum
       << "," << totalMsg
       << "," << totalTest
       << "," << meanValue / 1000; // msec
    LOGMSG_MSG_S_C() << ss.str() << "\n";
}
void RunTestMain(std::string msgQName, int inThreadNum, int outThreadNum, int totalTest, int totalMsg)
{
    std::vector<uint64_t> resultTimes; resultTimes.resize(totalTest, 0xFFFFFFFFFFFFFFFF);
    std::vector<int> resultCannotAddMsg; resultCannotAddMsg.resize(totalTest, 0xFFFFFFFF);
    for (int i = 0; i < totalTest; i++)
    {
        // LOGMSG_MSG_C("Start test: %d\n", i);
        SpeedTest test;
        test.InitComponent(msgQName, inThreadNum, outThreadNum, totalMsg);
        test.RunTest();
        resultTimes[i] = test.GetResultTimeNSec();
        resultCannotAddMsg[i] = test.GetCannotAddMsgCount();
    }
    PrintResultRaw(msgQName, inThreadNum, outThreadNum, totalMsg, resultTimes, totalTest, resultCannotAddMsg);
}
void RunTestMain000(std::string msgQName, int totalTest, int totalMsg)
{
    std::vector<int> numThreads = {1, 2, 4, 10};
    for (size_t i = 0; i < numThreads.size(); i++)
    {
        RunTestMain(msgQName, numThreads[i], numThreads[i], totalTest, totalMsg);
    }
}
int main(int argc, char* argv[])
{
    // std::shared_ptr<int> tt = std::make_shared<int>(10);
    // bool yy = false;
    // std::atomic<bool> xx = true;
    // while (!xx.compare_exchange_weak(yy, true));
    // LOGMSG_MSG_S_C() << std::atomic_is_lock_free(&xx) << "\n";
    // LOGMSG_MSG_S_C() << yy << "\n";
    // return 0;
    // Test para
    int totalTest = 5;
    int totalMsg = 300000;
    int inThreadNum = 1;
    int outThreadNum = 1;
    RunTestMain("MsgQLockFree_Linux", inThreadNum, outThreadNum, totalTest, totalMsg);
    RunTestMain("MsgQLockFree_LinkList_Std", inThreadNum, outThreadNum, totalTest, totalMsg);

    RunTestMain000("MsgStackLockFree_LinkList_Std", totalTest, totalMsg);
    RunTestMain000("MsgQOneLock_RingBuf_Linux", totalTest, totalMsg);
    RunTestMain000("MsgQTwoLock_RingBuf_Linux", totalTest, totalMsg);
    RunTestMain000("MsgQOneLock_RingBuf_Std", totalTest, totalMsg);
    RunTestMain000("MsgQTwoLock_RingBuf_Std", totalTest, totalMsg);
    RunTestMain000("MsgQOneLock_LinkList_Linux", totalTest, totalMsg);
    RunTestMain000("MsgQTwoLock_LinkList_Linux", totalTest, totalMsg);
    RunTestMain000("MsgQOneLock_LinkList_Std", totalTest, totalMsg);
    RunTestMain000("MsgQTwoLock_LinkList_Std", totalTest, totalMsg);
    RunTestMain000("MsgQOneLock_Queue_Linux", totalTest, totalMsg);
    RunTestMain000("MsgQOneLock_Queue_Std", totalTest, totalMsg);

    return 0;
}
