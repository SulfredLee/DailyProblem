#include "NLClock.h"

NLClock::NLClock()
{
    m_isDebug = false;
    m_isEnableToTune = false;
    m_countEnableToTune = 0;
}

NLClock::~NLClock()
{
}

NLClock& NLClock::GetInstance()
{
    static NLClock instance;
    return instance;
}

bool NLClock::IsDebugMode()
{
    DefaultLock lock(m_mutex);
    return m_isDebug;
}

void NLClock::SetDebugMode(bool isDebug)
{
    DefaultLock lock(m_mutex);
    m_isDebug = isDebug;
    m_isEnableToTune = isDebug;
}

void NLClock::SetClock(time_t unixTimeInSeconds)
{
    DefaultLock lock(m_mutex);
    InitStructure();

    gmtime_r(&unixTimeInSeconds, &m_time);
    mktime(&m_time); /* call mktime: timeinfo->tm_wday will be set */
}

void NLClock::SetClock(int Y, int Mon, int D, int H, int Min, int S)
{
    DefaultLock lock(m_mutex);
    InitStructure();

    m_time.tm_year = Y - 1900;
    m_time.tm_mon = Mon - 1;
    m_time.tm_mday = D;
    m_time.tm_hour = H;
    m_time.tm_min = Min;
    m_time.tm_sec = S;
    mktime(&m_time);
}

void NLClock::SetEnableToTune(bool enable)
{
    DefaultLock lock(m_mutex);
    if (enable == true)
    {
        if (m_countEnableToTune <= 1)
        {
            m_isEnableToTune = true;
            m_countEnableToTune = 0;
        }
        else
            m_countEnableToTune--;
    }
    else
    {
        m_countEnableToTune++;
        m_isEnableToTune = false;
    }
}

void NLClock::AddSec(int sec)
{
    DefaultLock lock(m_mutex);
    if (m_isEnableToTune)
    {
        m_time.tm_sec += sec;
        mktime(&m_time);
    }
}

time_t NLClock::GetTimeT() const
{
    DefaultLock lock(m_mutex);
    tm result = m_time;
    result.tm_sec -= timezone;
    return mktime(&result);
}

void NLClock::InitStructure()
{
    // init the tm structure
    time_t rawTime;
    time(&rawTime);
    gmtime_r(&rawTime, &m_time);
}

std::string NLClock::ToString(std::string format)
{
    char buff[1024];
    strftime(buff, sizeof(buff), format.c_str(), &m_time);
    return std::string(buff);
}
