#include "DailyTimer.h"
#include "Logger.h"

#include <unistd.h>
#include <iostream>
DailyTimer::~DailyTimer()
{
    m_bTimerThreadStop = true;
    m_bTimerThreadExit = true;
    m_waitCond.Signal();
    m_TimerThread.join();
}

void DailyTimer::Start()
{
    m_bTimerThreadStop = false;
}

void DailyTimer::Stop()
{
    m_bTimerThreadStop = true;
    m_waitCond.Signal();
}

bool DailyTimer::IsTimeUP()
{
    NLTimeUTC curTime;
    LOGMSG_DBG_S() << "curTime: " << curTime.ToString() << "\n";
    LOGMSG_DBG_S() << "m_DateTime: " << m_DateTime.ToString() << "\n";
    if (m_DateTime == curTime)
        return true;
    else if (m_DateTime - curTime > 5)
    {
        m_sleepTimeMSec = static_cast<int>(m_DateTime - curTime) * 1000 - 5000;
        return false;
    }
    else
    {
        m_sleepTimeMSec = 30;
        return false;
    }
}

bool DailyTimer::ValidateTargetTime()
{
    NLTimeUTC curTime; curTime.GetCurrentTime();
    if (m_DateTime < curTime)
    {
        int Year, Month, Day;
        curTime.GetDate(Year, Month, Day);
        m_DateTime.SetDate(Year, Month, Day);

        while (m_DateTime < curTime)
            m_DateTime.AddDate(0, 0, 1);
        return true;
    }
    return false;
}

void DailyTimer::Main()
{
    ValidateTargetTime();
    {
        std::stringstream ss; ss << "Next alert time: " << m_DateTime.ToString();
        LOGMSG_MSG("%s\n", ss.str().c_str());
    }
    while (!m_bTimerThreadExit)
    {
        m_waitCond.WaitWithTime(m_sleepTimeMSec);
        if (!m_bTimerThreadStop && IsTimeUP())
        {
            m_DateTime.AddDate(0, 0, 1);
            m_fn();
        }
        else
        {
            if (ValidateTargetTime())
            {
                std::stringstream ss; ss << "Next alert time: " << m_DateTime.ToString();
                LOGMSG_MSG("%s\n", ss.str().c_str());
            }
        }
    }
}
