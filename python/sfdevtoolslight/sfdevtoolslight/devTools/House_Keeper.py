from datetime import datetime
from pathlib import Path
from dateutil.relativedelta import *
import logging

class House_Keeper(object):
    def __init__(self):
        self.__logger: logging.Logger = None
        pass

    def Init_Component(self
                       , logger: logging.Logger) -> None:
        self.__logger = logger

        return None

    def Remove_Files_Older_Than(self
                                , file_path: Path
                                , duration: relativedelta = relativedelta(months=+1)
                                , file_pattern: str = "*") -> None:
        if file_path.exists() == False:
            return None

        for item in Path(file_path).glob(file_pattern):
            if item.is_file():
                file_created_time = datetime.fromtimestamp(item.stat().st_mtime)
                oldest_accept_time = datetime.now() - duration
                if file_created_time < oldest_accept_time:
                    self.__logger.info(f"remove file: {file_created_time} due to older than {oldest_accept_time}")
                    item.unlink()

        return None

