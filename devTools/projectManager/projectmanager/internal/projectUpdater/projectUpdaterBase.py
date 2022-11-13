from abc import ABC, abstractmethod
from pathlib import Path
import logging
import shutil
import jinja2
import os
import stat

class projectUpdaterBase(ABC):
    def __init__(self, module_name: str, project_path: str, logger: logging.Logger):
        self._module_name: str = module_name
        self._project_path: Path = Path(project_path)
        self._logger: logging.Logger = logger

        # remove space
        self._module_name = self._module_name.replace(" ", "_")

    @abstractmethod
    def update_project(self, project_type: str):
        pass
