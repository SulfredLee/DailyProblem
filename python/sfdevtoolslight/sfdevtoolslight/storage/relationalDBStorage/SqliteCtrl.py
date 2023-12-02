from typing import Dict, List, Set, Tuple, Union, Any
from pathlib import Path
from sqlalchemy import exc, create_engine, MetaData # poetry add psycopg2-binary, sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import sqlalchemy
import pandas as pd
import logging

class SqliteCtrl(object):
    def __init__(self
                 , db_location: Path
                 , logger: logging.Logger
                 , include_tables: List[str] = None
                 , connection_time: int = 10):
        self._logger = logger
        self._logger = logger

        self._logger.info(f"db config db_location: {db_location}")
        # prepare database connection
        self._engine = sqlalchemy.create_engine(f"sqlite:///{db_location}", echo=False)

        # prepare metadata, metadata will contain tables information
        self._metadata = MetaData()
        if None == include_tables:
            self._metadata.reflect(bind=self._engine)
        else:
            self._metadata.reflect(bind=self._engine, only=include_tables)

        # prepare automap base, this will map tables to python class
        self._automap_base = automap_base(metadata=self._metadata)
        self._automap_base.prepare(self._engine, reflect=True)

        # successfully connected
        self._logger.info("Successfully connected")
        self._logger.info(self._metadata.tables.keys())
        self._logger.info(self._automap_base.classes.keys())

        pass

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
        except exc.SQLAlchemyError as e:
            self._logger.error(e)
            self._logger.error(traceback.format_exc())
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
        except exc.SQLAlchemyError as e:
            self._logger.error(e)
            self._logger.error(traceback.format_exc())
            db_session.rollback()
            return False
        finally:
            db_session.close()

    def upsert_records_df(self, df: pd.DataFrame, table_name: str) -> int:
        # this method will recreate the table, only use this when you fully understand what you are doing
        # return df.to_sql(name=table_name, con=self._engine, if_exists="replace")
        return 10
