#ifndef TSTIMEUTC_H
#define TSTIMEUTC_H
#include <string>

#include <time.h>

#include "NLClock.h"
// This Time structure stored a UTC time
class NLTimeUTC
{
 private:
    mutable struct tm m_time; // this is UTC time
 public:
    NLTimeUTC();
    NLTimeUTC(time_t unixTimeInSeconds);
    NLTimeUTC(int Y, int Mon, int D, int H, int Min, int S);
    NLTimeUTC(const std::string& source, const std::string& format);
    NLTimeUTC(const NLTimeUTC& other);
    ~NLTimeUTC();

    struct tm GetRawData();
    struct tm const * const GetRawDataPointer();
    time_t GetTimeT();
    time_t GetTimeT() const;
    void GetCurrentTime();
    void GetDate(int& Y, int& Mon, int& D);
    void GetTime(int& H, int& Min, int& S);
    void GetDate(int& Y, int& Mon, int& D) const;
    void GetTime(int& H, int& Min, int& S) const;

    void SetFromString(const std::string& source, const std::string& format);

    void SetDate(int Y, int Mon, int D);
    void SetTime(int H, int Min, int S);

    void AddDate(int Y, int Mon, int D);
    void AddTime(int H, int Min, int S);

    bool IsSameDate(const NLTimeUTC& other);

    // example
    // toString("%Y %m %d %H %M %S"), Year Month Day Hour Minute Second
    std::string ToString(std::string format = "%Y-%m-%d %H:%M:%S");
    std::string ToString(std::string format = "%Y-%m-%d %H:%M:%S") const;

    // there has no meaning for += operator, implement for demo only
    NLTimeUTC& operator+= (const NLTimeUTC& that);
};
bool operator== (const NLTimeUTC& lhs, const NLTimeUTC& rhs);
bool operator!= (const NLTimeUTC& lhs, const NLTimeUTC& rhs);
bool operator< (const NLTimeUTC& lhs, const NLTimeUTC& rhs);
bool operator> (const NLTimeUTC& lhs, const NLTimeUTC& rhs);
bool operator>= (const NLTimeUTC& lhs, const NLTimeUTC& rhs);
bool operator<= (const NLTimeUTC& lhs, const NLTimeUTC& rhs);

// return seconds for - operator
double operator- (const NLTimeUTC& lhs, const NLTimeUTC& rhs);
double operator- (const NLTimeUTC& lhs, NLTimeUTC&& rhs);
double operator- (NLTimeUTC&& lhs, const NLTimeUTC& rhs);
double operator- (NLTimeUTC&& lhs, NLTimeUTC&& rhs);

// there has no meaning for + operator, implement for demo only
NLTimeUTC operator+ (const NLTimeUTC& lhs, const NLTimeUTC& rhs);
NLTimeUTC&& operator+ (const NLTimeUTC& lhs, NLTimeUTC&& rhs);
NLTimeUTC&& operator+ (NLTimeUTC&& lhs, const NLTimeUTC& rhs);
NLTimeUTC&& operator+ (NLTimeUTC&& lhs, NLTimeUTC&& rhs);
#endif
