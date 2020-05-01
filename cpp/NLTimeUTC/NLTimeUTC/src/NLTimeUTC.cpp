#include "NLTimeUTC.h"

#include <utility>

NLTimeUTC::NLTimeUTC()
{
    mktime(&m_time);
    GetCurrentTime();
}

NLTimeUTC::NLTimeUTC(time_t unixTimeInSeconds)
    : NLTimeUTC()
{
    gmtime_r(&unixTimeInSeconds, &m_time);
    mktime(&m_time); /* call mktime: timeinfo->tm_wday will be set */
}

NLTimeUTC::NLTimeUTC(int Y, int Mon, int D, int H, int Min, int S)
    : NLTimeUTC()
{
    m_time.tm_year = Y - 1900;
    m_time.tm_mon = Mon - 1;
    m_time.tm_mday = D;
    m_time.tm_hour = H;
    m_time.tm_min = Min;
    m_time.tm_sec = S;
    mktime(&m_time);
}

NLTimeUTC::NLTimeUTC(const std::string& source, const std::string& format)
    : NLTimeUTC()
{
    SetFromString(source, format);
}

NLTimeUTC::NLTimeUTC(const NLTimeUTC& other)
{
    time_t tempTime = other.GetTimeT();
    gmtime_r(&tempTime, &m_time);
    mktime(&m_time);
}

NLTimeUTC::~NLTimeUTC()
{}

tm NLTimeUTC::GetRawData()
{
    return m_time;
}

tm const * const NLTimeUTC::GetRawDataPointer()
{
    return &m_time;
}

time_t NLTimeUTC::GetTimeT()
{
    tm result = m_time;
    result.tm_sec -= timezone;
    return mktime(&result);
}

time_t NLTimeUTC::GetTimeT() const
{
    tm result = m_time;
    result.tm_sec -= timezone;
    return mktime(&result);
}

void NLTimeUTC::GetCurrentTime()
{
    time_t rawTime;
    if (TSCLOCK_IS_DEBUG())
        rawTime = TSCLOCK_GET_TIME_T();
    else
        time(&rawTime);
    // m_time = *localtime(&rawTime);
    gmtime_r(&rawTime, &m_time);
}

void NLTimeUTC::GetDate(int& Y, int& Mon, int& D)
{
    Y = m_time.tm_year + 1900;
    Mon = m_time.tm_mon + 1;
    D = m_time.tm_mday;
}

void NLTimeUTC::GetTime(int& H, int& Min, int& S)
{
    H = m_time.tm_hour;
    Min = m_time.tm_min;
    S = m_time.tm_sec;
}

void NLTimeUTC::GetDate(int& Y, int& Mon, int& D) const
{
    Y = m_time.tm_year + 1900;
    Mon = m_time.tm_mon + 1;
    D = m_time.tm_mday;
}

void NLTimeUTC::GetTime(int& H, int& Min, int& S) const
{
    H = m_time.tm_hour;
    Min = m_time.tm_min;
    S = m_time.tm_sec;
}

void NLTimeUTC::SetFromString(const std::string& source, const std::string& format)
{
    strptime(source.c_str(), format.c_str(), &m_time);
    mktime(&m_time);
}

void NLTimeUTC::SetDate(int Y, int Mon, int D)
{
    m_time.tm_year = Y - 1900;
    m_time.tm_mon = Mon - 1;
    m_time.tm_mday = D;
    mktime(&m_time);
}

void NLTimeUTC::SetTime(int H, int Min, int S)
{
    m_time.tm_hour = H;
    m_time.tm_min = Min;
    m_time.tm_sec = S;
    mktime(&m_time);
}

void NLTimeUTC::AddDate(int Y, int Mon, int D)
{
    m_time.tm_year += Y;
    m_time.tm_mon += Mon;
    m_time.tm_mday += D;
    mktime(&m_time);
}

void NLTimeUTC::AddTime(int H, int Min, int S)
{
    m_time.tm_hour += H;
    m_time.tm_min += Min;
    m_time.tm_sec += S;
    mktime(&m_time);
}

bool NLTimeUTC::IsSameDate(const NLTimeUTC& other)
{
    int thisY, thisMon, thisD;
    GetDate(thisY, thisMon, thisD);
    int otherY, otherMon, otherD;
    other.GetDate(otherY, otherMon, otherD);

    if (thisY == otherY && thisMon == otherMon && thisD == otherD)
        return true;
    else
        return false;
}

std::string NLTimeUTC::ToString(std::string format)
{
    char buff[1024];
    strftime(buff, sizeof(buff), format.c_str(), &m_time);
    return std::string(buff);
}

std::string NLTimeUTC::ToString(std::string format) const
{
    char buff[1024];
    strftime(buff, sizeof(buff), format.c_str(), &m_time);
    return std::string(buff);
}

NLTimeUTC& NLTimeUTC::operator+= (const NLTimeUTC& that)
{
    m_time.tm_year += that.m_time.tm_year;
    m_time.tm_mon += that.m_time.tm_mon;
    m_time.tm_mday += that.m_time.tm_mday;
    m_time.tm_hour += that.m_time.tm_hour;
    m_time.tm_min += that.m_time.tm_min;
    m_time.tm_sec += that.m_time.tm_sec;
    mktime(&m_time);
    return *this;
}

bool operator== (const NLTimeUTC& lhs, const NLTimeUTC& rhs)
{
    return difftime(lhs.GetTimeT(), rhs.GetTimeT()) == 0 ? true : false;
}

bool operator!= (const NLTimeUTC& lhs, const NLTimeUTC& rhs)
{
    return !(lhs == rhs);
}

bool operator< (const NLTimeUTC& lhs, const NLTimeUTC& rhs)
{
    return difftime(lhs.GetTimeT(), rhs.GetTimeT()) < 0 ? true : false;
}

bool operator> (const NLTimeUTC& lhs, const NLTimeUTC& rhs)
{
    return rhs < lhs;
}

bool operator>= (const NLTimeUTC& lhs, const NLTimeUTC& rhs)
{
    return !(lhs < rhs);
}

bool operator<= (const NLTimeUTC& lhs, const NLTimeUTC& rhs)
{
    return !(rhs < lhs);
}

double operator- (const NLTimeUTC& lhs, const NLTimeUTC& rhs)
{
    return difftime(lhs.GetTimeT(), rhs.GetTimeT());
}

double operator- (const NLTimeUTC& lhs, NLTimeUTC&& rhs)
{
    return difftime(lhs.GetTimeT(), rhs.GetTimeT());
}

double operator- (NLTimeUTC&& lhs, const NLTimeUTC& rhs)
{
    return difftime(lhs.GetTimeT(), rhs.GetTimeT());
}

double operator- (NLTimeUTC&& lhs, NLTimeUTC&& rhs)
{
    return difftime(lhs.GetTimeT(), rhs.GetTimeT());
}

NLTimeUTC operator+ (const NLTimeUTC& lhs, const NLTimeUTC& rhs)
{
    NLTimeUTC temp = lhs;
    return temp += rhs;
}

NLTimeUTC&& operator+ (const NLTimeUTC& lhs, NLTimeUTC&& rhs)
{
    return std::move(rhs += lhs);
}

NLTimeUTC&& operator+ (NLTimeUTC&& lhs, const NLTimeUTC& rhs)
{
    return std::move(lhs += rhs);
}

NLTimeUTC&& operator+ (NLTimeUTC&& lhs, NLTimeUTC&& rhs)
{
    return std::move(lhs += rhs);
}
