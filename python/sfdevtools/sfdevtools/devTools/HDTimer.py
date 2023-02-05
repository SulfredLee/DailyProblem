import time
import threading

class HDTimer(object):
    def __init__(self, avg_size: int = 1):
        self.__avg_size = avg_size
        self.__lock = threading.Lock()
        self.__start_time = None
        self.__total_durationg = 0
        self.__window = list()

    def start_timer(self):
        with self.__lock:
            self.__start_time = time.time()

    def stop_timer(self):
        with self.__lock:
            diff_time = time.time() - self.__start_time
            self.__total_durationg += diff_time
            self.__window.append(diff_time)

            if len(self.__window) > self.__avg_size:
                self.__total_durationg -= self.__window[0]
                self.__window.pop(0)

    def get_avg_time(self):
        with self.__lock:
            return self.__total_durationg / max(min(len(self.__window), self.__avg_size), 1)

    def get_avg_size(self):
        return max(min(len(self.__window), self.__avg_size), 1)
