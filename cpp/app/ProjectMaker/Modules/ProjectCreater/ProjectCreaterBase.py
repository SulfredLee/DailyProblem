import os
import errno

from Business.ConfigData import *

class ProjectCreaterBase(object):
    def __init__(self, config: ConfigData):
        self._config = config
        self._ProjectFolderName = "Projects"
        self._DebugFolderName = "Debug"
        self._ReleaseFolderName = "Release"
        self._InstallFolderName = "Install"

    # pure virtual
    def GenerateProject(self):
        raise NotImplementedError
