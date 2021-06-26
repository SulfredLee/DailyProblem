#ifndef STD_THREAD_H
#define STD_THREAD_H
#include <thread>
#include <atomic>
#include <chrono>

class StdThread
{
 public:
    StdThread();
    virtual ~StdThread();
 protected:
    virtual void* Main() = 0;

    bool StartThread();
    void StopThread();
    void JoinThread();
    bool IsThreadRunning();

 protected:
    std::thread m_thread;
 private:
    std::atomic<bool> m_isRun;
};

#endif
