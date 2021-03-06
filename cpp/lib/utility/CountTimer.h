#ifndef COUNTTIMER_H
#define COUNTTIMER_H
#include <chrono>
#include <ctime>
#include <string>
#include <atomic>
#include <mutex>

class CountTimer
{
 public:
    CountTimer();
    ~CountTimer();

    void Start();
    void Stop();
    void MovingStop();

    double GetSecondDouble() const;
    uint64_t GetSecond() const;
    uint64_t GetMSecond() const;
    uint64_t GetNSecond() const;
    // toString("%Y %m %d %H %M %S"), Year Month Day Hour Minute Second
    std::string ToStringStartTime(bool isGMT = true, std::string format = "%Y-%m-%d %H:%M:%S") const;
    std::string ToStringStopTime(bool isGMT = true, std::string format = "%Y-%m-%d %H:%M:%S") const;
 private:
    std::chrono::time_point<std::chrono::system_clock> m_start;
    std::chrono::time_point<std::chrono::system_clock> m_end;
    std::chrono::duration<double> m_elapsed_seconds;
    std::atomic<bool> m_started;
    std::mutex m_mutex;
};

#endif
