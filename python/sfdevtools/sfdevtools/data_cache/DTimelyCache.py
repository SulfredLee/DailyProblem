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
        self.__time_index: List[Any] = list()
        self.__hist_data: List[Union[Any, Any]] = list()
        self.__mutex: threading.Lock = threading.Lock()
        self.__max_size = max_size

    def upsert_multi(self, keys: List[Any], values: List[Any]) -> None:
        with self.__mutex:
            for key, value in zip(keys, values):
                if key not in self.__dict:
                    self.__time_index.append(key)
                self.__hist_data.append((key, value))
                self.__dict[key] = value

            self.__remove_extra_records()

    def upsert_ele(self, key: Any, value: Any) -> None:
        with self.__mutex:
            if key not in self.__dict:
                self.__time_index.append(key)
            self.__hist_data.append((key, value))
            self.__dict[key] = value

            self.__remove_extra_records()

    def is_exist(self, key: Any) -> Any:
        with self.__mutex:
            return key in self.__dict

    def get_records_by_index(self, idx: int) -> Any:
        with self.__mutex:
            return copy.deepcopy(self.__dict[self.__time_index[idx]])

    def get_records_in_time_series(self) -> List[Any]:
        with self.__mutex:
            return [ele[1] for ele in self.__hist_data]

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
            old_key_list: List[Any] = list()
            idx = 0
            while total_old_records > len(old_key_list):
                if len(old_key_list) == 0:
                    old_key_list.append(self.__time_index[idx])
                else:
                    if old_key_list[-1] != self.__time_index[idx]:
                        old_key_list.append(self.__time_index[idx])

                while old_key_list[-1] == self.__time_index[idx]:
                    idx += 1

            last_n = idx
            # remove from dict
            for old_key in old_key_list:
                del self.__dict[old_key]
            # remove from list
            del self.__time_index[:last_n]
            # remove from hist data
            del self.__hist_data[:total_old_records]

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
