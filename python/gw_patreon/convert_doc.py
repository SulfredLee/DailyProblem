import argparse
import logging
import re
from pathlib import Path
from typing import Any, Optional


if __package__:
    from .base_name_converter import BaseNameConverter
else:
    from base_name_converter import BaseNameConverter


class TeaDoctorNameConverter(BaseNameConverter):
    PATTERN = re.compile(
        r"茶博士怪論\s+"
        r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})\s+"
        r"第(?P<episode>\d+)集[\s_\\]*"
        r"Part\s*(?P<part>\d+)\s+mp3聲音檔案\.mp3",
        re.IGNORECASE,
    )

    def convert_name(self, name: str) -> Optional[str]:
        match = self.PATTERN.fullmatch(name)
        if not match:
            return None

        year, month, day = match.group("year", "month", "day")
        episode = int(match["episode"])
        part = int(match["part"])
        return f"{year}{month}{day}_{episode}_{part:03d} 茶博士怪論.mp3"


def get_args() -> Any:
    parser = argparse.ArgumentParser(
        description="Rename 茶博士怪論 MP3 files."
    )
    parser.add_argument("folder", type=Path, help="Folder containing MP3 files")
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Preview changes without renaming files",
    )
    parser.add_argument(
        "--recursive", action="store_true",
        help="Also scan subfolders",
    )

    return parser.parse_args()

def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
    )
    args = get_args()
    converter = TeaDoctorNameConverter()

    converter.run(args.folder, dry_run=args.dry_run, recursive=args.recursive)


if __name__ == "__main__":
    main()
