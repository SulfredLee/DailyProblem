#include <iostream>
#include <thread>
#include <chrono>

#include "MSecTimer.h"

void Foo(int x)
{
    std::cout << "Hello from " << __FUNCTION__ << " " << x << std::endl;
}
int main(int argc, char *argv[])
{
    MSecTimer timer(1000, Foo, 10);
    timer.Start();
    int count = 0;
    while (count++ < 5)
    {
        std::this_thread::sleep_for(std::chrono::seconds(1));
    }
    timer.Stop();

    return 0;
}
