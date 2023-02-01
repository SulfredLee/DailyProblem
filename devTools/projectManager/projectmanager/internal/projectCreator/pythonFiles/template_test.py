content_st = """
# poetry run python -m unittest

# Imports
import unittest
import sfdevtools.observability.log_helper as lh

# Functions
class Test_{{ project_name }}(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.__logger = lh.init_logger(logger_name="test_{{ project_name }}_logger", is_json_output=False)

    def tearDown(self):
        pass

    def test_example(self):
        \"\"\"! Example Test funtions
        @param description Argument parser description

        @return argument parser
        \"\"\"
        self.assertEqual("test".upper(), "TEST")

if __name__ == "__main__":
    unittest.main()
"""
