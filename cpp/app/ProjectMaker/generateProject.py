from Modules.ConfigReader.JsonConfigReader import *
from Modules.ProjectCreater.CppCMakeCreater import *

if __name__ == "__main__":
    configReader = JsonConfigReader()
    config = configReader.ReadFrom("projectStructure.json")

    print("Going to create project: {}".format(config.MainProjectName))
    creater = CppCMakeCreater(config)
    creater.GenerateProject()
