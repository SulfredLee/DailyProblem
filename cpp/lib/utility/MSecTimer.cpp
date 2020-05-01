#include "MSecTimer.h"

#include <unistd.h>
MSecTimer::~MSecTimer(){
    m_bTimerThreadStop = true;
    m_bTimerThreadExit = true;
    m_waitCond.Signal();
    m_TimerThread.join();
}

void MSecTimer::Start(){
    m_bTimerThreadStop = false;
}

void MSecTimer::Stop(){
    m_bTimerThreadStop = true;
    m_waitCond.Signal();
}

void MSecTimer::Main(){
    int sleepDurationMSec = m_unDuration;
    while (!m_bTimerThreadExit)
    {
        m_waitCond.WaitWithTime(sleepDurationMSec);
        if (!m_bTimerThreadStop)
        {
            m_fn();
        }
    }
}
