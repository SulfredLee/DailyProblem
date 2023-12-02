import logging
import boto3
from botocore.config import Config
from typing import List, Dict, Any, Union
from datetime import datetime, timedelta, date
import threading
import time
import pandas as pd

# https://github.com/awslabs/amazon-timestream-tools/blob/7d01250e8cda6a3da94150d1df6c125f70a017f3/sample_apps/python/CsvIngestionExample.py
class AWSTimeSeriesStorage(object):
    def __init__(self):
        self.__logger: logging.Logger = None
        self.__write_client: boto3.Session.client = None
        self.__query_client: boto3.Session.client = None
        self.__batch_size: int = 100
        self.__db_name: str = None
        self.__tb_name: str = None
        self.__mutex: threading.Lock = threading.Lock()

    def init_component(self
                       , logger: logging.Logger
                       , db_name: str
                       , tb_name: str
                       , batch_size: int = 100
                       , read_timeout: int = 20
                       , max_pool_connections: int = 5000
                       , max_attempts: int = 10) -> None:
        self.__logger = logger
        self.__batch_size = batch_size
        self.__db_name = db_name
        self.__tb_name = tb_name

        session = boto3.Session()
        self.__write_client = session.client("timestream-write", config=Config(read_timeout=read_timeout
                                                                               , max_pool_connections=max_pool_connections
                                                                               , retries={"max_attempts": max_attempts}))
        self.__query_client = session.client("timestream-query")

    def save_records(self, data_records: List[Any]):
        current_time = self._current_milli_time()
        with self.__mutex:
            records: List = list()
            # counter = 0
            for data in data_records:
                dimensions: List[Dict[str, str]] = data[0]
                measure_name: str = data[1]
                measure_value: str = data[2]
                measure_value_type: str = data[3]
                time_str: str = data[4]

                # record_time = current_time - (counter * 50)
                record = {
                    "Dimensions": dimensions
                    , "MeasureName": measure_name # "Any"
                    , "MeasureValue": measure_value # "0.01"
                    , "MeasureValueType": measure_value_type # "DOUBLE"
                    , "Time": time_str
                    # , "Time": str(record_time)
                    # , "Time": str(datetime.utcnow().timestamp())
                   }

                self.__logger.info(record)
                records.append(record)
                # counter = counter + 1

                if len(records) == self.__batch_size:
                    self._submit_batch(records=records, db_name=self.__db_name, tb_name=self.__tb_name)
                    records = list()

            if len(records) != 0:
                self._submit_batch(records=records, db_name=self.__db_name, tb_name=self.__tb_name)

    def get_records(self, query: str):
        q_data = self.__query_client.query(QueryString=query)

        header: List[str] = list()
        for col_ele in q_data["ColumnInfo"]:
            header.append(col_ele["Name"])
            # dtypes.append(col_ele["Type"]["ScalarType"]) # TODO, can map datatype from aws to pandas


        data_list: List[List] = list()
        for row_ele in q_data["Rows"]:
            data: List = list()
            for ele in row_ele["Data"]:
                for k, v in ele.items():
                    if k == "NullValue":
                        data.append(None)
                    else:
                        data.append(v)

            data_list.append(data)

        return pd.DataFrame(data_list, columns=header)

    def _submit_batch(self
                      , records: List
                      , db_name: str
                      , tb_name: str) -> None:
        result = self.__write_client.write_records(DatabaseName=db_name
                                                   , TableName=tb_name
                                                   , Records=records
                                                   , CommonAttributes={})

    @staticmethod
    def _current_milli_time():
        return int(round(time.time() * 1000))
