#ifndef TSCLOCK_H
#define TSCLOCK_H
#include "DefaultMutex.h"

#include <time.h>
#include <string>
class NLClock
{
 public:
    ~NLClock();

    static NLClock& GetInstance();
    bool IsDebugMode();
    void SetDebugMode(bool isDebug);
    void SetClock(time_t unixTimeInSeconds);
    void SetClock(int Y, int Mon, int D, int H, int Min, int S); // input UTC time
    void SetEnableToTune(bool enable);
    void AddSec(int sec);
    time_t GetTimeT() const ;

    // toString("%Y %m %d %H %M %S"), Year Month Day Hour Minute Second
    std::string ToString(std::string format = "%Y-%m-%d %H:%M:%S");
 private:
    NLClock();
    NLClock(const NLClock&) = delete;
    NLClock & operator=(const NLClock&) = delete;

    void InitStructure();
 private:
    bool m_isDebug;
    bool m_isEnableToTune;
    int m_countEnableToTune;
    mutable DefaultMutex m_mutex;
    struct tm m_time;
};

#define TSCLOCK_IS_DEBUG() NLClock::GetInstance().IsDebugMode()
#define TSCLOCK_SET_DEBUG(isDebug) NLClock::GetInstance().SetDebugMode(isDebug)
#define TSCLOCK_SET_CLOCK_UNIX_TIME(unixTimeInSeconds) NLClock::GetInstance().SetClock(unixTimeInSeconds)
#define TSCLOCK_SET_CLOCK_DATE(Y, Mon, D, H, Min, S) NLClock::GetInstance().SetClock(Y, Mon, D, H, Min, S)
#define TSCLOCK_SET_ENABLE_TO_TUNE(enable) NLClock::GetInstance().SetEnableToTune(enable);
#define TSCLOCK_ADD_SEC(sec) NLClock::GetInstance().AddSec(sec)
#define TSCLOCK_GET_TIME_T() NLClock::GetInstance().GetTimeT()
#define TSCLOCK_GET_TIME_STRING() NLClock::GetInstance().ToString()

#endif
