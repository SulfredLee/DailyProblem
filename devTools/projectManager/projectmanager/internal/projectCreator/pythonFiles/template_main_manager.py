content_st = """
import logging
from typing import List, Dict, Tuple

import sfdevtools.observability.log_helper as lh
from sfdevtools.devTools.SingletonDoubleChecked import SDC

class MainManager(SDC):
    def __init__(self):
        self._logger = lh.init_logger(logger_name="{{ project_name }}_logger", is_json_output=False)

    def get_logger(self) -> logging.Logger:
        return self._logger
"""
