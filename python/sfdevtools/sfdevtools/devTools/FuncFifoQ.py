import threading
from typing import List, Dict, Tuple
import logging
from functools import partial
import signal

from sfdevtools.devTools.MsgQ import MsgQ

class FuncFifoQ(object):
    def __init__(self
                 , logger: logging.Logger
                 , pool_size: int = 1):
        self.__logger: logging.Logger = logger
        self.__threads: List[threading.Thread] = list()
        self.__msg_q: MsgQ = MsgQ()
        self.__mutex: threading.Lock = threading.Lock()
        self.__is_running: bool = False

        # init threads
        for i in range(pool_size):
            self.__threads.append(threading.Thread(target=self.main))

        signal.signal(signal.SIGINT, self.__cleanup)

    def start_q(self) -> None:
        with self.__mutex:
            self.__is_running = True

        for th in self.__threads:
            th.start()

    def stop_q(self) -> None:
        if not self.__is_q_running():
            return

        with self.__mutex:
            self.__is_running = False

        # notify all the threads
        for th in self.__threads:
            self.push_func(partial(self.__dummy_func))

        for th in self.__threads:
            th.join()

    def push_func(self, user_func):
        self.__msg_q.push(user_func)

    def main(self):
        self.__logger.info("Start")

        while True:
            if not self.__is_q_running():
                break

            user_func = self.__msg_q.get()
            user_func()

            if not self.__is_q_running():
                break

        self.__logger.info("End")

    def __is_q_running(self) -> bool:
        with self.__mutex:
            return self.__is_running

    def __dummy_func(self) -> None:
        pass

    def __cleanup(self, signum, frame):
        self.stop_q()
        exit(0)
