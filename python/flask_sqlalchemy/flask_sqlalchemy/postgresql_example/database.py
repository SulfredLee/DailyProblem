from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('postgresql+psycopg2://postgres:postgres@127.0.0.1:25432/postgres', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.metadata.schema = "example_company"
Base.query = db_session.query_property()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    from models import Employee
    # Base.metadata.drop_all(bind=engine) # this will drop the original table
    # Base.metadata.create_all(bind=engine) # this will drop the original table

    # Create an employee record
    # peter = Employee(id=2, name='Peter', hired_on=datetime(2022, 4, 9, 14, 30, 1))
    peter = Employee(name='Peter')
    # john = Employee(id=6, name='John', hired_on=datetime(2022, 4, 9, 14, 30, 1))
    # db_session.add(john)
    db_session.add(peter)
    db_session.commit()
    print("Finished init db")
    # # Create the fixtures
    # engineering = Department(name='Engineering')
    # db_session.add(engineering)
    # hr = Department(name='Human Resources')
    # db_session.add(hr)

    # manager = Role(name='manager')
    # db_session.add(manager)
    # engineer = Role(name='engineer')
    # db_session.add(engineer)

    # peter = Employee(name='Peter', department=engineering, role=engineer)
    # db_session.add(peter)
    # roy = Employee(name='Roy', department=engineering, role=engineer)
    # db_session.add(roy)
    # tracy = Employee(name='Tracy', department=hr, role=manager)
    # db_session.add(tracy)
    # db_session.commit()
