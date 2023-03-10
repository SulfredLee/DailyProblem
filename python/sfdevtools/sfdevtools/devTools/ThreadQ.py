import logging
import threading
import signal

import sfdevtools.observability.log_helper as lh
import sfdevtools.devTools.HDTimer as HDTimer
import sfdevtools.devTools.MsgQ as MsgQ
import sfdevtools.devTools.AtomicData as AtomicData
import sfdevtools.devTools.DiscontinueSeelp as DSleep

class ThreadQ(object):
    def __init__(self):
        self.__logger: logging.Logger = None
        self._msg_q: MsgQ.MsgQ = None
        self._d_sleep: DSleep.DiscontinueSeelp = None
        self._is_running: AtomicData.AtomicData = None
        self._th: threading = None
        self._min_insertable_q_size: int = None

    def init_component(self
                       , logger: logging.Logger
                       , sleep_time_ms: int = 5000
                       , min_insertable_q_size: int = 100):
        self.__logger = logger
        self._msg_q = MsgQ.MsgQ()
        self._d_sleep = DSleep.DiscontinueSeelp(sleep_time_ms=sleep_time_ms)
        self._min_insertable_q_size = min_insertable_q_size
        self._is_running = AtomicData.AtomicData()
        self._is_running.save(user_data=True)

        self._th = threading.Thread(target=self._main)
        signal.signal(signal.SIGINT, self._cleanup)

    def start_th(self) -> None:
        self._th.start()

    def stop_th(self) -> None:
        if not self._is_running.get():
            return

        self._is_running.save(user_data=False)
        self._th.join()

    def _cleanup(self, signum, frame):
        self.stop_th()
        exit(0)

    # override
    def _is_time_to_aweak(self) -> bool:
        return self._is_running.get()\
            or not self._is_time_to_sleep()

    # override
    def _is_time_to_sleep(self) -> bool:
        return (self._msg_q.size()) < self._min_insertable_q_size

    # override
    def _user_main(self):
        raise NotImplementedError

    def _main(self):
        self.__logger.info("Start")

        while self._is_running.get():
            if not self._is_running.get():
                break

            if self._is_time_to_sleep():
                self._d_sleep.sleep(user_fun=self._is_time_to_aweak)
            # TODO - add user processing logic
            self._user_main()

            if not self._is_running.get():
                break

        self.__logger.info("End")
