import argparse
import logging
import re
from pathlib import Path
from typing import Any, Optional


if __package__:
    from .base_name_converter import BaseNameConverter
else:
    from base_name_converter import BaseNameConverter


class NightNameConverter(BaseNameConverter):
    PATTERN = re.compile(
        r"(?P<year>\d{4})_(?P<month>\d{1,2})_(?P<day>\d{1,2})\s+"
        r".*神秘之夜》：\s*"
        r"(?P<title>.+)\.m4a",
        re.IGNORECASE,
    )

    def convert_name(self, name: str) -> Optional[str]:
        match = self.PATTERN.fullmatch(name)
        if not match:
            return None

        year = match["year"]
        month = int(match["month"])
        day = int(match["day"])
        # get title with first 10 char or until , . ?
        title = re.split(r"[，。？]", match["title"].strip(), maxsplit=1)[0][:10]
        return f"{year}{month:02d}{day:02d} {title}.m4a"


def get_args() -> Any:
    parser = argparse.ArgumentParser(
        description="Rename 異靈異異·神秘之夜 M4A files."
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
    converter = NightNameConverter()

    converter.run(args.folder, dry_run=args.dry_run, recursive=args.recursive)


if __name__ == "__main__":
    main()
