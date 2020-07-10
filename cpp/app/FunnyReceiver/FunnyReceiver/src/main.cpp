#include <iostream>
#include <string>
#include "FunServer.h"
#include "FunReceiver.h"
#include "Logger.h"

int main(int argc, char* argv[])
{
    // Logger ready
    Logger::LoggerConfig logConfig;
    logConfig.logLevel = Logger::LogLevel::WARN;
    logConfig.logPath = ".";
    logConfig.fileSize = 0;
    logConfig.fileSizeLimit = 4 * 1024 * 1024; // 4 MByte
    logConfig.isToConsole = true;
    logConfig.isToFile = false;

    LOGMSG_INIT(logConfig);

    // dirty method for config input
    int maxMessageCount = 10;
    std::string tcpIP = "127.0.0.1"; short tcpPort = 7788;
    std::string udpIP = "127.0.0.1"; short udpPort = 7789;
    std::string udpClientIP = "127.0.0.1"; short udpClientPort = 8899;

    // server ready
    FunServer server;
    server.InitComponent(tcpIP, tcpPort, udpIP, udpPort, maxMessageCount);
    server.Start();

    // client ready
    FunReceiver receiver;
    receiver.InitComponent(tcpIP, tcpPort, udpIP, udpPort, udpClientIP, udpClientPort, maxMessageCount);
    receiver.Start();

    // wait until end
    while (true)
        std::this_thread::sleep_for(std::chrono::milliseconds(500));


    return 0;
}
