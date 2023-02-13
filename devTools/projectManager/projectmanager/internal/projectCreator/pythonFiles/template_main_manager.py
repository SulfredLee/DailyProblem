content_st = """
import logging
from typing import List, Dict, Tuple

import sfdevtools.observability.log_helper as lh
from sfdevtools.devTools.SingletonDoubleChecked import SDC
import atexit

class MainManager(SDC):
    def __init__(self):
        self.__logger: logging.Logger = None

        atexit.register(self.__cleanup)

    def init_component(self, logger: logging.Logger):
        self.__logger = logger

    def get_logger(self) -> logging.Logger:
        return self.__logger

    def __cleanup(self):
        pass
"""
