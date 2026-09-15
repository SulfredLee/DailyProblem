from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional


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

        files = folder.rglob("*.mp3") if recursive else folder.glob("*.mp3")
        count = 0

        for source in sorted(files):
            if not source.is_file() or source.is_symlink():
                continue

            new_name = self.convert_name(source.name)
            if new_name is None:
                continue

            destination = source.with_name(new_name)

            if destination.exists() or destination.is_symlink():
                print(f"SKIP (destination exists): {destination}")
                continue

            if dry_run:
                print(f"PREVIEW: {source.name} -> {new_name}")
            else:
                continue
                try:
                    source.rename(destination)
                    print(f"RENAMED: {source.name} -> {new_name}")
                except OSError as error:
                    print(f"ERROR: {source.name}: {error}")
                    continue

            count += 1

        print(f"\n{count} file(s) {'matched' if dry_run else 'renamed'}.")
