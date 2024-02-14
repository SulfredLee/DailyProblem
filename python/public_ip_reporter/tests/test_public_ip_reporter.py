
# poetry run python -m unittest

# Imports
import unittest
from unittest.mock import Mock, create_autospec, patch
import sfdevtoolslight.observability.log_helper as lh
from typing import List, Dict, Tuple
import inspect

# Functions
class Test_public_ip_reporter(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.__logger = lh.init_logger(logger_name="test_public_ip_reporter_logger", is_json_output=False)

        self.__test_config = {
            "test_example": False
        }
        if not self.__test_config[self._testMethodName]:
            self.__logger.info(f"Skip test {self._testMethodName}")
            return

    def tearDown(self):
        pass

    def test_example(self):
        """! Example Test funtions
        @param description Argument parser description

        @return argument parser
        """
        if not self.__test_config[inspect.stack()[0][3]]:
            return
        # import sfdevtoolslight.storage.relationalDBStorage.PostgresDBCtrl as postDBCtrl
        # mock_PostgresDBCtrl = create_autospec(postDBCtrl.PostgresDBCtrl)
        self.assertEqual("test".upper(), "TEST")

if __name__ == "__main__":
    unittest.main()