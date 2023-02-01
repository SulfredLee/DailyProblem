content_st = """
import logging
from typing import List, Dict, Tuple

import sfdevtools.observability.log_helper as lh
from sfdevtools.devTools.SingletonDoubleChecked import SDC

class MainManager(SDC):
    def __init__(self):
        self.__logger: logging.Logger = None

    def init_component(self, logger: logging.Logger, bucket_name: str):
        self.__logger = logger

    def get_logger(self) -> logging.Logger:
        return self.__logger
"""
