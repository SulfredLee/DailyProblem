#include <iostream>
#include <chrono>
#include <string>
#include <thread>

using namespace std::chrono;
std::string GetTimeString(const time_point<system_clock>& tp, const std::string& format)
{
    std::time_t now_c = std::chrono::system_clock::to_time_t(tp);
    std::tm now_tm = *std::localtime(&now_c);
    char buff[70];
    strftime(buff, sizeof(buff), format.c_str(), &now_tm);
    return buff;
}

void TrySystemClock()
{
    std::cout << __FUNCTION__ << ":" << __LINE__ << " Start==========================" << std::endl;

    time_point<system_clock> sysClock = system_clock::now();
    std::cout << GetTimeString(sysClock, "%Y-%m-%d %H:%M:%S") << std::endl;
    std::cout << GetTimeString(sysClock, "%F %T") << std::endl;

    std::cout << __FUNCTION__ << ":" << __LINE__ << " End==========================" << std::endl;
}

void TrySteadyClock()
{
    std::cout << __FUNCTION__ << ":" << __LINE__ << " Start==========================" << std::endl;

    steady_clock::time_point t1 = steady_clock::now();

    std::cout << "printing out 1000 stars...\n";
    for (int i=0; i<1000; ++i) std::cout << "*";
    std::cout << std::endl;

    steady_clock::time_point t2 = steady_clock::now();

    duration<double> time_span = duration_cast<duration<double>>(t2 - t1);

    std::cout << "It took me " << time_span.count() << " seconds.";
    std::cout << std::endl;

    std::cout << __FUNCTION__ << ":" << __LINE__ << " End==========================" << std::endl;
}

void TryHighResolutionClock()
{
    std::cout << __FUNCTION__ << ":" << __LINE__ << " Start==========================" << std::endl;

    high_resolution_clock::time_point t1 = high_resolution_clock::now();

    std::cout << "printing out 1000 stars...\n";
    for (int i=0; i<1000; ++i) std::cout << "*";
    std::cout << std::endl;

    high_resolution_clock::time_point t2 = high_resolution_clock::now();

    duration<double> time_span = duration_cast<duration<double>>(t2 - t1);

    std::cout << "It took me " << time_span.count() << " seconds.";
    std::cout << std::endl;

    std::cout << __FUNCTION__ << ":" << __LINE__ << " End==========================" << std::endl;
}

int main(int argc, char* argv[])
{
    TrySystemClock();
    TrySteadyClock();
    TryHighResolutionClock();

    return 0;
}
