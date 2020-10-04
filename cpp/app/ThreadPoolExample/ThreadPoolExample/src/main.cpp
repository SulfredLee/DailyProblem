#include <iostream>
#include <chrono>
#include "ThreadPool.h"
#include "Logger.h"

void Print001(const int& inInt)
{
    LOGMSG_MSG_S_C() << "Number: " << inInt << std::endl;
}

int main(int argc, char* argv[])
{
    ThreadPool<int> pool001;
    pool001.InitComponent(3, std::bind(Print001, std::placeholders::_1));
    pool001.StartPool();

    for (int i = 0; i < 100; i++)
        pool001.PushJob(i);

    LOGMSG_MSG_S_C() << "Before sleep" << std::endl;
    using namespace std::chrono_literals;
    std::this_thread::sleep_for(5s);
    LOGMSG_MSG_S_C() << "After sleep" << std::endl;

    return 0;
}
