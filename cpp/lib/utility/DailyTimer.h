#ifndef DAILYTIMER_H
#define DAILYTIMER_H

#include <thread>
#include <memory>
#include <functional>
#include <atomic>

#include <string>
#include <sstream>

#include "NLTimeUTC.h"
#include "LinuxCond.h"

// example
// class TradingWorker
// {
//      void DailyTimeUpCallback();
// };
//
// std::unique_ptr<DailyTimer> timer = std::unique_ptr<DailyTimer>(new DailyTimer(it->m_tradeTime, std::bind(&TradingWorker::DailyTimeUpCallback, this, *it)))
// std::unique_ptr<DailyTimer> timer = std::make_unique<DailyTimer>(it->m_tradeTime, std::bind(&TradingWorker::DailyTimeUpCallback, this, *it))
//
// std::unique_ptr<DailyTimer> timer = std::make_unique<DailyTimer>(it->m_tradeTime, [=] (int x) { int y = x; }, 10);

class DailyTimer{
public:
    template <class Fn, class... Args>
        DailyTimer(const NLTimeUTC& DateTimeIN, Fn&& fn, Args&&... args);
    ~DailyTimer();

    void Start();
    void Stop();
private:
    bool IsTimeUP();
    bool ValidateTargetTime();
    void Main();
private:
    std::thread m_TimerThread;
    std::atomic<bool> m_bTimerThreadExit;
    std::atomic<bool> m_bTimerThreadStop;
    NLTimeUTC m_DateTime;
    std::function<void()> m_fn;
    int m_sleepTimeMSec;
    LinuxCond m_waitCond;
};

template <class Fn, class... Args>
    DailyTimer::DailyTimer(const NLTimeUTC& DateTimeIN, Fn&& fn, Args&&... args)
    : m_DateTime(DateTimeIN)
    , m_fn(std::bind(std::forward<Fn>(fn), std::forward<Args>(args)...))
    , m_sleepTimeMSec(30){
        m_bTimerThreadStop = false;
        m_bTimerThreadExit = false;
        m_TimerThread = std::thread(&DailyTimer::Main, this);
}
#endif
