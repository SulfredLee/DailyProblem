import threading
from typing import List, Dict, Tuple, Any, Deque
from collections import deque

class MsgQ(object):
    def __init__(self, timeout: float = None):
        self.__q: Deque[Any] = deque()
        self.__mutex: threading.Lock = threading.Lock()
        self.__cond: threading.Condition = threading.Condition()
        self.__timeout: float = timeout

    def push(self, user_data: Any):
        with self.__mutex:
            self.__q.append(user_data)

        self.__cond.acquire()
        self.__cond.notify()
        self.__cond.release()

    def get(self) -> Any:
        self.__cond.acquire()
        self.__cond.wait(timeout=self.__timeout)
        self.__cond.release()

        with self.__mutex:
            if len(self.__q) == 0:
                return None
            else:
                return self.__q.popleft()

    def get_all(self) -> List[Any]:
        with self.__mutex:
            if len(self.__q) == 0:
                return None
            else:
                out_list = list(self.__q)
                self.__q = deque()
                return out_list

    def get_all_wait(self) -> List[Any]:
        self.__cond.acquire()
        self.__cond.wait(timeout=self.__timeout)
        self.__cond.release()

        with self.__mutex:
            if len(self.__q) == 0:
                return None
            else:
                out_list = list(self.__q)
                self.__q = deque()
                return out_list

    def size(self) -> int:
        with self.__mutex:
            return len(self.__q)
