import argparse
import logging
import re
from pathlib import Path
from typing import Any, Optional


if __package__:
    from .base_name_converter import BaseNameConverter
else:
    from base_name_converter import BaseNameConverter


class ScienceFrontierNameConverter(BaseNameConverter):
    PATTERN = re.compile(
        r"科學新知\s+"
        r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})\s+"
        r"Part\s*(?P<part>\d+)_\s+"
        r"(?P<title>.+?)mp3聲音檔案\.mp3",
        re.IGNORECASE,
    )
    MEMOIR_PATTERN = re.compile(
        r"科學新知\s+"
        r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})\s+"
        r"科學回憶錄：(?P<title>.+?)mp3聲音檔案\.mp3",
        re.IGNORECASE,
    )

    def convert_name(self, name: str) -> Optional[str]:
        match = self.PATTERN.fullmatch(name)
        memoir_match = match is None
        if memoir_match:
            match = self.MEMOIR_PATTERN.fullmatch(name)
            if not match:
                return None

        year, month, day = match.group("year", "month", "day")
        part = 5 if memoir_match else int(match["part"])
        # get title with first 10 char or until , . ?
        title = re.split(r"[，。？]", match["title"].strip(), maxsplit=1)[0][:10]
        return f"{year}{month}{day}_{part:03d} {title}.mp3"


def get_args() -> Any:
    parser = argparse.ArgumentParser(
        description="Rename 科學新知 MP3 files."
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
    converter = ScienceFrontierNameConverter()

    converter.run(args.folder, dry_run=args.dry_run, recursive=args.recursive)


if __name__ == "__main__":
    main()
