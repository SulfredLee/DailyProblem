import unittest
from unittest.mock import MagicMock, patch, Mock
from unittest import mock

from mock_alchemy.comparison import ExpressionMatcher
from mock_alchemy.mocking import AlchemyMagicMock
from python_mock_trying.PgSqlExample_Declarative.resolver import CompanyResolver
from python_mock_trying.PgSqlExample_Declarative.database_connection\
    import CompanyTable, DepartmentTable, EmployeeTable

class TestSqlalchemyMock(unittest.TestCase):
    def test_connection(self):
        mock_db_session = AlchemyMagicMock()
        # mock_db_session.add(CompanyTable(id="cjisldfh28fgsvKL9"
        #                                  , name="OO Capital"
        #                                  , start_up_time="2022-01-01 08:30:00"
        #                                  , owner=["Mr A", "Miss A"]))
        # mock_db_session.add(CompanyTable(id="cjieddfh28fgsvKL9"
        #                                  , name="PP Capital"
        #                                  , start_up_time="2022-01-02 08:30:00"
        #                                  , owner=["Mr A", "Miss B"]))
        mock_db_session.add_all([CompanyTable(id="cjisldfh28fgsvKL9"
                                              , name="OO Capital"
                                              , start_up_time="2022-01-01 08:30:00"
                                              , owner=["Mr A", "Miss A"])
                                 , CompanyTable(id="cjieddfh28fgsvKL9"
                                                , name="PP Capital"
                                                , start_up_time="2022-01-02 08:30:00"
                                                , owner=["Mr A", "Miss B"])])
        print(mock_db_session.query(CompanyTable).all())
        rs = CompanyResolver(mock_db_session)

        company = "OO Capital"
        start_from = None
        only_employee = False
        print(rs.show_company_details_resolver(company
                                               , start_from
                                               , only_employee))



if __name__ == "__main__":
    unittest.main()
