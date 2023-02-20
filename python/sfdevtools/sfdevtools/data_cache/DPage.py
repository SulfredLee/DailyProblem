import logging
from typing import List, Dict, Tuple, Union, Any
import threading

class DPage(object):
    def __init__(self):
        self.__logger: logging.Logger = None
        self.__int_mutex: threading.Lock = threading.Lock()
        self.__float_mutex: threading.Lock = threading.Lock()
        self.__str_mutex: threading.Lock = threading.Lock()
        self.__bool_mutex: threading.Lock = threading.Lock()
        self.__other_mutex: threading.Lock = threading.Lock()
        self.__int32_map: Dict[int, int] = dict()
        self.__int64_map: Dict[int, int] = dict()
        self.__float_map: Dict[int, float] = dict()
        self.__double_map: Dict[int, float] = dict()
        self.__string_map: Dict[int, str] = dict()
        self.__bool_map: Dict[int, bool] = dict()

        self.__save_map: Dict[int, Any] = {
            0: self.__save_fid_int32
            , 1: self.__save_fid_int64
            , 2: self.__save_fid_float
            , 3: self.__save_fid_double
            , 4: self.__save_fid_string
            , 5: self.__save_fid_other
            , 6: self.__save_fid_bool
        }
        self.__get_map: Dict[int, Any] = {
            0: self.__get_fid_int32
            , 1: self.__get_fid_int64
            , 2: self.__get_fid_float
            , 3: self.__get_fid_double
            , 4: self.__get_fid_string
            , 5: self.__get_fid_other
            , 6: self.__get_fid_bool
        }
        self.__bucket_size = 10000

    def init_component(self, logger: logging.Logger) -> None:
        self.__logger = logger

    def save_fid(self, fid_num: int, fid_value: Any) -> None:
        bucket_num = int((fid_num - 1) / self.__bucket_size)
        if bucket_num not in self.__save_map:
            return None
        self.__save_map[bucket_num](fid_num=fid_num, fid_value=fid_value)

    def get_fid(self, fid_num: int) -> Union[bool, Any]:
        bucket_num = int((fid_num - 1) / self.__bucket_size)
        if bucket_num not in self.__get_map:
            return (False, None)

        return (True, self.__get_map[bucket_num](fid_num=fid_num))

    def __save_fid_int32(self, fid_num: int, fid_value: int) -> None:
        with self.__int_mutex:
            self.__int32_map[fid_num] = fid_value

    def __save_fid_int64(self, fid_num: int, fid_value: int) -> None:
        with self.__int_mutex:
            self.__int64_map[fid_num] = fid_value

    def __save_fid_float(self, fid_num: int, fid_value: float) -> None:
        with self.__float_mutex:
            self.__float_map[fid_num] = fid_value

    def __save_fid_double(self, fid_num: int, fid_value: float) -> None:
        with self.__float_mutex:
            self.__double_map[fid_num] = fid_value

    def __save_fid_string(self, fid_num: int, fid_value: str) -> None:
        with self.__str_mutex:
            self.__string_map[fid_num] = fid_value

    def __save_fid_bool(self, fid_num: int, fid_value: float) -> None:
        with self.__bool_mutex:
            self.__bool_map[fid_num] = fid_value

    def __save_fid_other(self, fid_num: int, fid_value: Any) -> None:
        pass

    def __get_fid_int32(self, fid_num: int) -> Union[bool, int]:
        with self.__int_mutex:
            if fid_num in self.__int32_map:
                return (True, self.__int32_map[fid_num])
            else:
                return (False, None)

    def __get_fid_int64(self, fid_num: int) -> Union[bool, int]:
        with self.__int_mutex:
            if fid_num in self.__int64_map:
                return (True, self.__int64_map[fid_num])
            else:
                return (False, None)

    def __get_fid_float(self, fid_num: int) -> Union[bool, float]:
        with self.__float_mutex:
            if fid_num in self.__float_map:
                return (True, self.__float_map[fid_num])
            else:
                return (False, None)

    def __get_fid_double(self, fid_num: int) -> Union[bool, float]:
        with self.__float_mutex:
            if fid_num in self.__double_map:
                return (True, self.__double_map[fid_num])
            else:
                return (False, None)

    def __get_fid_string(self, fid_num: int) -> Union[bool, str]:
        with self.__str_mutex:
            if fid_num in self.__str_map:
                return (True, self.__str_map[fid_num])
            else:
                return (False, None)

    def __get_fid_bool(self, fid_num: int) -> Union[bool, bool]:
        with self.__bool_mutex:
            if fid_num in self.__bool_map:
                return (True, self.__bool_map[fid_num])
            else:
                return (False, None)

    def __get_fid_other(self, fid_num: int) -> Union[bool, Any]:
        pass
