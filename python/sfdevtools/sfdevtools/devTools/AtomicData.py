import threading
from typing import List, Dict, Tuple, Any, Deque
import copy

class AtomicData(object):
    def __init__(self):
        self.__mutex: threading.Lock = threading.Lock()
        self.__user_data: Any = None

    def save(self, user_data: Any) -> None:
        with self.__mutex:
            self.__user_data = user_data

    def get(self) -> Any:
        with self.__mutex:
            return copy.deepcopy(self.__user_data)

    def is_same(self, other_data: Any) -> None:
        with self.__mutex:
            return self.__user_data == other_data
