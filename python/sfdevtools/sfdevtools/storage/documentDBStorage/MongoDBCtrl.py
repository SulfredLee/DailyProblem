import logging
import pymongo
from pymongo import MongoClient

class MongoDBCtrl(object):
    def __init__(self
                 , db_user: str
                 , db_pw: str
                 , db_host: str
                 , db_port: str
                 , db_name: str
                 , logger: logging.Logger
                 , db_conn_protocol: str = "mongodb+srv"
                 , connection_time_ms: int = 20000):
        self._logger: logging.Logger = logger
        self._db_client = None
        if "mongodb" == db_conn_protocol:
            # this connection works for local minikube mongodb creation
            self._db_client = MongoClient(f"mongodb://{db_user}:{db_pw}@{db_host}:{db_port}/?authSource={db_name}"
                                          , serverSelectionTimeoutMS=connection_time_ms)
        else:
            # this connection works for mongodb service provided by altas
            self._db_client = MongoClient(f"mongodb+srv://{db_user}:{db_pw}@{db_host}/?retryWrites=true&w=majority"
                                          , serverSelectionTimeoutMS=connection_time_ms)
        self._db = self._db_client[db_name]

    def get_db(self, db_name: str = None) -> pymongo.database.Database:
        if None is db_name:
            return self._db
        else:
            return self._db_client[db_name]

    def get_collection(self, collection_name: str) -> pymongo.collection.Collection:
        return self._db[collection_name]
