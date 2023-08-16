content_st = """
# Imports
import argparse
import logging

import sfdevtoolslight.observability.log_helper as lh

# Functions
def init_argparse(description: str = "") -> argparse.Namespace:
    \"\"\"! initial argument parser

    @param description Argument parser description

    @return argument parser
    \"\"\"
    parser = argparse.ArgumentParser(description=description)
    # parser.add_argument("-a", "--action", required=True)
    # parser.add_argument("-l", "--lang", required=True)
    # parser.add_argument("-pn", "--projectName", default="")
    return parser.parse_args()

def main() -> None:
    \"\"\"! {{ project_name }} main function

    @return None
    \"\"\"
    logger = lh.init_logger(logger_name="{{ project_name }}_logger", is_json_output=False)
    args = init_argparse(description="{{ description }}")
    logger.info(f"We get args: {args}")

    # Here put your logic

if __name__ == "__main__":
    main()
"""
