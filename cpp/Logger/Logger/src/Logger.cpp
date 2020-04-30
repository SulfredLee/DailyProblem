#include "Logger.h"

#include <string>
#include <sstream>
#include <fstream>
#include <iostream>
#include <iomanip>
#if defined(_MSC_VER) && (_MSC_VER <= 1926)
#include <experimental/filesystem>
#else
#include "NLFileSys.h"
#endif

#include <stdarg.h>     /* va_list, va_start, va_arg, va_end */
#include <string.h>
#include <stdio.h>
#include <time.h>

#ifdef WIN32
int gettimeofday(struct timeval *tp, void *tzp)
{
    time_t clock;
    struct tm tm;
    SYSTEMTIME wtm;
    GetLocalTime(&wtm);
    tm.tm_year = wtm.wYear - 1900;
    tm.tm_mon = wtm.wMonth - 1;
    tm.tm_mday = wtm.wDay;
    tm.tm_hour = wtm.wHour;
    tm.tm_min = wtm.wMinute;
    tm.tm_sec = wtm.wSecond;
    tm.tm_isdst = -1;
    clock = mktime(&tm);
    tp->tv_sec = static_cast<long>(clock);
    tp->tv_usec = wtm.wMilliseconds * 1000;
    return (0);
}
std::thread::id GetCurrentThreadID_()
{
    return std::this_thread::get_id();
}
#else
int GetCurrentThreadID_()
{
    return syscall(SYS_gettid);
}
#endif

Logger::Logger()
{
    // handle default value
    m_config.logLevel = Logger::LogLevel::INFO;
    m_config.logPath = ".";
    m_config.fileSize = 0;
    m_config.fileSizeLimit = 4 * 1024 * 1024; // 4 MByte
    m_config.isToConsole = false;
    m_config.isToFile = true;
}

Logger::~Logger()
{}

Logger& Logger::GetInstance()
{
    static Logger instance;
    return instance;
}

Logger& Logger::GetInstance_ResetSS(LogLevel logLevel, void *logObject, std::string functionName, int lineNumber)
{
    Logger& logger = GetInstance();
    logger.ResetSS(logLevel, logObject, functionName, lineNumber);
    return logger;
}

void Logger::InitComponent(const Logger::LoggerConfig& config)
{
    std::lock_guard<std::mutex> lock(m_mutex);
    m_config = config;
}

Logger::LoggerConfig Logger::GetConfig()
{
    std::lock_guard<std::mutex> lock(m_mutex);
    return m_config;
}

void Logger::Log(LogLevel logLevel, const char* format, ...)
{
    std::lock_guard<std::mutex> lock(m_mutex);
    if (logLevel < m_config.logLevel)
    {
        return;
    }
    char dest[5120]; // 5 KByte
    int destLen = sizeof(dest);
    memset(dest, 0, destLen);

    va_list	args;
    va_start(args, format);
    vsnprintf(dest, destLen, format, args);
    va_end(args);

    std::stringstream ss;
    ss << GetCurrentTime() << " [" << GetLogLevelName(logLevel) << "] " << dest;
    m_config.fileSize += ss.str().length();

    if (m_config.isToFile && OpenLogFile())
    {
        m_outFH << ss.str();
    }

    if (m_config.isToConsole)
    {
        std::cout << ss.str();
    }
}

void Logger::AddClassName(std::string className, void* object)
{
    m_classNameMap.insert(std::make_pair(object, className));
}

void Logger::ResetSS(LogLevel logLevel, void *logObject, const std::string& functionName, int lineNumber)
{
    std::lock_guard<std::mutex> lock(m_mutex);

    m_oneTimeLevel = logLevel;
    if (logLevel < m_config.logLevel)
    {
        return;
    }

    std::stringstream ss;
    ss << GetCurrentTime() << " [" << GetLogLevelName(logLevel) << "] ";
    if (logObject)
        ss << std::setw(25) << std::setfill(' ') << Logger::GetInstance().GetClassName(logObject, __PRETTY_FUNCTION__) << "::";
    ss << std::setw(25) << std::setfill(' ') << functionName << ":"
       << std::setw(6) << std::setfill(' ') << lineNumber << ","
       << std::setw(6) << std::setfill(' ') << GetCurrentThreadID_() << ",";
    m_config.fileSize += ss.str().length();

    if (m_config.isToFile && OpenLogFile())
    {
        m_outFH << ss.str();
    }

    if (m_config.isToConsole)
    {
        std::cout << ss.str();
    }
}

