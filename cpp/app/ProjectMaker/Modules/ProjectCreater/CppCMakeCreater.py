from Modules.ProjectCreater.ProjectCreaterBase import *

class CppCMakeCreater(ProjectCreaterBase):
    def __init__(self, config: ConfigData):
        super().__init__(config)

    # override
    def GenerateProject(self):
        try:
            self.__Handle_1_Layer()
            self.__Handle_2_Layer() # debug release install root
            self.__Handle_3_Layer() # project root
            self.__Handle_4_Layer() # inside subProject
        except OSError as e:
            if e.errno != errno.EEXIST:
                print("OSError: {}".format(e))
                print("Stop process")
                raise e

    def __Handle_1_Layer(self):
        os.makedirs(self._config.MainProjectName)

    def __Handle_2_Layer(self):
        os.makedirs(self._config.MainProjectName + "/" + self._DebugFolderName)
        os.makedirs(self._config.MainProjectName + "/" + self._ReleaseFolderName)
        os.makedirs(self._config.MainProjectName + "/" + self._InstallFolderName)
        os.makedirs(self._config.MainProjectName + "/" + self._ProjectFolderName)

    def __Handle_3_Layer(self):
        # handle debug folder
        with open(self._config.MainProjectName + "/Debug/readme.txt", 'w') as oFH:
            oFH.write("# Usage:\n")
            oFH.write("cmake -G Ninja ../{} -DCMAKE_BUILD_TYPE=Debug -DCMAKE_INSTALL_PREFIX=../{}\n".format(self._ProjectFolderName, self._InstallFolderName))
            oFH.write("ninja\n")

        # handle release folder
        with open(self._config.MainProjectName + "/Release/readme.txt", 'w') as oFH:
            oFH.write("# Usage:\n")
            oFH.write("cmake -G Ninja ../{} -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=../{}\n".format(self._ProjectFolderName, self._InstallFolderName))
            oFH.write("ninja\n")

        self.__Handle_3_Layer_Projects()

    def __Handle_3_Layer_Projects(self):
        # handle root cmake file
        with open(self._config.MainProjectName + "/{}/CMakeLists.txt".format(self._ProjectFolderName), 'w') as oFH:
            oFH.write(self.__GetRootCMakeFile())
        # handle projects
        for subProject in self._config.SubProjectList:
            # handle cmake files
            with open(self._config.MainProjectName + "/{}/{}.cmake".format(self._ProjectFolderName, subProject.ProjectName), 'w') as oFH:
                oFH.write(self.__GetRootSubProjectCMakeFile(subProject.ProjectName))
            # handle project folder
            os.makedirs(self._config.MainProjectName + "/" + self._ProjectFolderName + "/" + subProject.ProjectName)

    def __Handle_4_Layer(self):
        for subProject in self._config.SubProjectList:
            self.__Handle_SubProject(self._config.MainProjectName + "/" + self._ProjectFolderName + "/" + subProject.ProjectName, subProject)

    def __Handle_SubProject(self, rootPath: str, subProject: SubProjectConfig):
        # handle folders
        os.makedirs(rootPath + "/src")
        os.makedirs(rootPath + "/lib")
        # handle cmake file
        with open(rootPath + "/CMakeLists.txt", 'w') as oFH:
            oFH.write(self.__GetProjectRootCMakeFile(subProject))

        # handle src cmake file
        with open(rootPath + "/src/CMakeLists.txt", 'w') as oFH:
            oFH.write(self.__GetProjectSrcCMakeFile(subProject.ProjectName))
        # handle src main.cpp
        with open(rootPath + "/src/main.cpp", 'w') as oFH:
            oFH.write(self.__GetMainCpp())

        # handle lib folder
        self.__Handle_SubProject_Lib(rootPath + "/lib", subProject)

    def __GetRootCMakeFile(self) -> str:
        content = ["cmake_minimum_required (VERSION 3.8.2)"
                   , ""
                   , "# build a CPack driven installer package"
                   , "include (InstallRequiredSystemLibraries)"
                   , "include (CPack)"
                   , "include (ExternalProject)"
                   , ""
                   , "# Maps to a solution filed (*.sln). The solution will"
                   , "# have all targets (exe, lib, dll) as projects (.vcproj)"
                   , "project({})".format(self._config.MainProjectName)
                   , ""
        ]
        content.extend(self.__GetCommonCMakeProjectSetting())
        content.append("# Add External Project")
        for subProject in self._config.SubProjectList:
            content.append("include ({}.cmake)".format(subProject.ProjectName))
        content.append("")
        content.append("# Handle dependencies")
        isHasDependency = False
        for subProject in self._config.SubProjectList:
            if not len(subProject.DependsOnList) == 0:
                isHasDependency = True
                content.append("ExternalProject_Add_StepDependencies({} build)".format(subProject.ProjectName))

                for dependedProjectName in subProject.DependsOnList:
                    content.append("  {}".format(dependedProjectName))

                content.append("  )")
        if not isHasDependency:
            content.append("# ExternalProject_Add_StepDependencies(ProjectA build")
            content.append("#   ProjectB")
            content.append("#   )")

        content.append("")
        content.append("")
        content.append("# Problem 001")
        content.append("#        /usr/bin/ld: ... undefined reference to symbol 'pthread_rwlock_wrlock@@GLIBC_2.2.5'")

        return self.__ConvertListToNewLineString(content)

    def __GetRootSubProjectCMakeFile(self, projectName: str) -> str:
        content = ["include (ExternalProject)"
                   , ""
                   , "# Add External {}".format(projectName)
                   , "set ({} \"{}\")".format(projectName, projectName)
                   , "ExternalProject_Add ("
                   , "  ${" + projectName + "}"
                   , ""
                   , "  PREFIX " + self._ProjectFolderName + "/${" + projectName + "}"
                   , "  SOURCE_DIR ${" + "PROJECT_SOURCE_DIR}/${" + projectName + "}"
                   , ""
                   , "  BUILD_ALWAYS   ON"
                   , "  INSTALL_DIR    ${CMAKE_INSTALL_PREFIX}"
                   , ""
                   , "  CMAKE_CACHE_ARGS"
                   , "  -DBUILD_SHARED_LIBS:BOOL=ON"
                   , "  -DENABLE_STATIC_RUNTIME:BOOL=OFF"
                   , "  -DBUILD_EXAMPLES:BOOL=ON"
                   , "  -DCMAKE_BUILD_TYPE:STRING=${CMAKE_BUILD_TYPE}"
                   , "  -DCMAKE_INSTALL_PREFIX:PATH=<INSTALL_DIR>"
                   , ""
                   , "  BUILD_COMMAND ${CMAKE_COMMAND} --build <BINARY_DIR>"
                   , "  )"
        ]

        return self.__ConvertListToNewLineString(content)

    def __GetCommonCMakeProjectSetting(self) -> str:
        return ["# Turn on the ability to create folders to organize projects (.vcproj)"
                , "# It creates \"CMakePredefinedTargets\" folder by default and adds CMake"
                , "# defined projects like INSTALL.vcproj and ZERO_CHECK.vcproj"
                , "set_property(GLOBAL PROPERTY USE_FOLDERS ON)"
                , ""
                , "# Command to output information to the console"
                , "# Useful for displaying errors, warnings, and debugging"
                , "set(CMAKE_CXX_FLAGS \"-Wall -fPIC -std=c++2a -g\")"
                , "message(STATUS \"Root - cxx Flags: \" ${CMAKE_CXX_FLAGS})"
                , ""
                , "# Handle Preprocess Flags"
                , "if (UNIX)"
                , "  add_definitions(-DUNIX)"
                , "else ()"
                , "  add_definitions(-DWINDOWS -DWIN32 \"/EHsc\")"
                , "endif ()"
                , ""
                , "# Handle linux libraries"
                , "if (UNIX)"
                , "  find_package("
                , "    Threads) # include this package to fix problem 001"
                , "else ()"
                , "endif ()"
                , "message(STATUS \"Info - CMAKE_THREAD_LIBS_INIT: ${CMAKE_THREAD_LIBS_INIT}\")"
                , ""
        ]

    def __GetProjectRootCMakeFile(self, subProject: SubProjectConfig) -> str:
        content = ["cmake_minimum_required (VERSION 3.8.2)"
                   , ""
                   , "# build a CPack driven installer package"
                   , "include (InstallRequiredSystemLibraries)"
                   , "include (CPack)"
                   , ""
                   , "# Maps to a solution filed (*.sln). The solution will"
                   , "# have all targets (exe, lib, dll) as projects (.vcproj)"
                   , "project({})".format(subProject.ProjectName)
                   , ""
        ]
        content.extend(self.__GetCommonCMakeProjectSetting())
        content.append("# Sub-directories where more CMakeLists.txt exist")
        content.append("add_subdirectory(src)")
        if len(subProject.LibList) == 0:
            content.append("# add_subdirectory(lib)")
        else:
            content.append("add_subdirectory(lib)")

        return self.__ConvertListToNewLineString(content)

    def __ConvertListToNewLineString(self, content: list) -> str:
        # append newline and merge to one string
        resultString = ""
        for line in content:
            resultString += line + "\n"

        return resultString

    def __GetProjectSrcCMakeFile(self, projectName: str) -> str:
        content = ["set(targetName \"{}\")".format(projectName)
                   , "get_filename_component(folderName ${CMAKE_CURRENT_SOURCE_DIR} NAME)"
                   , "string(REPLACE \" \" \"_\" folderName ${folderName})"
                   , ""
                   , "set(CMAKE_CXX_FLAGS \"${CMAKE_CXX_FLAGS} -Wno-deprecated-declarations\")"
                   , ""
                   , "file(GLOB ${folderName}_inc"
                   , "  \"${CMAKE_CURRENT_SOURCE_DIR}/*.h\")"
                   , "file(GLOB ${folderName}_src"
                   , "  \"${CMAKE_CURRENT_SOURCE_DIR}/*.cpp\")"
                   , ""
                   , "include_directories("
                   , "  ${CMAKE_CURRENT_SOURCE_DIR}"
                   , "  )"
                   , "  # ${PROJECT_SOURCE_DIR}/../ProjectB/lib/PrintHelper"
                   , "  # ${PROJECT_SOURCE_DIR}/lib/utility"
                   , "  # ${libpng_INCLUDE_DIR}"
                   , "  # ${libbmp_INCLUDE_DIR})"
                   , ""
                   , "add_executable(${targetName} ${${folderName}_src})"
                   , ""
                   , "# target_link_libraries(${targetName}"
                   , "#   ${CMAKE_INSTALL_PREFIX}/lib/libPrintHelper.so"
                   , "#   ${CMAKE_THREAD_LIBS_INIT}"
                   , "#   utility"
                   , "#   ${libpng_LIBRARY_DIR}/libpng16.so"
                   , "#   ${libbmp_LIBRARY_DIR}/libbmp.so)"
                   , ""
                   , "# Creates a folder \"executables\" and adds target"
                   , "# project (*.vcproj) under it"
                   , "set_property(TARGET ${targetName} PROPERTY FOLDER \"executables\")"
                   , ""
                   , "# Adds logic to INSTALL.vcproj to copy *.exe to destination directory"
                   , "install (TARGETS ${targetName} DESTINATION bin)"
        ]
        return self.__ConvertListToNewLineString(content)

    def __GetMainCpp(self) -> str:
        content = ["#include <iostream>"
                   , ""
                   , "int main (int argc, char *argv[])"
                   , "{"
                   , "    return 0;"
                   , "}"
        ]
        return self.__ConvertListToNewLineString(content)

    def __GetProjectLibCMakeFile(self, libName: str) -> str:
        content = ["set(targetName \"{}\")".format(libName)
                   , "get_filename_component(folderName ${CMAKE_CURRENT_SOURCE_DIR} NAME)"
                   , "string(REPLACE \" \" \"_\" folderName ${folderName})"
                   , ""
                   , "file(GLOB ${folderName}_inc"
                   , "  \"${CMAKE_CURRENT_SOURCE_DIR}/*.h\")"
                   , "file(GLOB ${folderName}_src"
                   , "  \"${CMAKE_CURRENT_SOURCE_DIR}/*.cpp\")"
                   , ""
                   , "include_directories(${CMAKE_CURRENT_SOURCE_DIR}"
                   , "  ${Boost_INCLUDE_DIR})"
                   , ""
                   , "# state that this project is a library"
                   , "# add_library(${targetName} ${${folderName}_src}) # static library"
                   , "add_library(${targetName} SHARED ${${folderName}_src}) # dynamic library"
                   , "target_link_libraries(${targetName}"
                   , "  ${CMAKE_THREAD_LIBS_INIT})"
                   , ""
                   , "# Creates a folder \"libraries\" and adds target project (*.vcproj) under it"
                   , "set_property(TARGET ${targetName} PROPERTY FOLDER \"libraries\")"
                   , ""
                   , "# Adds logic to INSTALL.vcproj to copy *.a to destination directory"
                   , "install (TARGETS ${targetName} DESTINATION lib)"
                   , "install (FILES ${${folderName}_inc} DESTINATION include)"
        ]
        return self.__ConvertListToNewLineString(content)

    def __Handle_SubProject_Lib(self, rootPath: str, subProject: SubProjectConfig):
        # handle lib root cmake file
        with open(rootPath + "/CMakeLists.txt", 'w') as oFH:
            for libName in subProject.LibList:
                oFH.write("add_subdirectory({})\n".format(libName))

        # handle lib subfolders
        for libName in subProject.LibList:
            libFolderName = rootPath + "/{}".format(libName)
            os.makedirs(libFolderName)

            # handle cmake file
            with open(libFolderName + "/CMakeLists.txt", 'w') as oFH:
                oFH.write(self.__GetProjectLibCMakeFile(libName))
