import unittest

class TestPythonCreator(unittest.TestCase):
    def test_001(self):
        self.assertEqual("test".upper(), "TEST")

if __name__ == "__main__":
    unittest.main()
