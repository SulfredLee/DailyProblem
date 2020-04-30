#include "NLFileSys.h"
#include "Logger.h"

#include <sys/types.h>
#include <sys/stat.h>

#include <string.h>
#include <dirent.h>

NLFileSys::NLFileSys()
{
}

NLFileSys::~NLFileSys()
{
}
std::string NLFileSys::GetFolderPath(const std::string& fullPath)
{
    size_t found = fullPath.find_last_of("/\\");
    return fullPath.substr(0, found);
}

std::string NLFileSys::GetFileName(const std::string& fullPath)
{
    size_t found = fullPath.find_last_of("/\\");
    return fullPath.substr(found + 1);
}

bool NLFileSys::IsDirExist(const std::string& path)
{
    struct stat info;
    if (stat(path.c_str(), &info) != 0)
    {
        return false;
    }
    return (info.st_mode & S_IFDIR) != 0;
}

bool NLFileSys::MakePath(const std::string& path)
{
    mode_t mode = 0755;
    int ret = mkdir(path.c_str(), mode);

    if (ret == 0)
        return true;

    switch (errno)
    {
        case ENOENT:
            // parent didn't exist, try to create it
            {
                size_t pos = path.find_last_of('/');
                if (pos == std::string::npos)
                    return false;
                if (!MakePath( path.substr(0, pos) ))
                    return false;
            }
            // now, try to create again
            return 0 == mkdir(path.c_str(), mode);

        case EEXIST:
            // done!
            return IsDirExist(path);

        default:
            return false;
    }
}

std::vector<std::string> NLFileSys::ListDirectory(const std::string& path)
{
    std::vector<std::string> result;

    DIR *dir;
    struct dirent *ent;
    if ((dir = opendir (path.c_str())) != NULL)
    {
        /* print all the files and directories within directory */
        while ((ent = readdir (dir)) != NULL)
        {
            if (strcmp(ent->d_name, ".") == 0 || strcmp(ent->d_name, "..") == 0)
                continue;
            result.push_back(ent->d_name);
        }
        closedir (dir);
    }
    else
    {
        LOGMSG_ERR_S() << "Could not open directory " << path << "\n";
        return std::vector<std::string>();
    }

    return result;
}
