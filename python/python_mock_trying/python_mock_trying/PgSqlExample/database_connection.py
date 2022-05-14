from sqlalchemy.orm\
    import scoped_session, sessionmaker, relationship, backref, query_expression
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base
from loguru import logger

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

Base_auto = automap_base()
Base_auto.metadata.schema = "hk"
Base_auto.metadata.reflect(engine, only=[
    'company', 'employee', 'department',
])
Base_auto.query = db_session.query_property()

class CompanyTable(Base_auto):
    __tablename__ = "company"
    __table_args__ = {"extend_existing": True}
    expr = query_expression()  # so can use order by

class EmployeeTable(Base_auto):
    __tablename__ = "employee"
    __table_args__ = {"extend_existing": True}
    expr = query_expression()  # so can use order by

class DepartmentTable(Base_auto):
    __tablename__ = "department"
    __table_args__ = {"extend_existing": True}
    expr = query_expression()  # so can use order by

def generate_relationships(base, direction, return_fn, attrname, local_cls, referred_cls, **kw):
    return None

# Mappings are not produced until the .prepare() method is called on the class hierarchy
Base_auto.prepare(generate_relationship=generate_relationships)
