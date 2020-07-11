#ifndef TOOLS_H
#define TOOLS_H
#include <string>
#include <vector>
#include <sys/stat.h> // stat
#include <errno.h>    // errno, ENOENT, EEXIST

#if defined(WIN32)
#include <direct.h>   // _mkdir
#endif

namespace Utility
{
    bool IsNumber(const std::string& s);
    std::vector<std::string> SplitString(const std::string& s, const char delim);
    bool IsBigEndian();
    int ReadFileToArray(const std::string& fileName, std::vector<unsigned char>& data);
    bool ReplaceSubstring(std::string& str, const std::string& from, const std::string& to);
    void ReplaceAllSubstring(std::string& str, const std::string& from, const std::string& to);
    std::string GetFolderPath(const std::string& fullPath);
    std::string GetFileName(const std::string& fillPath);
    bool IsDirExist(const std::string& path);
    bool MakePath(const std::string& path);
    std::pair<double, double> GetRunningMeanVariance(const std::vector<double>& vec);
};
#endif
