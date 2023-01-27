
import argparse
import sfdevtools.observability.log_helper as lh
import logging

def init_argparse() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="sfdevtools Inputs")
    # parser.add_argument("-a", "--action", required=True)
    # parser.add_argument("-l", "--lang", required=True)
    # parser.add_argument("-pn", "--projectName", default="")
    return parser.parse_args()

def main():
    logger = lh.init_logger(logger_name="sfdevtools_logger", is_json_output=False)
    args = init_argparse()
    logger.info(f"We get args: {args}")

    # Here put your logic

if __name__ == "__main__":
    main()
