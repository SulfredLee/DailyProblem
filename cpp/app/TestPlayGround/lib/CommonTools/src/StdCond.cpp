#include "StdCond.h"

using namespace std::chrono_literals;

StdCond::StdCond()
{
}

StdCond::~StdCond()
{
}

void StdCond::Signal()
{
    m_cond.notify_one();
}

bool StdCond::WaitWithTime(int MSec)
{
    std::unique_lock<std::mutex> lock(m_mutex);
    auto now = std::chrono::system_clock::now();
    return m_cond.wait_until(lock, now + (MSec * 1ms), [&] { return false; });
}

void StdCond::Wait()
{
    std::unique_lock<std::mutex> lock(m_mutex);
    m_cond.wait(lock, [&] {return false; });
}
