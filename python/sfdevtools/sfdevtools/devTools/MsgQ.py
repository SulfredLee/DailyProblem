import threading
from typing import List, Dict, Tuple, Any, Deque
from collections import deque

class MsgQ(object):
    def __init__(self):
        self.__q: Deque[Any] = deque()
        self.__mutex: threading.Lock = threading.Lock()
        self.__cond: threading.Condition = threading.Condition()

    def push(self, user_data: Any):
        with self.__mutex:
            self.__q.append(user_data)

        self.__cond.acquire()
        self.__cond.notify()
        self.__cond.release()

    def get(self) -> Any:
        self.__cond.acquire()
        self.__cond.wait()
        self.__cond.release()

        with self.__mutex:
            return self.__q.popleft()
