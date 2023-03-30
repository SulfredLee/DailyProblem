import logging
from typing import List, Dict, Tuple, Union, Any
import threading
from datetime import datetime

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
        self.__d_int32_map: Dict[int, Union[int, datetime]] = dict()
        self.__d_int64_map: Dict[int, Union[int, datetime]] = dict()
        self.__d_float_map: Dict[int, Union[float, datetime]] = dict()
        self.__d_double_map: Dict[int, Union[float, datetime]] = dict()
        self.__d_string_map: Dict[int, Union[str, datetime]] = dict()
        self.__d_bool_map: Dict[int, Union[bool, datetime]] = dict()

        self.__save_map: Dict[int, Any] = dict()
        self.__get_map: Dict[int, Any] = dict()
        self.__save_other_map: Dict[int, Any] = dict()
        self.__get_other_map: Dict[int, Any] = dict()
        self.__bucket_size = 10000
        self.__update_cb: Any = None
        self.__get_parent_dcache_fun: Any = None
        self.__page_id: str = None

    def init_component(self
                       , logger: logging.Logger
                       , update_cb: Any
                       , get_parent_dcache_fun: Any
                       , page_id: str
                       , save_other_map: Dict
                       , get_other_map: Dict) -> None:
        self.__logger = logger
        self.__get_parent_dcache_fun = get_parent_dcache_fun
        self.__update_cb = update_cb
        self.__save_other_map = save_other_map
        self.__get_other_map = get_other_map
        self.__page_id = page_id

        self.__save_map = {
            0: self.__save_fid_int32
            , 1: self.__save_fid_int64
            , 2: self.__save_fid_float
            , 3: self.__save_fid_double
            , 4: self.__save_fid_string
            , 5: self.__save_fid_other
            , 6: self.__save_fid_bool
            , 7: self.__save_fid_d_int32
            , 8: self.__save_fid_d_int64
            , 9: self.__save_fid_d_float
            , 10: self.__save_fid_d_double
            , 11: self.__save_fid_d_string
            , 12: self.__save_fid_d_bool
        }
        self.__get_map = {
            0: self.__get_fid_int32
            , 1: self.__get_fid_int64
            , 2: self.__get_fid_float
            , 3: self.__get_fid_double
            , 4: self.__get_fid_string
            , 5: self.__get_fid_other
            , 6: self.__get_fid_bool
            , 7: self.__get_fid_d_int32
            , 8: self.__get_fid_d_int64
            , 9: self.__get_fid_d_float
            , 10: self.__get_fid_d_double
            , 11: self.__get_fid_d_string
            , 12: self.__get_fid_d_bool
        }

    def save_fid(self, fid_num: int, fid_value: Any) -> None:
        bucket_num = int((fid_num - 1) / self.__bucket_size)
        if bucket_num not in self.__save_map:
            return None
        is_new = self.__save_map[bucket_num](fid_num=fid_num, fid_value=fid_value)
        if is_new is not None and is_new and self.__update_cb is not None:
            self.__update_cb(dcache=self.__get_parent_dcache_fun(), msg_id=self.__page_id, fid_num=fid_num, fid_value=fid_value)

    def get_page_id(self) -> str:
        return self.__page_id

    def get_fids(self) -> List[Union[int, Any]]:
        result_list: List[Union[int, Any]] = list()
        with self.__int_mutex:
            for fid_num, v in self.__int32_map.items():
                result_list.append((fid_num, v))
            for fid_num, v in self.__d_int32_map.items():
                result_list.append((fid_num, v))

            for fid_num, v in self.__int64_map.items():
                result_list.append((fid_num, v))
            for fid_num, v in self.__d_int64_map.items():
                result_list.append((fid_num, v))

        with self.__float_mutex:
            for fid_num, v in self.__float_map.items():
                result_list.append((fid_num, v))
            for fid_num, v in self.__d_float_map.items():
                result_list.append((fid_num, v))

            for fid_num, v in self.__double_map.items():
                result_list.append((fid_num, v))
            for fid_num, v in self.__d_double_map.items():
                result_list.append((fid_num, v))

        with self.__str_mutex:
            for fid_num, v in self.__string_map.items():
                result_list.append((fid_num, v))
            for fid_num, v in self.__d_string_map.items():
                result_list.append((fid_num, v))

        with self.__bool_mutex:
            for fid_num, v in self.__bool_map.items():
                result_list.append((fid_num, v))
            for fid_num, v in self.__d_bool_map.items():
                result_list.append((fid_num, v))

        return result_list

    def get_fid(self, fid_num: int) -> Union[bool, Any]:
        bucket_num = int((fid_num - 1) / self.__bucket_size)
        if bucket_num not in self.__get_map:
            return (False, None)

        return (True, self.__get_map[bucket_num](fid_num=fid_num))

    def __save_fid_int32(self, fid_num: int, fid_value: int) -> bool:
        return self.__save_fid_imp(mutex=self.__int_mutex, the_map=self.__int32_map, fid_num=fid_num, fid_value=fid_value)

    def __save_fid_int64(self, fid_num: int, fid_value: int) -> bool:
        return self.__save_fid_imp(mutex=self.__int_mutex, the_map=self.__int64_map, fid_num=fid_num, fid_value=fid_value)

    def __save_fid_float(self, fid_num: int, fid_value: float) -> bool:
        return self.__save_fid_imp(mutex=self.__float_mutex, the_map=self.__float_map, fid_num=fid_num, fid_value=fid_value)

    def __save_fid_double(self, fid_num: int, fid_value: float) -> bool:
        return self.__save_fid_imp(mutex=self.__float_mutex, the_map=self.__double_map, fid_num=fid_num, fid_value=fid_value)

    def __save_fid_string(self, fid_num: int, fid_value: str) -> bool:
        return self.__save_fid_imp(mutex=self.__str_mutex, the_map=self.__str_map, fid_num=fid_num, fid_value=fid_value)

    def __save_fid_bool(self, fid_num: int, fid_value: float) -> bool:
        return self.__save_fid_imp(mutex=self.__bool_mutex, the_map=self.__bool_map, fid_num=fid_num, fid_value=fid_value)

    def __save_fid_imp(self, mutex: threading.Lock, the_map: Dict[int, Any], fid_num: int, fid_value: Any) -> bool:
        is_new = False
        with mutex:
            if fid_num not in the_map:
                is_new = True

                the_map[fid_num] = fid_value
            else:
                if the_map[fid_num] == fid_value:
                    is_new = False
                else:
                    is_new = True

                    the_map[fid_num] = fid_value

        return is_new

    def __save_fid_d_int32(self, fid_num: int, fid_value: int) -> bool:
        return self.__save_fid_d_imp(mutex=self.__int_mutex, the_map=self.__d_int32_map, fid_num=fid_num, fid_value=fid_value)

    def __save_fid_d_int64(self, fid_num: int, fid_value: int) -> bool:
        return self.__save_fid_d_imp(mutex=self.__int_mutex, the_map=self.__d_int64_map, fid_num=fid_num, fid_value=fid_value)

    def __save_fid_d_float(self, fid_num: int, fid_value: float) -> bool:
        return self.__save_fid_d_imp(mutex=self.__float_mutex, the_map=self.__d_float_map, fid_num=fid_num, fid_value=fid_value)

    def __save_fid_d_double(self, fid_num: int, fid_value: float) -> bool:
        return self.__save_fid_d_imp(mutex=self.__float_mutex, the_map=self.__d_double_map, fid_num=fid_num, fid_value=fid_value)

    def __save_fid_d_string(self, fid_num: int, fid_value: str) -> bool:
        return self.__save_fid_d_imp(mutex=self.__str_mutex, the_map=self.__d_str_map, fid_num=fid_num, fid_value=fid_value)

    def __save_fid_d_bool(self, fid_num: int, fid_value: float) -> bool:
        return self.__save_fid_d_imp(mutex=self.__bool_mutex, the_map=self.__d_bool_map, fid_num=fid_num, fid_value=fid_value)

    def __save_fid_d_imp(self, mutex: threading.Lock, the_map: Dict[int, Any], fid_num: int, fid_value: Any) -> bool:
        is_new = False
        with mutex:
            if fid_num not in the_map:
                is_new = True

                the_map[fid_num] = fid_value
            else:
                if the_map[fid_num][0] == fid_value[0]\
                   or the_map[fid_num][1] == fid_value[1]:
                    is_new = False
                else:
                    is_new = True

                    the_map[fid_num] = fid_value

        return is_new

    def __save_fid_other(self, fid_num: int, fid_value: Any) -> None:
        with self.__other_mutex:
            if fid_num not in self.__save_other_map:
                return None

            self.__save_other_map[fid_num](fid_value)
            return None

    def __get_fid_int32(self, fid_num: int) -> Union[bool, int]:
        return self.__get_fid_imp(mutex=self.__int_mutex, the_map=self.__int32_map, fid_num=fid_num)

    def __get_fid_int64(self, fid_num: int) -> Union[bool, int]:
        return self.__get_fid_imp(mutex=self.__int_mutex, the_map=self.__int64_map, fid_num=fid_num)

    def __get_fid_float(self, fid_num: int) -> Union[bool, float]:
        return self.__get_fid_imp(mutex=self.__float_mutex, the_map=self.__float_map, fid_num=fid_num)

    def __get_fid_double(self, fid_num: int) -> Union[bool, float]:
        return self.__get_fid_imp(mutex=self.__float_mutex, the_map=self.__double_map, fid_num=fid_num)

    def __get_fid_string(self, fid_num: int) -> Union[bool, str]:
        return self.__get_fid_imp(mutex=self.__str_mutex, the_map=self.__str_map, fid_num=fid_num)

    def __get_fid_bool(self, fid_num: int) -> Union[bool, bool]:
        return self.__get_fid_imp(mutex=self.__bool_mutex, the_map=self.__bool_map, fid_num=fid_num)

    def __get_fid_imp(self, mutex: threading.Lock, the_map: Dict[int, Any], fid_num: int) -> Union[bool, Any]:
        with mutex:
            if fid_num in the_map:
                return (True, the_map[fid_num])
            else:
                return (False, None)

    def __get_fid_d_int32(self, fid_num: int) -> Union[bool, int]:
        return self.__get_fid_d_imp(mutex=self.__int_mutex, the_map=self.__d_int32_map, fid_num=fid_num)

    def __get_fid_d_int64(self, fid_num: int) -> Union[bool, int]:
        return self.__get_fid_d_imp(mutex=self.__int_mutex, the_map=self.__d_int64_map, fid_num=fid_num)

    def __get_fid_d_float(self, fid_num: int) -> Union[bool, float]:
        return self.__get_fid_d_imp(mutex=self.__float_mutex, the_map=self.__d_float_map, fid_num=fid_num)

    def __get_fid_d_double(self, fid_num: int) -> Union[bool, float]:
        return self.__get_fid_d_imp(mutex=self.__float_mutex, the_map=self.__d_double_map, fid_num=fid_num)

    def __get_fid_d_string(self, fid_num: int) -> Union[bool, str]:
        return self.__get_fid_d_imp(mutex=self.__str_mutex, the_map=self.__d_str_map, fid_num=fid_num)

    def __get_fid_d_bool(self, fid_num: int) -> Union[bool, bool]:
        return self.__get_fid_d_imp(mutex=self.__bool_mutex, the_map=self.__d_bool_map, fid_num=fid_num)

    def __get_fid_d_imp(self, mutex: threading.Lock, the_map: Dict[int, Any], fid_num: int) -> Union[bool, Union[Any, datetime]]:
        with mutex:
            if fid_num in the_map:
                return (True, the_map[fid_num])
            else:
                return (False, None)

    def __get_fid_other(self, fid_num: int) -> Union[bool, Any]:
        with self.__other_mutex:
            if fid_num in self.__get_other_map:
                return (True, self.__get_other_map[fid_num]())
            else:
                return (False, None)
