#include <iostream>
#include <thread>

#include "CountTimer.h"

// usage: ./CountTimer
void SimpleStartStop()
{
    std::cout << "Simple Start Stop:" << std::endl;
    using namespace std::chrono_literals;
    CountTimer timer;
    timer.Start();
    std::this_thread::sleep_for(200ms);
    timer.Stop();
    std::cout << "Second: " << timer.GetSecond()
              << " MSecond: " << timer.GetMSecond()
              << " NSecond: " << timer.GetNSecond() << std::endl;
}
void MovingStartStop()
{
    std::cout << "Moving Start Stop:" << std::endl;
    using namespace std::chrono_literals;
    CountTimer timer;
    timer.Start();
    for (int i = 0; i < 3; i++)
    {
        std::this_thread::sleep_for(500ms);
        timer.MovingStop();
        std::cout << "Second: " << timer.GetSecond()
                  << " MSecond: " << timer.GetMSecond()
                  << " NSecond: " << timer.GetNSecond() << std::endl;
    }
}
void TimeToString()
{
    std::cout << "Time To String:" << std::endl;
    using namespace std::chrono_literals;
    CountTimer timer;
    timer.Start();
    std::cout << "StartTimeGmt: " << timer.ToStringStartTime() << " StartTimeLocal: " << timer.ToStringStartTime(false) << std::endl;
    std::this_thread::sleep_for(1s);
    timer.Stop();
    std::cout << "StopTimeGmt: " << timer.ToStringStopTime() << " StopTimeLocal: " << timer.ToStringStopTime(false) << std::endl;
}
int main(int argc, char *argv[])
{
    SimpleStartStop();
    MovingStartStop();
    TimeToString();

    return 0;
}
