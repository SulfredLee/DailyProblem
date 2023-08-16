# poetry run python -m unittest

# Imports
import unittest
import logging
import inspect
from functools import partial
from time import sleep
import datetime
from typing import List, Dict, Any

import sfdevtoolslight.observability.log_helper as lh

# Functions
class Test_sfdevtoolslight(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.__logger = lh.init_logger(logger_name="light_logger", is_json_output=False)

        return

    def tearDown(self):
        pass

    def test_example(self):
        """! Example Test funtions
        """
        self.assertEqual("test".upper(), "TEST")
        self.__logger.info(f"here")

if __name__ == "__main__":
    unittest.main()
