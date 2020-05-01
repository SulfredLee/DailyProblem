#ifndef MSECTIMER_H
#define MSECTIMER_H

#include <thread>
#include <memory>
#include <functional>
#include <atomic>

#include <time.h>

#include "LinuxCond.h"
class MSecTimer{
public:
    template <class Fn, class... Args>
    MSecTimer(const unsigned int& unDuration, Fn&& fn, Args&&... args);
    ~MSecTimer();

    void Start();
    void Stop();
private:
    void Main();
private:
    std::thread m_TimerThread;
    std::atomic<bool> m_bTimerThreadExit;
    std::atomic<bool> m_bTimerThreadStop;
    unsigned int m_unDuration; // MSec
    std::function<void()> m_fn;
    LinuxCond m_waitCond;
};

template <class Fn, class... Args>
    MSecTimer::MSecTimer(const unsigned int& unDuration, Fn&& fn, Args&&... args)
    : m_unDuration(unDuration)
    , m_fn(std::bind(std::forward<Fn>(fn), std::forward<Args>(args)...)){
        m_bTimerThreadStop = false;
        m_bTimerThreadExit = false;
        m_TimerThread = std::thread(&MSecTimer::Main, this);
}
#endif
