from typing import List, Dict, Tuple, Union, Any, Set
import threading
import copy

class TimelyCache_Snapshot(object):
    """! Keep a limited list of latest snapshot
    self.__dict: it stores a pair of key and value, the value is the latest snapshot
    self.__time_index: it stores a list of key in time sequential. Key value can be duplicated
    """
    def __init__(self, max_size: int = 1000, eq_fun: Any = None):
        self.__dict: Dict[Any, Any] = dict()
        self.__time_index: List[Any] = list() # store the timeseries of keys
        self.__key_counter: Dict[Any, int] = dict() # counting the number of occurance of a key
        self.__hist_data: List[Union[Any, Any]] = list()
        self.__mutex: threading.Lock = threading.Lock()
        self.__max_size = max_size
        self.__eq_fun = eq_fun

    def upsert_multi(self, keys: List[Any], values: List[Any]) -> List[bool]:
        is_new_list: List[bool] = list()
        with self.__mutex:
            for key, value in zip(keys, values):
                is_new_list.append(self.__upsert_ele_imp(key=key, value=value))

            return is_new_list

        is_new_list = [False] * len(keys)
        return is_new_list

    def upsert_ele(self, key: Any, value: Any) -> bool:
        with self.__mutex:
            return self.__upsert_ele_imp(key=key, value=value)

    def is_exist(self, key: Any) -> bool:
        with self.__mutex:
            return key in self.__dict

    def get_records_by_index(self, idx: int) -> Any:
        with self.__mutex:
            return copy.deepcopy(self.__dict[self.__time_index[idx]])

    def get_last_n_records_in_time_series(self, n: int) -> List[Any]:
        with self.__mutex:
            return [ele[1] for ele in self.__hist_data[-n:]]

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

    def __upsert_ele_imp(self, key: Any, value: Any) -> bool:
        is_new = False
        if key not in self.__dict:
            # new value found
            self.__time_index.append(key)
            if key not in self.__key_counter:
                self.__key_counter[key] = 0
            self.__key_counter[key] += 1
            is_new = True

            # save record
            self.__hist_data.append((key, value))
            self.__dict[key] = value
        else:
            if (None is not self.__eq_fun and self.__eq_fun(first=self.__dict[key], second=value))\
               or self.__dict[key] == value:
                # old value found
                return is_new
            else:
                # new value found
                self.__time_index.append(key)
                if key not in self.__key_counter:
                    self.__key_counter[key] = 0
                self.__key_counter[key] += 1
                is_new = True

                # save record
                self.__hist_data.append((key, value))
                self.__dict[key] = value

        self.__remove_extra_records()
        return is_new

    def __remove_extra_records(self):
        if len(self.__time_index) > self.__max_size:
            the_key = self.__time_index[0]
            self.__key_counter[the_key] -= 1
            if self.__key_counter[the_key] <= 0:
                del self.__key_counter[the_key]
                del self.__dict[the_key]
            del self.__hist_data[0]
            del self.__time_index[0]

        # if len(self.__dict) > self.__max_size:
        #     total_old_records = len(self.__dict) - self.__max_size
        #     old_key_set: Set[Any] = list()
        #     idx = 0
        #     while total_old_records > len(old_key_set):
        #         if len(old_key_set) == 0:
        #             old_key_set.append(self.__time_index[idx])
        #         else:
        #             if old_key_set[-1] != self.__time_index[idx]:
        #                 old_key_set.append(self.__time_index[idx])

        #         while old_key_set[-1] == self.__time_index[idx]:
        #             idx += 1

        #     last_n = idx
        #     # remove from dict
        #     for old_key in old_key_set:
        #         if old_key in self.__dict:
        #             del self.__dict[old_key]
        #     # remove from list
        #     del self.__time_index[:last_n]
        #     # remove from hist data
        #     del self.__hist_data[:total_old_records]

class TimelyCache_Hist(object):
    """! Keep a limited list of latest records
    self.__dict: it stores a pair of key and value
    self.__time_index: it stores a list of key in time sequential
    """
    def __init__(self, max_size: int = 1000, eq_fun: Any = None):
        self.__dict: Dict[Any, Any] = dict()
        self.__time_index: List[Union[Any, Any]] = list()
        self.__mutex: threading.Lock = threading.Lock()
        self.__max_size = max_size
        self.__eq_fun = eq_fun

    def upsert_multi(self, keys: List[Any], values: List[Any]) -> List[bool]:
        is_new_list: List[bool] = list()
        with self.__mutex:
            for key, value in zip(keys, values):
                is_new_list.append(self.__upsert_ele_imp(key=key, value=value))

            return is_new_list

        is_new_list = [False] * len(keys)
        return is_new_list

    def upsert_ele(self, key: Any, value: Any) -> bool:
        with self.__mutex:
            return self.__upsert_ele_imp(key=key, value=value)

    def is_exist(self, key: Any) -> bool:
        with self.__mutex:
            return key in self.__dict

    def get_records_by_index(self, idx: int) -> Any:
        with self.__mutex:
            return copy.deepcopy(self.__time_index[idx][1])

    def get_last_n_records_in_time_series(self, n: int) -> List[Any]:
        with self.__mutex:
            return [ele[1] for ele in self.__time_index[-n:]]

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

    def __upsert_ele_imp(self, key: Any, value: Any) -> bool:
        is_new = False
        if key not in self.__dict:
            # found new record
            is_new = True

            self.__time_index.append((key, value))
            self.__dict[key] = value
        else:
            if (None is not self.__eq_fun and self.__eq_fun(first=self.__dict[key], second=value))\
               or self.__dict[key] == value:
                # found old record
                is_new = False
            else:
                # found new record
                is_new = True

                self.__time_index.append((key, value))
                self.__dict[key] = value

        self.__remove_extra_records()

        return is_new

    def __remove_extra_records(self):
        if len(self.__time_index) > self.__max_size:
            del self.__dict[self.__time_index[0][0]]
            del self.__time_index[0]
        # if len(self.__time_index) > self.__max_size:
        #     extra_n = len(self.__time_index) - self.__max_size
        #     for ele in self.__time_index[:extra_n]:
        #         del self.__dict[ele[0]] # ele = (old_key, old_value)
        #     del self.__time_index[:extra_n]
