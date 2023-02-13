from sqlalchemy import create_engine, MetaData # poetry add psycopg2-binary, sqlalchemy
from sqlalchemy.ext.automap import automap_base
import sqlalchemy
from sqlalchemy.orm import Session
from typing import List, Dict, Tuple, Any
import pandas as pd
import logging

# https://hackersandslackers.com/database-queries-sqlalchemy-orm/
class PostgresDBCtrl(object):
    def __init__(self
                 , db_user: str
                 , db_pw: str
                 , db_host: str
                 , db_port: str
                 , db_name: str
                 , db_schema: str
                 , logger: logging.Logger
                 , include_tables: List[str] = None
                 , connection_time: int = 10):
        self._logger = logger

        self._logger.info(f"db config db_user: {db_user}, db_host: {db_host}, db_port: {db_port}, db_name: {db_name}")
        # prepare database connection
        self._engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_pw}@{db_host}:{db_port}/{db_name}"
                                     , connect_args={"connect_timeout": connection_time})

        # prepare metadata, metadata will contain tables information
        self._metadata = MetaData()
        if None == include_tables:
            self._metadata.reflect(bind=self._engine)
        else:
            self._metadata.reflect(bind=self._engine, only=include_tables)

        # prepare automap base, this will map tables to python class
        self._automap_base = automap_base(metadata=self._metadata)
        self._automap_base.prepare(self._engine, reflect=True, schema=db_schema)

        # successfully connected
        self._logger.info("Successfully connected")
        self._logger.info(self._metadata.tables.keys())
        self._logger.info(self._automap_base.classes.keys())

    def get_classes(self) -> sqlalchemy.util._collections.Properties:
        return self._automap_base.classes

    def get_tables(self) -> sqlalchemy.util._collections.FacadeDict:
        return self._metadata.tables

    def get_session(self) -> sqlalchemy.orm.session.Session:
        return Session(self._engine)

    def get_connection(self) -> sqlalchemy.engine.base.Connection:
        return self._engine.connect()

    def get_query(self, *args) -> sqlalchemy.orm.query.Query:
        return Session(self._engine).query(*args)

    def get_df_from_query(self, query: sqlalchemy.orm.query.Query, is_debug: bool = False) -> pd.DataFrame:
        if is_debug:
            self._logger.debug(query.statement.compile(compile_kwargs={"literal_binds": True}))
        return pd.read_sql(sql=query.statement, con=self.get_connection())

    def add_records(self, db_records: List[Any]) -> bool:
        db_session = Session(self._engine)
        db_session.add_all(db_records)

        try:
            db_session.commit()
            return True
        except SQLAlchemyError as e:
            db_session.rollback()
            return False
        finally:
            db_session.close()

    def upsert_records(self, db_records: List[Any]) -> bool:
        if len(db_records) == 0:
            return True

        db_session = Session(self._engine)
        for db_record in db_records:
            db_session.merge(db_record)

        try:
            db_session.commit()
            return True
        except SQLAlchemyError as e:
            db_session.rollback()
            return False
        finally:
            db_session.close()
