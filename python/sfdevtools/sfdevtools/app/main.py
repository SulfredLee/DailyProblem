
import argparse
import sfdevtools.observability.log_helper as lh
import logging
from sfdevtools.devTools.SingletonDoubleChecked import SDC

def demo_singleton_double_checked(logger):
    # create class X
    class X(SDC):
        pass

    # create class Y
    class Y(SDC):
        pass

    A1, A2 = X.instance(), X.instance()
    B1, B2 = Y.instance(), Y.instance()

    assert A1 is not B1
    assert A1 is A2
    assert B1 is B2

    logger.info('A1 : {}'.format(A1))
    logger.info('A2 : {}'.format(A2))
    logger.info('B1 : {}'.format(B1))
    logger.info('B2 : {}'.format(B2))

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
    demo_singleton_double_checked(logger)

if __name__ == "__main__":
    main()
