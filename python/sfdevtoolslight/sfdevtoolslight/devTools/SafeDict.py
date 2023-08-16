from typing import List, Dict, Tuple, Union, Any
import threading
import copy

class SafeDict(object):
    def __init__(self):
        self.__dict: Dict[Any, Any] = dict()
        self.__mutex: threading.Lock = threading.Lock()

    def upsert_ele(self, key: Any, value: Any) -> None:
        with self.__mutex:
            self.__dict[key] = value

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
