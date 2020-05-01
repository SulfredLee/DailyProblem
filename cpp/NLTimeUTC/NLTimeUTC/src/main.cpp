#include <iostream>
#include <thread>
#include <chrono>

#include "NLTimeUTC.h"

// usage: ./NLTimeUTC
void NormalUseCase()
{
    std::cout << __FUNCTION__ << "-----------------" << std::endl;
    {
        NLTimeUTC time;
        std::cout << time.ToString() << std::endl;
    }
    std::this_thread::sleep_for(std::chrono::seconds(1));
    {
        NLTimeUTC time;
        std::cout << time.ToString() << std::endl;
    }
}
void DebugUseCase_TickTick()
{
    {
        NLTimeUTC time;
        std::cout << time.ToString() << std::endl;
    }
    if (TSCLOCK_IS_DEBUG())
        TSCLOCK_ADD_SEC(1);
    else
        std::this_thread::sleep_for(std::chrono::seconds(1));
    {
        NLTimeUTC time;
        std::cout << time.ToString() << std::endl;
    }
}
void DebugUseCase()
{
    std::cout << std::endl;
    std::cout << __FUNCTION__ << "-----------------" << std::endl;
    std::cout << "Is debug: " << TSCLOCK_IS_DEBUG() << std::endl;
    DebugUseCase_TickTick();

    TSCLOCK_SET_DEBUG(true);
    std::cout << "Is debug: " << TSCLOCK_IS_DEBUG() << std::endl;
    TSCLOCK_SET_CLOCK_DATE(2020, 3, 23, 3, 32, 40);
    DebugUseCase_TickTick();
}
int main(int argc, char *argv[])
{
    NormalUseCase();
    DebugUseCase();
    return 0;
}
