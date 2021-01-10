import json

from Modules.ConfigReader.ConfigReaderBase import *

class JsonConfigReader(ConfigReaderBase):
    def __init__(self):
        pass

    # override
    def ReadFrom(self, srcName: str):
        resultConfig = ConfigData()
        with open(srcName) as read_file:
            data = json.load(read_file)

            # handle main project name
            resultConfig.MainProjectName = data["Main Project Name"]

            # handle sub project info
            for subPro in data["Sub Project List"]:
                tempData = SubProjectConfig()
                tempData.ProjectName = subPro["Project Name"]

                for lib in subPro["Libraries"]:
                    tempLibConfig = LibConfig()
                    tempLibConfig.LibName = lib["LibName"]
                    tempLibConfig.LibType = lib["LibType"]

                    tempData.LibList.append(tempLibConfig)

                tempData.DependsOnList = subPro["Depends On"]

                resultConfig.SubProjectList.append(tempData)

        return resultConfig
