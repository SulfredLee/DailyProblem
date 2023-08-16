content_st = """
import logging
from typing import List, Dict, Tuple

import sfdevtoolslight.observability.log_helper as lh
from sfdevtoolslight.devTools.SingletonDoubleChecked import SDC

from {{ project_name }}.app.{{ app_subfolder }}.db.db import MicroBlog_DC

class MainManager(SDC):
    def __init__(self):
        self._logger = lh.init_logger(logger_name="{{ project_name }}_logger", is_json_output=False)
        self._dc = MicroBlog_DC()

    def get_logger(self) -> logging.Logger:
        return self._logger

    def get_all_blog_post(self) -> List:
        return self._dc.get_all_blog_post()

    def save_a_blog_post(self, blog_post: Dict) -> None:
        self._dc.save_a_blog_post(blog_post)
"""
