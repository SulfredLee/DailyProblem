#ifndef LOGGER_H
#define LOGGER_H
#include <string>
#include <fstream>
#include <sstream>
#include <iostream>
#include <map>
#include <thread>

#include <unistd.h>
#include <sys/syscall.h>
#include <sys/time.h>
#include "DefaultMutex.h"
// using endl_type = decltype( std::endl ); //This is the key: std::endl is a template function, and this is the signature of that function (For std::ostream).
class Logger
{
 public:
    enum class LogLevel { DEBUG, WARN, INFO, ERR };
    struct LoggerConfig
    {
    public:
        LoggerConfig()
        {
            logLevel = Logger::LogLevel::WARN;
            logPath = ".";
            fileSize = 0;
            fileSizeLimit = 4 * 1024 * 1024; // 4 MByte
            isToConsole = true;
            isToFile = true;
        };
        ~LoggerConfig() {};
    public:
        Logger::LogLevel logLevel;
        std::string logPath;
        std::string logFilePathName;
        int fileSize;
        int fileSizeLimit;
        bool isToConsole;
        bool isToFile;
    };
 public:
    ~Logger();

    static Logger& GetInstance();
    static Logger& GetInstance_ResetSS(LogLevel logLevel, void *logObject, std::string functionName, int lineNumber);
    static std::string GetFileName(const std::string& fillPath);

    void InitComponent(const LoggerConfig& config);
    LoggerConfig GetConfig();
    void Log(LogLevel logLevel, const char* format, ...);
    void AddClassName(std::string className, void* object);
    void ResetSS(LogLevel logLevel, void *logObject, const std::string& functionName, int lineNumber);
    std::string GetClassName(void* object, std::string prettyFunction);
    // Logger& operator<< (endl_type endl)
    // {
    //     m_SS << endl;
    //     return *this;
    // }
    template<typename T>
        Logger& operator<< (const T& data)
    {
#ifdef Use_Linux_Lock
        DefaultLock lock(m_DefaultMutex);
#elif Use_Windows_Lock
#elif Use_Std_Lock
        std::lock_guard<std::mutex> lock(m_mutex);
#endif

        if (m_oneTimeLevel < m_config.logLevel)
        {
            return *this;
        }

        std::stringstream ss;
        ss << data;
        m_config.fileSize += ss.str().length();

        if (m_config.isToFile && OpenLogFile())
        {
            m_outFH << ss.str();
        }

        if (m_config.isToConsole)
        {
            std::cout << ss.str();
        }

        return *this;
    }
 private:
    LoggerConfig m_config;
    std::ofstream m_outFH;
    LogLevel m_oneTimeLevel;
    DefaultMutex m_DefaultMutex;
    std::map<void*, std::string> m_classNameMap; // key: object address, object class name
 private:
    Logger();
    Logger(const Logger&) = delete;
    Logger(const Logger&&) = delete;
    Logger& operator=(const Logger&) = delete;
    Logger& operator=(const Logger&&) = delete;

    std::string GetCurrentTime();
    std::string GetLogLevelName(LogLevel logLevel);
    std::string _GetClassName(const std::string& prettyFunction);
    bool OpenLogFile();
    void LogImplement(char dest[], int size, LogLevel logLevel, bool useTimeStamp, bool printLogLocation, void *logObject);
};

#define __LOGMSG(level, ...)                                            \
    do{                                                                 \
        char buffer[5120];                                              \
        snprintf(buffer, sizeof(buffer), __VA_ARGS__);                  \
        Logger::GetInstance().Log(level, "%25s::%25s:%6d,%6d,%s", Logger::GetInstance().GetClassName(this, __PRETTY_FUNCTION__).c_str(), __FUNCTION__, __LINE__, syscall(SYS_gettid), buffer); \
    }while(0)

#define __LOGMSG_C(level, ...)                                          \
    do{                                                                 \
        char buffer[5120];                                              \
        snprintf(buffer, sizeof(buffer), __VA_ARGS__);                  \
        Logger::GetInstance().Log(level, "%25s:%6d,%6d,%s", __FUNCTION__, __LINE__, syscall(SYS_gettid), buffer); \
    }while(0)

#define LOGMSG_DBG(...) __LOGMSG(Logger::LogLevel::DEBUG, __VA_ARGS__)
#define LOGMSG_MSG(...)  __LOGMSG(Logger::LogLevel::INFO, __VA_ARGS__)
#define LOGMSG_WRN(...)  __LOGMSG(Logger::LogLevel::WARN, __VA_ARGS__)
#define LOGMSG_ERR(...) __LOGMSG(Logger::LogLevel::ERR, __VA_ARGS__)
#define LOGMSG_DBG_C(...) __LOGMSG_C(Logger::LogLevel::DEBUG, __VA_ARGS__)
#define LOGMSG_MSG_C(...)  __LOGMSG_C(Logger::LogLevel::INFO, __VA_ARGS__)
#define LOGMSG_WRN_C(...)  __LOGMSG_C(Logger::LogLevel::WARN, __VA_ARGS__)
#define LOGMSG_ERR_C(...) __LOGMSG_C(Logger::LogLevel::ERR, __VA_ARGS__)
#define LOGMSG_DBG_S() Logger::GetInstance_ResetSS(Logger::LogLevel::DEBUG, this, __FUNCTION__, __LINE__)
#define LOGMSG_MSG_S() Logger::GetInstance_ResetSS(Logger::LogLevel::INFO, this, __FUNCTION__, __LINE__)
#define LOGMSG_WRN_S() Logger::GetInstance_ResetSS(Logger::LogLevel::WARN, this, __FUNCTION__, __LINE__)
#define LOGMSG_ERR_S() Logger::GetInstance_ResetSS(Logger::LogLevel::ERR, this, __FUNCTION__, __LINE__)
#define LOGMSG_DBG_S_C() Logger::GetInstance_ResetSS(Logger::LogLevel::DEBUG, NULL, __FUNCTION__, __LINE__)
#define LOGMSG_MSG_S_C() Logger::GetInstance_ResetSS(Logger::LogLevel::INFO, NULL, __FUNCTION__, __LINE__)
#define LOGMSG_WRN_S_C() Logger::GetInstance_ResetSS(Logger::LogLevel::WARN, NULL, __FUNCTION__, __LINE__)
#define LOGMSG_ERR_S_C() Logger::GetInstance_ResetSS(Logger::LogLevel::ERR, NULL, __FUNCTION__, __LINE__)
#define LOGMSG_CLASS_NAME(className) Logger::GetInstance().AddClassName(className, this)
#define LOGMSG_INIT(config) Logger::GetInstance().InitComponent(config)

#endif
