content_st = """
# poetry run python -m unittest

import unittest

class Test_{{ project_name }}(unittest.TestCase):
    def test_example(self):
        self.assertEqual("test".upper(), "TEST")

if __name__ == "__main__":
    unittest.main()
"""
