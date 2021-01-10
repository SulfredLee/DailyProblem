class LibConfig(object):
    def __init__(self):
        self.LibName = ""
        self.LibType = "" # type: share or static

class SubProjectConfig(object):
    def __init__(self):
        self.ProjectName = ""
        self.LibList = list() # list of LibConfig
        self.DependsOnList = list() # list of string

class ConfigData(object):
    def __init__(self):
        self.MainProjectName = ""
        self.SubProjectList = list() # List of SubProjectConfig
