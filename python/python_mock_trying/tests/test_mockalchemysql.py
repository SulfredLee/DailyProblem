import unittest
from unittest.mock import MagicMock, patch, Mock

from mock_alchemy.comparison import ExpressionMatcher

class TestSqlalchemyMock(unittest.TestCase):
    def test_connection(self):
        ExpressionMatcher(Model.foo == 5) == (Model.foo == 5)
        pass

if __name__ == "__main__":
    unittest.main()
