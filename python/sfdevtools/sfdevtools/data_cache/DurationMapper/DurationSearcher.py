import logging
import datetime
from typing import Dict, List, Any, Union
import pandas as pd

class DurationSearcher(object):
    def __init__(self):
        self.__logger: logging.Logger = None
        self.__map: Dict[str, List[Any]] = dict()
        self.__row_key: str = None
        self.__create_new_ele: Any = None

    def init_component(self
                       , logger: logging.Logger
                       , row_key: str
                       , create_new_ele: Any):
        self.__logger = logger
        self.__row_key = row_key
        self.__create_new_ele = create_new_ele

    def create_map(self, df: pd.DataFrame) -> None:
        for index, row in df.iterrows():
            if row[self.__row_key] not in self.__map:
                # insert new code

                ele = self.__create_new_ele(row=row)

                self.__map[row[self.__row_key]] = [ele]
                continue

            # insert new record to an existing code
            ele = self.__create_new_ele(row=row)

            ele_list = self.__map[row[self.__row_key]]
            insert_idx = self.__find_insert_idx(ele_list=ele_list, start_date=ele.start_date)
            ele_list.insert(insert_idx, ele)

    def get_ele(self, code: str, point_of_time: datetime.datetime) -> Any:
        if code not in self.__map:
            return None

        ele_list: List[Any] = self.__map[code]
        if len(ele_list) == 0:
            return None

        idx = self.__find_retrieve_idx(ele_list=ele_list, start_date=point_of_time)

        if idx == len(ele_list):
            return ele_list[-1]
        elif idx == -1:
            return ele_list[0]
        else:
            return ele_list[idx]

    def items(self):
        for k, v in self.__map.items():
            yield k, v

    def __find_retrieve_idx(self, ele_list: List[Any], start_date: datetime.datetime):
        for idx, ele in enumerate(ele_list):
            if start_date <= ele.start_date:
                return idx - 1

        return len(ele_list)

    def __find_insert_idx(self, ele_list: List[Any], start_date: datetime.datetime):
        for idx, ele in enumerate(ele_list):
            if start_date <= ele.start_date:
                return idx

        return len(ele_list)
