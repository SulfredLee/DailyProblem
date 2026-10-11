from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional
from converter_logger import ConverterLogger


class BaseNameConverter(ABC):
    """Shared file-processing workflow with subclass-specific name conversion."""

    @abstractmethod
    def convert_name(self, name: str) -> Optional[str]:
        """Return the converted filename, or None if the pattern does not match."""
        raise NotImplementedError

    def run(
        self, folder: Path, dry_run: bool = False, recursive: bool = False
    ) -> None:
        folder = folder.expanduser()
        if not folder.is_dir():
            raise ValueError(f"Folder does not exist: {folder}")

        list_files = folder.rglob if recursive else folder.glob
        files = (
            path
            for pattern in ("*.mp3", "*.m4a")
            for path in list_files(pattern)
        )
        count = 0
        logger = ConverterLogger()

        for source in sorted(files):
            if not source.is_file() or source.is_symlink():
                continue

            new_name = self.convert_name(source.name)
            if new_name is None:
                continue

            destination = source.with_name(new_name)

            if destination.exists() or destination.is_symlink():
                logger.info(f"SKIP (destination exists): {destination}")
                continue

            if dry_run:
                logger.info(f"PREVIEW: {source.name} -> {new_name}")
            else:
                try:
                    source.rename(destination)
                    logger.info(f"RENAMED: {source.name} -> {new_name}")
                except OSError as error:
                    logger.error(f"ERROR: {source.name}: {error}")
                    continue

            count += 1

        logger.info(f"{count} file(s) {'matched' if dry_run else 'renamed'}.")
