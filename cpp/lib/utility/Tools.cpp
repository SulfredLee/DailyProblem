#include "Tools.h"

#include <sstream>
#include <algorithm>

#include <stdio.h>

bool Utility::IsNumber(const std::string& s)
{
    if (s.empty()) return false;
    if (s[0] == '-')
        return std::find_if(s.begin() + 1, s.end(), [](char c){return !std::isdigit(c) && c != '.';}) == s.end();
    else
        return std::find_if(s.begin(), s.end(), [](char c){return !std::isdigit(c) && c != '.';}) == s.end();
}

std::vector<std::string> Utility::SplitString(const std::string& s, const char delim)
{
    std::vector<std::string> elems;
    std::stringstream ss(s);
    std::string item;
    while (std::getline(ss, item, delim))
    {
        elems.push_back(item);
    }
    return elems;
}

bool Utility::IsBigEndian()
{
    union
    {
        uint32_t i;
        char c[4];
    } bint = {0x01020304};

    return bint.c[0] == 1;
}

int Utility::ReadFileToArray(const std::string& fileName, std::vector<unsigned char>& data)
{
    // Reading size of file
    FILE * file = fopen(fileName.c_str(), "rb");
    if (file == NULL)  { throw "cannot open file " + fileName; return 0; };
    fseek(file, 0, SEEK_END);
    long int size = ftell(file);
    fclose(file);

    // Reading data to array of unsigned chars
    file = fopen(fileName.c_str(), "rb");
    data.resize(size);
    int bytes_read = fread(&(data[0]), sizeof(unsigned char), size, file);
    fclose(file);
    if (bytes_read != size)
    {
        data.clear();
        throw "cannot read data";
        return 0;
    }
    return bytes_read;
}

bool Utility::ReplaceSubstring(std::string& str, const std::string& from, const std::string& to)
{
    size_t start_pos = str.find(from);
    if(start_pos == std::string::npos)
        return false;
    str.replace(start_pos, from.length(), to);
    return true;
}

void Utility::ReplaceAllSubstring(std::string& str, const std::string& from, const std::string& to)
{
    if(from.empty())
        return;
    size_t start_pos = 0;
    while((start_pos = str.find(from, start_pos)) != std::string::npos)
    {
        str.replace(start_pos, from.length(), to);
        start_pos += to.length(); // In case 'to' contains 'from', like replacing 'x' with 'yx'
    }
}

std::string Utility::GetFolderPath(const std::string& fullPath)
{
    size_t found = fullPath.find_last_of("/\\");
    return fullPath.substr(0, found);
}

std::string Utility::GetFileName(const std::string& fullPath)
{
    size_t found = fullPath.find_last_of("/\\");
    return fullPath.substr(found + 1);
}

bool Utility::IsDirExist(const std::string& path)
{
#if defined(WIN32)
    struct _stat info;
    if (_stat(path.c_str(), &info) != 0)
    {
        return false;
    }
    return (info.st_mode & _S_IFDIR) != 0;
#else
    struct stat info;
    if (stat(path.c_str(), &info) != 0)
    {
        return false;
    }
    return (info.st_mode & S_IFDIR) != 0;
#endif
}

bool Utility::MakePath(const std::string& path)
{
#if defined(WIN32)
    int ret = _mkdir(path.c_str());
#else
    mode_t mode = 0755;
    int ret = mkdir(path.c_str(), mode);
#endif
    if (ret == 0)
        return true;

    switch (errno)
    {
    case ENOENT:
        // parent didn't exist, try to create it
        {
            size_t pos = path.find_last_of('/');
            if (pos == std::string::npos)
#if defined(WIN32)
                pos = path.find_last_of('\\');
            if (pos == std::string::npos)
#endif
                return false;
            if (!MakePath( path.substr(0, pos) ))
                return false;
        }
        // now, try to create again
#if defined(WIN32)
        return 0 == _mkdir(path.c_str());
#else
        return 0 == mkdir(path.c_str(), mode);
#endif

    case EEXIST:
        // done!
        return IsDirExist(path);

    default:
        return false;
    }
}

std::pair<double, double> Utility::GetRunningMeanVariance(const std::vector<double>& vec)
{
    double mean = 0, M2 = 0, variance = 0;

    size_t n = vec.size();
    for(size_t i = 0; i < n; ++i)
    {
        double delta = vec[i] - mean;
        mean += delta / (i + 1);
        M2 += delta * (vec[i] - mean);
        variance = M2 / (i + 1);
        if (i >= 2)
        {
            // <-- You can use the running mean and variance here
        }
    }

    return std::make_pair(mean, variance);
}
