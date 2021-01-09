from Business.ConfigData import *

class ConfigReaderBase(object):
    def __init__(self):
        pass

    # pure virtual
    def ReadFrom(self, srcName: str):
        raise NotImplementedError
