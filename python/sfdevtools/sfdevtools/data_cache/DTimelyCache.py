from typing import List, Dict, Tuple, Union, Any
import threading
import copy

class TimelyCache_Snapshot(object):
    """! Keep a limited list of latest snapshot
    self.__dict: it stores a pair of key and value, the value is the latest snapshot
    self.__time_index: it stores a list of key in time sequential. Key value can be duplicated
    """
    def __init__(self, max_size: int = 1000):
        self.__dict: Dict[Any, Any] = dict()
        self.__time_index: List[Union[Any, Any]] = list()
        self.__mutex: threading.Lock = threading.Lock()
        self.__max_size = max_size

    def upsert_multi(self, keys: List[Any], values: List[Any]) -> None:
        with self.__mutex:
            for key, value in zip(keys, values):
                self.__time_index.append((key, value))
                self.__dict[key] = value

            self.__remove_extra_records()

    def upsert_ele(self, key: Any, value: Any) -> None:
        with self.__mutex:
            self.__time_index.append((key, value))
            self.__dict[key] = value

            self.__remove_extra_records()

    def is_exist(self, key: Any) -> Any:
        with self.__mutex:
            return key in self.__dict

    def get_records_by_index(self, idx: int) -> Any:
        with self.__mutex:
            return copy.deepcopy(self.__time_index[idx])

    def get_records_in_time_series(self) -> List[Any]:
        with self.__mutex:
            return [ele[1] for ele in self.__time_index]

    def get_ele(self, key: Any) -> Any:
        with self.__mutex:
            if key not in self.__dict:
                return None
            return copy.deepcopy(self.__dict[key])

    def size(self) -> int:
        with self.__mutex:
            return len(self.__dict)

    def items(self):
        with self.__mutex:
            for k, v in self.__dict.items():
                yield k, v

    def __remove_extra_records(self):
        if len(self.__dict) > self.__max_size:
            total_old_records = len(self.__dict) - self.__max_size
            # find the outdated key
            old_key, old_value = self.__time_index[0]
            last_n = 0
            old_record_count = 1
            old_key_list: List[Any] = list()
            # find old records from list
            for idx, ele in enumerate(self.__time_index):
                if not ele[0] == old_key:
                    old_record_count += 1
                    old_key_list.append(old_key)
                    old_key = ele[0]
                    if old_record_count > total_old_records:
                        last_n = idx
                        break
            # remove from dict
            for old_key in old_key_list:
                del self.__dict[old_key]
            # remove from list
            del self.__time_index[:last_n]

class TimelyCache_Hist(object):
    """! Keep a limited list of latest records
    self.__dict: it stores a pair of key and value
    self.__time_index: it stores a list of key in time sequential
    """
    def __init__(self, max_size: int = 1000):
        self.__dict: Dict[Any, Any] = dict()
        self.__time_index: List[Union[Any, Any]] = list()
        self.__mutex: threading.Lock = threading.Lock()
        self.__max_size = max_size

    def upsert_multi(self, keys: List[Any], values: List[Any]) -> None:
        with self.__mutex:
            for key, value in zip(keys, values):
                if key in self.__dict:
                    return

                self.__time_index.append((key, value))
                self.__dict[key] = value

            self.__remove_extra_records()

    def upsert_ele(self, key: Any, value: Any) -> None:
        with self.__mutex:
            if key in self.__dict:
                return

            self.__time_index.append((key, value))
            self.__dict[key] = value

            self.__remove_extra_records()

    def is_exist(self, key: Any) -> Any:
        with self.__mutex:
            return key in self.__dict

    def get_records_by_index(self, idx: int) -> Any:
        with self.__mutex:
            return copy.deepcopy(self.__time_index[idx][1])

    def get_records_in_time_series(self) -> List[Any]:
        with self.__mutex:
            return [ele[1] for ele in self.__time_index]

    def get_ele(self, key: Any) -> Any:
        with self.__mutex:
            if key not in self.__dict:
                return None
            return copy.deepcopy(self.__dict[key])

    def size(self) -> int:
        with self.__mutex:
            return len(self.__dict)

    def items(self):
        with self.__mutex:
            for k, v in self.__dict.items():
                yield k, v

    def __remove_extra_records(self):
        if len(self.__dict) > self.__max_size:
            extra_n = len(self.__dict) - self.__max_size
            for ele in self.__time_index[:extra_n]:
                del self.__dict[ele[0]] # ele = (old_key, old_value)
            del self.__time_index[:extra_n]
