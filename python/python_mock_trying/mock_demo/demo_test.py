# this example comes from : https://mock-alchemy.readthedocs.io/en/latest/user_guide/index.html#data-stubbing
import datetime
import unittest
from unittest import mock

import pytest
from mock_alchemy.mocking import UnifiedAlchemyMagicMock

from mock_demo.data_analysis import complex_data_analysis, Data1, Data2, Data3, CombinedAnalysis

class TestMockDemo(unittest.TestCase):
    def test_data_analysis(self):
        stop_time = datetime.datetime.utcnow()
        cfg = {
            "final_time": stop_time
        }
        data1_values = [
            Data1(1, 10, 11, 12),
            Data1(2, 20, 21, 22),
            Data1(3, 30, 31, 32),
        ]
        data2_values = [
            Data2(1, 10, 11, 12),
            Data2(2, 20, 21, 22),
            Data2(3, 30, 31, 32),
        ]
        data3_values = [
            Data3(1, 10, 11, 12),
            Data3(2, 20, 21, 22),
            Data3(3, 30, 31, 32),
        ]
        session = UnifiedAlchemyMagicMock(data=[
            (
                [mock.call.query(Data1),
                 mock.call.filter(Data1.data_val1 < 20)],
                data1_values
            ),
            (
                [mock.call.query(Data2),
                 mock.call.filter(Data2.data_val2 < 30)],
                data2_values
            ),
            (
                [mock.call.query(Data3),
                 mock.call.filter(Data3.data_val3 < 40)],
                data3_values
            ),
        ])
        complex_data_analysis(cfg, session)
        expected_anyalsis = [
            CombinedAnalysis(1, 10, 11, 12),
            CombinedAnalysis(2, 20, 21, 22),
            CombinedAnalysis(3, 30, 31, 32),
        ]
        combined_anyalsis = session.query(CombinedAnalysis).all()
        print(combined_anyalsis)
        print(expected_anyalsis)
        assert sorted(combined_anyalsis, key=lambda x: x.pk1) == sorted(expected_anyalsis, key=lambda x: x.pk1)

if __name__ == "__main__":
    unittest.main()
