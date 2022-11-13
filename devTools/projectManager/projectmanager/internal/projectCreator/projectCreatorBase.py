from abc import ABC, abstractmethod
from pathlib import Path
import logging
import shutil
import jinja2
import os
import stat

class projectCreatorBase(ABC):
    def __init__(self, project_name: str, project_path: str, logger: logging.Logger):
        self._project_name: str = project_name
        self._project_path: Path = Path(project_path)
        self._logger: logging.Logger = logger

        # remove space
        self._project_name = self._project_name.replace(" ", "_")

    @abstractmethod
    def create_project(self, project_type: str):
        pass
