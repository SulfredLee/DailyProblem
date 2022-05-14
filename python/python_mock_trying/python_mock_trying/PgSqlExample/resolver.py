import datetime
import sqlalchemy
from python_mock_trying.PgSqlExample.database_connection\
    import CompanyTable, DepartmentTable, EmployeeTable
from typing import List, Set, Dict
from loguru import logger

class Resolver(object):
    def __init__(self
                 , db_session: sqlalchemy.orm.scoping.scoped_session):
        self._db_session = db_session

    def _get_table_col_names(self
                             , table: sqlalchemy.orm.decl_api.DeclarativeMeta
                            , exclude: Set[str] = {}) -> List[sqlalchemy.sql.schema.Column]:
        cols = [c for c in table.__table__.c if c.name not in exclude]

        assert len(cols) > 0, 'get_table_col_names() filtered out all columns!'
        return cols

    def _get_several_table_col_names(self
                                      , tables: List[sqlalchemy.orm.decl_api.DeclarativeMeta]
                                      , exclude: Set[str] = {}) -> List[sqlalchemy.sql.schema.Column]:
        cols = []
        for table in tables:
            cols += self._get_table_col_names(table, exclude)
        return cols

    def _new_query_multi(self
                         , tables: List[sqlalchemy.orm.decl_api.DeclarativeMeta]
                         , cols: List[sqlalchemy.sql.schema.Column] = None) -> sqlalchemy.orm.query.Query:
        qry = self._db_session().query(*tables)
        if cols is not None and len(cols) > 0:
            qry = qry.with_entities(*cols)
        return qry

    def _get_col_str_names_remove_duplicates(self
                                             , cols: List[sqlalchemy.sql.schema.Column]
                                             , duplicated_col: Set[str]) -> List[str]:
        result = list()

        for col in cols:
            if col.description in duplicated_col:
                result.append(f"{col.table.description}_{col.description}")
            else:
                result.append(col.description)

        return result

    def _convert_sa_row_to_dict(self
                                , src: List[sqlalchemy.engine.row.Row]
                                , cols_str: List[str] = None) -> List[dict]:
        if None == cols_str or len(cols_str) == 0:
            return [dict(row._mapping) for row in src]
        else:
            results_in_dict = list()
            for row in src:
                row_in_dict = dict()
                for idx, col in enumerate(row):
                    row_in_dict[cols_str[idx]] = col
                results_in_dict.append(row_in_dict)

            return results_in_dict

class CompanyResolver(Resolver):
    def __init__(self
                 , db_session: sqlalchemy.orm.scoping.scoped_session):
        super().__init__(db_session)

    def show_company_details_resolver(self
                                      , company: str
                                      , start_from: datetime.datetime
                                      , only_employee: bool) -> dict:
        result = dict()
        result["department"] = self.__get_all_department(company)
        for department in result["department"]:
            all_employee = self.show_all_employee(company, department["name"])
            department["number_of_employee"] = len(all_employee)
            department["employee"] = all_employee
        company_details = self.__get_company_details(company)
        result["owner"] = company_details["owner"]
        result["start_up_time"] = company_details["start_up_time"]
        result["name"] = company_details["name"]

        return result

    def show_all_employee(self
                          , company: str
                          , department: str
                          , join_time: datetime.datetime = None) -> List[dict]:
        cols = self._get_several_table_col_names([CompanyTable, DepartmentTable, EmployeeTable])
        cols_str = self._get_col_str_names_remove_duplicates(cols, {"name", "id"})
        query = self._new_query_multi([CompanyTable, DepartmentTable, EmployeeTable], cols)


        # join with department table
        query = query.join(DepartmentTable, CompanyTable.id == DepartmentTable.company_id)
        # join with employee table
        query = query.join(EmployeeTable, DepartmentTable.id == EmployeeTable.department_id)

        # filter by company
        if not "All" == company: query = query.filter(CompanyTable.name == company)
        # filter by department
        if not "All" == department: query = query.filter(DepartmentTable.name == department)

        results = self.__run_query(query)
        return self._convert_sa_row_to_dict(results, cols_str)

    def __get_all_department(self, company: str) -> dict:
        cols = self._get_several_table_col_names([CompanyTable, DepartmentTable])
        query = self._new_query_multi([CompanyTable, DepartmentTable], cols)

        # join with department table
        query = query.join(DepartmentTable, CompanyTable.id == DepartmentTable.company_id)

        # where case
        if not "All" == company:
            query = query.filter(CompanyTable.name == company)

        results = self.__run_query(query)
        results_in_dict = [dict(row._mapping) for row in results]

        return results_in_dict

    def __get_company_details(self, company: str) -> dict:
        cols = self._get_several_table_col_names([CompanyTable])
        query = self._new_query_multi([CompanyTable], cols)

        # where case
        query = query.filter(CompanyTable.name == company)

        results = self.__run_query(query)
        if len(results) > 0:
            return results[0]
        else:
            return {}

    def __run_query(self
                    , query: sqlalchemy.orm.query.Query
                    , debug: bool = False) -> List[sqlalchemy.engine.row.Row]:
        if debug:
            print(query.statement.compile(compile_kwargs={"literal_binds": True}))

        new_updated_since = datetime.datetime.now()
        # TODO add a timeout to this
        # https://stackoverflow.com/questions/492519/timeout-on-a-function-call
        results: List[sqlalchemy.engine.row.Row] = []
        try:
            results = query.all()
        except Exception as ex:
            query_time = datetime.datetime.now() - new_updated_since
            query_time = query_time.seconds + query_time.microseconds * 1e-6
            logger.error(f"query.all() failed sql ran for {query_time}")
            logger.error(ex)
            logger.error(f"SQL Statement:")
            logger.error(query.statement.compile(compile_kwargs={"literal_binds": True}))

        self._db_session.close()

        return results
