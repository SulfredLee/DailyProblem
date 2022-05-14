from python_mock_trying import __version__
from python_mock_trying.main import quick_fun
from python_mock_trying.NewOfficeManager.FundManager import FundManager

import unittest
from unittest.mock import MagicMock, patch, Mock

class TestProject(unittest.TestCase):
    def test_partial_mock_class_functions(self):
        '''
        Here shows how to mock a class member function
        while we keep the other functions as unmock version
        '''
        fund_manager = FundManager()

        '''
        check if member function exist
         - we need this checking because the MagicMock function will always success even if the member function is not exist
        '''
        fund_manager.tell_total_members() # check if member function exist
        fund_manager.tell_total_members = MagicMock()
        fund_manager.tell_total_members.return_value = 8
        self.assertEqual(8, fund_manager.tell_total_members()) # call the mock function
        self.assertEqual(0, fund_manager.get_office_size()) # call original function
        self.assertEqual("Not enough office size", quick_fun(fund_manager)) # real test here

        fund_manager.tell_total_members.return_value = 1
        self.assertEqual("Enough office size", quick_fun(fund_manager)) # real test here

    def test_mock_function_with_dynamic_input(self):
        fund_manager = FundManager()
        fund_manager.get_office_size() # check if member function exist

        def demo_function(value: int):
            return value + 1

        is_constructor_example = True
        if is_constructor_example:
            fund_manager.get_office_size = MagicMock(side_effect=demo_function) # here we use the mock to redefine the member function
        else:
            fund_manager.get_office_size = MagicMock()
            fund_manager.get_office_size.side_effect = demo_function
        self.assertEqual(11, fund_manager.get_office_size(10))

    def test_version(self):
        assert __version__ == '0.1.0'

if __name__ == "__main__":
    unittest.main()
