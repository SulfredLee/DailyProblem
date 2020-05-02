#include <iostream>
#include <vector>

#include "Tools.h"

void IsNumberExample()
{
    std::cout << std::endl;
    std::cout << __FUNCTION__ << "-------------------" << std::endl;
    std::cout << Utility::IsNumber("9900") << std::endl;
    std::cout << Utility::IsNumber("99x00") << std::endl;
    std::cout << Utility::IsNumber("99.00") << std::endl;
    std::cout << Utility::IsNumber("99:00") << std::endl;
}
void SplitStringExample()
{
    std::cout << std::endl;
    std::cout << __FUNCTION__ << "-------------------" << std::endl;
    auto parts = Utility::SplitString("abd,cd,sfd,e", ',');
    for (const auto& part : parts)
    {
        std::cout << part << std::endl;
    }
}
void IsBigEndianExample()
{
    std::cout << std::endl;
    std::cout << __FUNCTION__ << "-------------------" << std::endl;
    std::cout << Utility::IsBigEndian() << std::endl;
}
void ReadFileToArrayExample()
{
    std::cout << std::endl;
    std::cout << __FUNCTION__ << "-------------------" << std::endl;
    std::vector<unsigned char> tempData;
    try
    {
        int readSize = Utility::ReadFileToArray("testing.txt", tempData);
        std::cout << "Read Size: " << readSize << std::endl;
    }
    catch (const std::string& err)
    {
        std::cout << err << std::endl;
    }
}
void ReplaceSubstringExample()
{
    std::cout << std::endl;
    std::cout << __FUNCTION__ << "-------------------" << std::endl;
    std::string strInput = "apple is orange and it is not an apple";
    Utility::ReplaceSubstring(strInput, "apple", "orange");
    std::cout << strInput << std::endl;
}
void ReplaceAllSubstringExample()
{
    std::cout << std::endl;
    std::cout << __FUNCTION__ << "-------------------" << std::endl;
    std::string strInput = "apple is orange and it is not an apple";
    Utility::ReplaceAllSubstring(strInput, "apple", "orange");
    std::cout << strInput << std::endl;
}
void GetFolderPathExample()
{
    std::cout << std::endl;
    std::cout << __FUNCTION__ << "-------------------" << std::endl;
    std::string strFolderPathLinux = "/Path/To/Your/File.txt";
    std::cout << "Linux example: " << Utility::GetFolderPath(strFolderPathLinux) << std::endl;
    std::string strFolderPathWindows = "C:\\Path\\To\\Your\\File.txt";
    std::cout << "Windows example: " << Utility::GetFolderPath(strFolderPathWindows) << std::endl;
}
void GetFileNameExample()
{
    std::cout << std::endl;
    std::cout << __FUNCTION__ << "-------------------" << std::endl;
    std::string strFolderPathLinux = "/Path/To/Your/File.txt";
    std::cout << "Linux example: " << Utility::GetFileName(strFolderPathLinux) << std::endl;
    std::string strFolderPathWindows = "C:\\Path\\To\\Your\\File.txt";
    std::cout << "Windows example: " << Utility::GetFileName(strFolderPathWindows) << std::endl;
}
void IsDirExistExample()
{
    std::cout << std::endl;
    std::cout << __FUNCTION__ << "-------------------" << std::endl;
    std::cout << "Linux example: " << Utility::IsDirExist("/Path/To/Your/Folder") << std::endl;
    std::cout << "Windows example: " << Utility::IsDirExist("C:\\Path\\To\\Your\\Folder") << std::endl;
}
void MakePathExample()
{
    std::cout << std::endl;
    std::cout << __FUNCTION__ << "-------------------" << std::endl;
    std::cout << "Create Path on linx: " << Utility::MakePath("./tempFolder") << std::endl;
}
int main(int argc, char *argv[])
{
    IsNumberExample();
    SplitStringExample();
    IsBigEndianExample();
    ReadFileToArrayExample();
    ReplaceSubstringExample();
    ReplaceAllSubstringExample();
    GetFolderPathExample();
    GetFileNameExample();
    IsDirExistExample();
    MakePathExample();
    return 0;
}
