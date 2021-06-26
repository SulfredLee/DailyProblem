#include "StdThread.h"

using namespace std::chrono_literals;
StdThread::StdThread()
{
    m_isRun.store(false);
}

StdThread::~StdThread()
{
    StopThread();
}

bool StdThread::StartThread()
{
    m_isRun.store(true);
    m_thread = std::thread(&StdThread::Main, this);
    std::this_thread::sleep_for(1ms);
    m_thread.detach();
    return true;
}

void StdThread::StopThread()
{
    if (m_isRun.load())
    {
        m_isRun.store(false);
        JoinThread();
    }
}

void StdThread::JoinThread()
{
    if (m_thread.joinable()) m_thread.join();
}

bool StdThread::IsThreadRunning()
{
    return m_isRun.load();
}
