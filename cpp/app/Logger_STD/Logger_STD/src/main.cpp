#include <iostream>
#include <thread>
#include "Logger.h"

void Worker001()
{
    for (int i = 0; i < 100; i++)
        LOGMSG_MSG_S_C() << "New Hello" << ": " << i << std::endl;
}

void Worker002()
{
    for (int i = 0; i < 100; i++)
        LOGMSG_MSG_S_C() << "New Hello" << ": " << i << std::endl;
}

int main(int argc, char* argv[])
{
    Logger::LoggerConfig config;
    config.logLevel = Logger::LogLevel::WARN;
    config.logPath = "./LogFiles";
    config.fileSize = 0;
    config.fileSizeLimit = 4 * 1024 * 1024; // 4 MByte
    config.isToConsole = true;
    config.isToFile = true;
    LOGMSG_INIT(config);

    std::thread th001(Worker001);
    std::thread th002(Worker002);

    th001.join();
    th002.join();

    return 0;
}
