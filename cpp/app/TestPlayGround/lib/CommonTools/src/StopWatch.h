#ifndef STOPWATCH_H
#define STOPWATCH_H
#include <chrono>
#include <ctime>
#include <string>
#include <atomic>
#include <mutex>

class StopWatch
{
 public:
    StopWatch();
    ~StopWatch();

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
    std::chrono::high_resolution_clock::time_point m_start;
    std::chrono::high_resolution_clock::time_point m_end;
    std::chrono::duration<double> m_elapsed_seconds;
    std::atomic<bool> m_started;
    std::mutex m_mutex;
};

#endif
