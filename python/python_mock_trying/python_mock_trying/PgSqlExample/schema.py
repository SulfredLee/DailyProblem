import graphene
from graphene import ResolveInfo
from python_mock_trying.PgSqlExample.resolver import CompanyResolver
from python_mock_trying.PgSqlExample.database_connection import db_session

rs = CompanyResolver(db_session)

class EmployeeSchema(graphene.ObjectType):
    name = graphene.String()
    gender = graphene.String()
    salary = graphene.Float()
    is_full_time = graphene.Boolean()
    join_time = graphene.DateTime()
    department = graphene.String()
    company = graphene.String()

    def resolve_name(root: dict, info: ResolveInfo):
        return root["employee_name"]

    def resolve_department(root: dict, info: ResolveInfo):
        return root["department_name"]

    def resolve_company(root: dict, info: ResolveInfo):
        return root["company_name"]

class DepartmentSchema(graphene.ObjectType):
    name = graphene.String()
    number_of_employee = graphene.Int()
    address = graphene.String()
    start_time = graphene.Time()
    end_time = graphene.Time()

    employee = graphene.List(EmployeeSchema)

class ShowCompanyDetailsSchema(graphene.ObjectType):
    department = graphene.List(DepartmentSchema)
    owner = graphene.List(graphene.String)
    start_up_time = graphene.DateTime()
    name = graphene.String()

class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()

    showCompanyDetails = graphene.Field(
        ShowCompanyDetailsSchema
        , company=graphene.String()
        , start_from=graphene.DateTime()
        , only_employee=graphene.Boolean())

    showAllEmployee = graphene.List(
        EmployeeSchema
        , company=graphene.String()
        , department=graphene.String()
        , join_time=graphene.DateTime())

    def resolve_showCompanyDetails(root, info: ResolveInfo, **args):
        company = args.get("company", "All")
        start_from = args.get("start_from", None)
        only_employee = args.get("only_employee", False)

        return rs.show_company_details_resolver(company
                                                , start_from
                                                , only_employee)

    def resolve_showAllEmployee(root, info: ResolveInfo, **args):
        company = args.get("company", "All")
        department = args.get("department", "All")
        join_time = args.get("join_time", None)

        return rs.show_all_employee(company
                                    , department
                                    , join_time)
