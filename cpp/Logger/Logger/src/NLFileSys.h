#ifndef NLFILESYS_H
#define NLFILESYS_H
#include <string>
#include <vector>

class NLFileSys
{
 public:
    NLFileSys();
    ~NLFileSys();

    std::string GetFolderPath(const std::string& fullPath);
    std::string GetFileName(const std::string& fillPath);
    bool IsDirExist(const std::string& path);
    bool MakePath(const std::string& path);
    std::vector<std::string> ListDirectory(const std::string& path);
};

#endif
