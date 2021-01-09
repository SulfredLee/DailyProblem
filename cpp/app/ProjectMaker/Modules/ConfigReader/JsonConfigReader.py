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
                tempData.LibList = subPro["Libraries"]

                resultConfig.SubProjectList.append(tempData)

        return resultConfig
