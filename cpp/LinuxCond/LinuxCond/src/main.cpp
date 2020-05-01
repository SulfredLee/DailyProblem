#include <iostream>
#include <thread>
#include <chrono>

#include "LinuxCond.h"

LinuxCond cond;
void firstWorker()
{
    int count = 0;
    while (count++ < 5)
    {
        std::cout << "firstWorker say Hello" << std::endl;
        cond.Wait();
    }
}
void secondWorker()
{
    int count = 0;
    while (count++ < 5)
    {
        std::cout << "secondWorker say Hello" << std::endl;
        std::this_thread::sleep_for(std::chrono::seconds(1));
        cond.Signal();
    }
}
int main(int argc, char *argv[])
{
    std::thread worker1(firstWorker); worker1.detach();
    std::thread worker2(secondWorker); worker2.detach();

    int count = 0;
    while (count++ < 5)
    {
        std::this_thread::sleep_for(std::chrono::seconds(2));
    }

    return 0;
}
