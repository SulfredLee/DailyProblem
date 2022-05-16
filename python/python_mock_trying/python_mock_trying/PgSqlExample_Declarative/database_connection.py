from sqlalchemy.orm\
    import scoped_session, sessionmaker, relationship, backref, query_expression
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base
from loguru import logger
import sqlalchemy as sa

db_user = "postgres"
db_password = "postgres"
db_host = "localhost"
db_port = 25432
db_name = "postgres"

try:
    engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
                           , convert_unicode=True)
    db_session = scoped_session(sessionmaker(autocommit=False
                                             , autoflush=False
                                             , bind=engine))
except Exception as e:
    logger.error(e)
    logger.error("No DB connection. Stop Server")
    exit(1)

Base = declarative_base()
Base.metadata.schema = "hk"

class CompanyTable(Base):
    __tablename__ = "company"
    id = sa.Column(sa.TEXT, primary_key=True)
    name = sa.Column(sa.TEXT)
    start_up_time = sa.Column(sa.DATETIME)
    owner = sa.Column(sa.ARRAY(sa.TEXT))

    def __init__(self, id, name, start_up_time, owner):
        self.id = id
        self.name = name
        self.start_up_time = start_up_time
        self.owner = owner

class EmployeeTable(Base):
    __tablename__ = "employee"
    id = sa.Column(sa.TEXT, primary_key=True)
    name = sa.Column(sa.TEXT)
    gender = sa.Column(sa.TEXT)
    is_full_time = sa.Column(sa.BOOLEAN)
    join_time = sa.Column(sa.DATETIME)
    department_id = sa.Column(sa.TEXT)

    def __init__(self, id, name, gender, is_full_time, join_time, department_id):
        self.id = id
        self.name = name
        self.gender = gender
        self.is_full_time = is_full_time
        self.join_time = join_time
        self.department_id = department_id

class DepartmentTable(Base):
    __tablename__ = "department"
    id = sa.Column(sa.TEXT, primary_key=True)
    name = sa.Column(sa.TEXT)
    start_time = sa.Column(sa.DATETIME)
    end_time = sa.Column(sa.DATETIME)
    address = sa.Column(sa.TEXT)
    company_id = sa.Column(sa.TEXT)

    def __init__(self, id, name, start_time, end_time, address, company_id):
        self.id = id
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.address = address
        self.company_id = company_id
