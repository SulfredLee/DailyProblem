#include "StopWatch.h"

StopWatch::StopWatch()
{
    m_started = false;
}

StopWatch::~StopWatch()
{}

void StopWatch::Start()
{
    std::lock_guard<std::mutex> lock(m_mutex);
    m_start = std::chrono::high_resolution_clock::now();
    m_started = true;
}

void StopWatch::Stop()
{
    std::lock_guard<std::mutex> lock(m_mutex);
    if (m_started)
    {
        m_started = false;
        m_end = std::chrono::high_resolution_clock::now();
        m_elapsed_seconds = m_end - m_start;
    }
}

void StopWatch::MovingStop()
{
    std::lock_guard<std::mutex> lock(m_mutex);
    m_end = std::chrono::high_resolution_clock::now();
    m_elapsed_seconds = m_end - m_start;
}

double StopWatch::GetSecondDouble() const
{
    return m_elapsed_seconds.count();
}

uint64_t StopWatch::GetSecond() const
{
    return static_cast<uint64_t>(m_elapsed_seconds.count() + 0.5);
}

uint64_t StopWatch::GetMSecond() const
{
    return static_cast<uint64_t>(m_elapsed_seconds.count() * 1000 + 0.5);
}

uint64_t StopWatch::GetNSecond() const
{
    return static_cast<uint64_t>(m_elapsed_seconds.count() * 1000 * 1000 + 0.5);
}

std::string StopWatch::ToStringStartTime(bool isGMT, std::string format) const
{
    std::time_t tempTimeT = std::chrono::high_resolution_clock::to_time_t(m_start);
    tm tempTimeTM;
    if (isGMT)
        gmtime_r(&tempTimeT, &tempTimeTM);
    else
        localtime_r(&tempTimeT, &tempTimeTM);
    char buff[1024];
    strftime(buff, sizeof(buff), format.c_str(), &tempTimeTM);
    return std::string(buff);
}

std::string StopWatch::ToStringStopTime(bool isGMT, std::string format) const
{
    std::time_t tempTimeT = std::chrono::high_resolution_clock::to_time_t(m_end);
    tm tempTimeTM;
    if (isGMT)
        gmtime_r(&tempTimeT, &tempTimeTM);
    else
        localtime_r(&tempTimeT, &tempTimeTM);
    char buff[1024];
    strftime(buff, sizeof(buff), format.c_str(), &tempTimeTM);
    return std::string(buff);
}
