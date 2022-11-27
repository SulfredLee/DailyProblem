content_st = """
# poetry run python -m unittest

# Imports
import unittest

# Functions
class Test_{{ project_name }}(unittest.TestCase):
    def test_example(self):
        \"\"\"! Example Test funtions
        \"\"\"
        self.assertEqual("test".upper(), "TEST")

if __name__ == "__main__":
    unittest.main()
"""
