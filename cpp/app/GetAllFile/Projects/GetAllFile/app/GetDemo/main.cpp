#include <iostream>
#include <vector>
#include <string>
#include <filesystem>

std::vector<std::string> GetFilesInFolder(const std::string& path, const std::string& ext)
{
    std::vector<std::string> result;

    for (const auto& file : std::filesystem::directory_iterator(path))
    {
        if (file.is_directory())
            std::cout << "Directory: " << file.path() << std::endl;
        else if (file.is_regular_file())
            std::cout << "Regular file: " << file.path() << std::endl;
        if (ext == file.path().filename().extension())
            result.emplace_back(file.path());
    }
    return result;
}

int main (int argc, char *argv[])
{
    std::string path = "./";

    for (const auto& csvFile : GetFilesInFolder(path, ".csv"))
        std::cout << "csv: " << csvFile << std::endl;


    return 0;
}
