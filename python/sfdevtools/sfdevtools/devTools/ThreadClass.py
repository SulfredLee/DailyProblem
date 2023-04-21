import logging
import threading
import signal

import sfdevtools.observability.log_helper as lh
import sfdevtools.devTools.AtomicData as AtomicData

class ThreadClass(object):
    def __init__(self):
        self.__logger: logging.Logger = None
        self._is_running: AtomicData.AtomicData = None
        self._th: threading = None

    # override
    def init_component(self
                       , logger: logging.Logger):
        self.__logger = logger
        self._is_running = AtomicData.AtomicData()
        self._is_running.save(user_data=True)

        self._th = threading.Thread(target=self._main)
        signal.signal(signal.SIGINT, self._cleanup)

    # override
    def _user_main(self):
        raise NotImplementedError

    def start_th(self) -> None:
        self._th.start()

    def stop_th(self) -> None:
        if not self._is_running.get():
            return

        self._is_running.save(user_data=False)
        self._th.join()

    def _main(self):
        self.__logger.info("Start")

        while self._is_running.get():
            if not self._is_running.get():
                break

            # TODO - add user processing logic
            self._user_main()

            if not self._is_running.get():
                break

        self.__logger.info("End")

    def _cleanup(self, signum, frame):
        self.stop_th()
        exit(0)
