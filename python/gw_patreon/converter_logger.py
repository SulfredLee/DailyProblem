import inspect
import logging
from pathlib import Path
from threading import get_ident


class ConverterLogger:
    def __init__(self) -> None:
        self._logger = logging.getLogger(__name__)

    def _log(self, level: int, message: str) -> None:
        frame = inspect.currentframe()
        caller = frame.f_back.f_back
        location = (
            f"{Path(caller.f_code.co_filename).name}:"
            f"{caller.f_code.co_name}:{caller.f_lineno}"
        )
        self._logger.log(
            level, f"{location} [thread={get_ident()}] {message}"
        )

    def info(self, message: str) -> None:
        self._log(logging.INFO, message)

    def error(self, message: str) -> None:
        self._log(logging.ERROR, message)