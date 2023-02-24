import time
from typing import List, Dict, Tuple, Any, Deque

class DiscontinueSeelp(object):
    def __init__(self
                 , sleep_time_ms: int
                 , d_sleep_time_ms: int = 100):
        self.__sleep_time_ms: int = sleep_time_ms
        self.__d_sleep_time_ms: int = d_sleep_time_ms

    def sleep(self, user_fun: Any) -> None:
        cur_sleep_time_ms: int = 0
        while cur_sleep_time_ms < self.__sleep_time_ms:
            next_sleep_time_ms = min(self.__sleep_time_ms - cur_sleep_time_ms, self.__d_sleep_time_ms)
            time.sleep(next_sleep_time_ms / 1000.0)
            cur_sleep_time_ms += next_sleep_time_ms

            if not user_fun():
                return
