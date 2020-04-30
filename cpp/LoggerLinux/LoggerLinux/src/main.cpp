#include <iostream>

#include "Logger.h"

// usage: ./Logger
class Foo
{
public:
    Foo() { LOGMSG_CLASS_NAME("Foo"); }
    ~Foo() {}

    void PrintLog()
    {
        LOGMSG_MSG("Multi thread function--------------\n");
        LOGMSG_DBG("Log inside class\n");
        LOGMSG_WRN("Log inside class\n");
        LOGMSG_MSG("Log inside class\n");
        LOGMSG_ERR("Log inside class\n");
        LOGMSG_MSG("\n");

        LOGMSG_MSG_S() << "Single thread function-----------------\n";
        LOGMSG_MSG_S() << "Log inside class\n";
        LOGMSG_DBG_S() << "Log inside class\n";
        LOGMSG_WRN_S() << "Log inside class\n";
        LOGMSG_ERR_S() << "Log inside class\n";
    }
};
int main (int argc, char *argv[])
{
    Logger::LoggerConfig config;
    config.logLevel = Logger::LogLevel::DEBUG;
    config.logPath = "./tempLog";
    config.fileSize = 0;
    config.fileSizeLimit = 4 * 1024 * 1024; // 4 MByte
    config.isToConsole = true;
    config.isToFile = true;

    LOGMSG_INIT(config);
    LOGMSG_MSG_C("Multi thread function--------------\n");
    LOGMSG_DBG_C("Log outside class\n");
    LOGMSG_WRN_C("Log outside class\n");
    LOGMSG_MSG_C("Log outside class\n");
    LOGMSG_ERR_C("Log outside class\n");
    LOGMSG_MSG_C("\n");

    LOGMSG_MSG_S_C() << "Single thread function-----------------\n";
    LOGMSG_MSG_S_C() << "Log outside class\n";
    LOGMSG_DBG_S_C() << "Log outside class\n";
    LOGMSG_WRN_S_C() << "Log outside class\n";
    LOGMSG_ERR_S_C() << "Log outside class\n";

    Foo xx;
    xx.PrintLog();
    return 0;
}
