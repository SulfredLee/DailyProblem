#ifndef STD_COND_H
#define STD_COND_H
#include <condition_variable>
#include <thread>
#include <chrono>
#include <atomic>

class StdCond
{
 public:
    StdCond();
    ~StdCond();

    void Signal();
    bool WaitWithTime(int MSec);
    void Wait();
 private:
    std::condition_variable m_cond;
    std::mutex m_mutex;
    std::atomic<bool> m_getSignal;
};

#endif
