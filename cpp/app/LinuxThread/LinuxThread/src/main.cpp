#include <iostream>
#include <thread>
#include <chrono>

#include "ClassWithThread.h"
#include "Logger.h"

int main(int argc, char *argv[])
{
    Logger::LoggerConfig config;
    config.logLevel = Logger::LogLevel::DEBUG;
    config.logPath = ".";
    config.fileSize = 0;
    config.fileSizeLimit = 4 * 1024 * 1024; // 4 MByte
    config.isToConsole = true;
    config.isToFile = false;
    LOGMSG_INIT(config);

    Trader cc;
    cc.InitComponent();
    std::this_thread::sleep_for(std::chrono::seconds(1));

    return 0;
}