std::string Logger::GetClassName(void* object, std::string prettyFunction)
{
    std::map<void*, std::string>::iterator it = m_classNameMap.find(object);
    if (it != m_classNameMap.end())
    {
        return it->second;
    }
    else
    {
        return _GetClassName(prettyFunction);
    }
}

std::string Logger::GetCurrentTime()
{
    timeval curTime;
    gettimeofday(&curTime, NULL);
    int milli = curTime.tv_usec / 1000;

    char buffer[80];
#ifdef WIN32
    tm tempTM;
    time_t rawTime = curTime.tv_sec;
    localtime_s(&tempTM, &rawTime);
    strftime(buffer, 80, "%Y%m%d_%H%M%S", &tempTM);
#else
    strftime(buffer, 80, "%Y%m%d_%H%M%S", localtime(&curTime.tv_sec));
#endif

    char currentTime[84] = "";
    sprintf(currentTime, "%s_%03d", buffer, milli);
    // time compare example
    // struct timeval tval_before, tval_after, tval_result;
    // gettimeofday(&tval_before, NULL);
    // // Some code you want to time, for example:
    // sleep(1);
    // gettimeofday(&tval_after, NULL);
    // timersub(&tval_after, &tval_before, &tval_result);
    // printf("Time elapsed: %ld.%06ld\n", (long int)tval_result.tv_sec, (long int)tval_result.tv_usec);
    return std::string(currentTime);
}

std::string Logger::GetLogLevelName(LogLevel logLevel)
{
    switch (logLevel)
    {
        case Logger::LogLevel::DEBUG:
            return "DBG";
        case Logger::LogLevel::WARN:
            return "WRN";
        case Logger::LogLevel::INFO:
            return "MSG";
        case Logger::LogLevel::ERR:
            return "ERR";
        default:
            return std::string();
    }
}

bool Logger::OpenLogFile()
{
    if (m_outFH.is_open() && m_config.fileSize < m_config.fileSizeLimit)
    {
        return true;
    }
    else if (m_outFH.is_open())
    {
        m_outFH.close();
        m_config.fileSize = 0;
    }
    else
    {
        m_config.fileSize = 0;
    }

#if defined(_MSC_VER) && (_MSC_VER <= 1926)
    if (!std::experimental::filesystem::exists(m_config.logPath))
        std::experimental::filesystem::create_directories(m_config.logPath);
#else
    NLFileSys fileSys;
    if (!fileSys.IsDirExist(m_config.logPath))
        fileSys.MakePath(m_config.logPath);

#endif
    m_config.logFilePathName = m_config.logPath + "/" + GetCurrentTime() + ".log";
    m_outFH.open(m_config.logFilePathName, std::ios::out);
    if (m_outFH.is_open())
    {
        return true;
    }
    else
    {
        m_config.logFilePathName = "./" + GetCurrentTime() + ".log";
        m_outFH.open(m_config.logFilePathName, std::ios::out);
        if (m_outFH.is_open())
        {
            return true;
        }
        else
        {
            return false;
        }
    }
}

void Logger::LogImplement(char dest[], int size, LogLevel logLevel, bool useTimeStamp, bool printLogLocation, void *logObject)
{
    std::stringstream ss;
    if (useTimeStamp)
        ss << GetCurrentTime() << " [" << GetLogLevelName(logLevel) << "] ";
    if (printLogLocation && logObject)
        ss << std::setw(25) << std::setfill(' ') << Logger::GetInstance().GetClassName(logObject, __PRETTY_FUNCTION__) << "::";
    if (printLogLocation)
        ss << std::setw(25) << std::setfill(' ') << __FUNCTION__ << ":"
           << std::setw(6) << std::setfill(' ') << __LINE__ << ","
           << std::setw(6) << std::setfill(' ') << GetCurrentThreadID_() << ",";
    if (size != 0)
        ss << dest;
    m_config.fileSize += ss.str().length();

    if (m_config.isToFile && OpenLogFile())
    {
        m_outFH << ss.str();
    }

    if (m_config.isToConsole)
    {
        std::cout << ss.str();
    }
}

std::string Logger::GetFileName(const std::string& fullPath)
{
    size_t found = fullPath.find_last_of("/\\");
    return fullPath.substr(found + 1);
}

std::string Logger::_GetClassName(const std::string& prettyFunction)
{
    size_t colons = prettyFunction.find("::");
    if (colons == std::string::npos)
        return "::";
    size_t begin = prettyFunction.substr(0, colons).rfind(" ") + 1;
    size_t end = colons - begin;

    return prettyFunction.substr(begin, end);
}
