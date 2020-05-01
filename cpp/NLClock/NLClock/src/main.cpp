#include <iostream>

#include "NLClock.h"

void StartStopDebug()
{
    std::cout << __FUNCTION__ << "-------------" << std::endl;
    std::cout << TSCLOCK_IS_DEBUG() << std::endl;
    TSCLOCK_SET_DEBUG(true);
    std::cout << TSCLOCK_IS_DEBUG() << std::endl;
    TSCLOCK_SET_DEBUG(false);
    std::cout << TSCLOCK_IS_DEBUG() << std::endl;
}
void SetClock()
{
    std::cout << std::endl;
    std::cout << __FUNCTION__ << "-------------" << std::endl;
    TSCLOCK_SET_CLOCK_DATE(2020, 3, 20, 1, 20, 34);
    std::cout << TSCLOCK_GET_TIME_STRING() << std::endl;
}
void AddSecExample()
{
    std::cout << std::endl;
    std::cout << __FUNCTION__ << "-------------" << std::endl;
    TSCLOCK_SET_CLOCK_DATE(2020, 3, 20, 1, 20, 34);
    std::cout << "Set clock: " << TSCLOCK_GET_TIME_STRING() << std::endl;
    TSCLOCK_ADD_SEC(1); // fail to add sec since currently is not be able to tune
    std::cout << "Fail example: " << TSCLOCK_GET_TIME_STRING() << std::endl;

    TSCLOCK_SET_ENABLE_TO_TUNE(true);
    TSCLOCK_ADD_SEC(1); // able to tune
    std::cout << "Success example: " << TSCLOCK_GET_TIME_STRING() << std::endl;
}
void AddSecExampleAdvance()
{
    std::cout << std::endl;
    std::cout << __FUNCTION__ << "-------------" << std::endl;
    TSCLOCK_SET_CLOCK_DATE(2020, 3, 20, 1, 20, 34);
    std::cout << "Set clock: " << TSCLOCK_GET_TIME_STRING() << std::endl;
    // we may have different threads to share the same clock while backtesting a trading strategy
    // we may only tune the clock time when all the threads are ready
    // we firest set the clock untunable by counting the number
    // following is an example to show 3 threads ask the clock to wait
    TSCLOCK_SET_ENABLE_TO_TUNE(false);
    TSCLOCK_SET_ENABLE_TO_TUNE(false);
    TSCLOCK_SET_ENABLE_TO_TUNE(false);

    // we need 3 enable before we can tune the clock
    TSCLOCK_SET_ENABLE_TO_TUNE(true);
    TSCLOCK_ADD_SEC(1); // fail to add
    std::cout << "Fail example: " << TSCLOCK_GET_TIME_STRING() << std::endl;

    TSCLOCK_SET_ENABLE_TO_TUNE(true);
    TSCLOCK_SET_ENABLE_TO_TUNE(true);
    TSCLOCK_ADD_SEC(1); // able to add
    std::cout << "Success example: " << TSCLOCK_GET_TIME_STRING() << std::endl;
}
// usage: ./NLClock
int main(int argc, char *argv[])
{
    StartStopDebug();
    SetClock();
    AddSecExample();
    AddSecExampleAdvance();

    return 0;
}
