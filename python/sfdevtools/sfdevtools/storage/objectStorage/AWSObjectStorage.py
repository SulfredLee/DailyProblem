import logging
import boto3 # poetry add boto3
from datetime import datetime
from nanoid import generate # poetry add nanoid
from pathlib import Path
import os
import sfdevtools.devTools.DatetimeTools as dtt

class AWSObjectStorage(object):
    def __init__(self, logger: logging.Logger):
        self.__logger = logger
        self.__s3_client = boto3.client("s3")

    def __del__(self):
        self.__s3_client.close()

    def upload_file_from_memory(self
                                , file_name: str
                                , file_content: str
                                , bucket_name: str
                                , obj_name: str) -> None:
        """! upload_file_from_memory
        @file_name file name, "test.csv"
        @file_content file content in memory
        @bucket_name s3 bucket name
        @obj_name object name on s3, example "other/cur_date/test.csv"

        @return None
        """
        temp_file_name: str = dtt.get_random_file_name(file_name=file_name)
        # temp_file_name: Path = Path.joinpath(Path(__file__).parent, temp_file_name)
        temp_file_name: Path = Path.joinpath(Path("/", "tmp"), temp_file_name)

        with open(temp_file_name, "w") as FH:
            FH.write(file_content)
        self.__s3_client.upload_file(temp_file_name, bucket_name, obj_name)

        if os.path.exists(temp_file_name):
            os.remove(temp_file_name)

    def list_objects(self, bucket_name: str) -> None:
        """! list_objects
        @bucket_name s3 bucket name

        @return None
        """
        response = self.__s3_client.list_objects(Bucket=bucket_name)
        self.__logger.info(response["Contents"])
