# poetry run python -m unittest

# Imports
import unittest
import sfdevtools.observability.log_helper as lh
import logging
from sfdevtools.devTools.SingletonDoubleChecked import SDC
import sfdevtools.storage.objectStorage.AWSObjectStorage as aws_obj_storage
import sfdevtools.devTools.DatetimeTools as dtt
import pandas as pd

# Functions
class Test_peacock(unittest.TestCase):
    def test_example(self):
        """! Example Test funtions
        """
        self.assertEqual("test".upper(), "TEST")

    def test_demo_SDC(self):
        """! Demo double check lock class
        """
        logger = lh.init_logger(logger_name="sfdevtools_logger", is_json_output=False)
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

    def test_demo_logger_to_logstash(self):
        """! Demo show how to send log to logstash
        """
        logger = lh.init_logger(logger_name="connection_tester_logger"
                                , is_json_output=False
                                , is_print_to_console=True
                                , is_print_to_logstash=True
                                , logstash_host="the host name"
                                , logstash_port=5960
                                , logstash_user_tags=["Test001", "Test002"])
        logger.info("Test Message from test")
        logger.error("Test Message from test")
        logger.warning("Test Message from test")

    def test_demo_logger_with_json_output(self):
        """! Demo show json output
        """
        logger = lh.init_logger(logger_name="connection_tester_logger"
                                , is_json_output=True
                                , is_print_to_console=True
                                , is_print_to_logstash=False)
        logger.info("Test Message from test")
        logger.error("Test Message from test")
        logger.warning("Test Message from test")

    def test_save_file_to_cloud(self):
        header = ["H_1", "H_2", "H_3"]
        content = [["r1 c1", "r1 c2", "r1 c3"]
                   , ["r2 c1", "r2 c2", "r2 c3"]]
        df = pd.DataFrame(content, columns=header)
        is_debug = False
        if is_debug:
            return
        logger = lh.init_logger(logger_name="s3_tester_logger", is_print_to_console=True)
        s3_storage = aws_obj_storage.AWSObjectStorage(logger=logger)
        file_name = "test_file_name.csv"
        s3_storage.upload_file_from_memory(file_name=file_name
                                           , file_content=df.to_csv()
                                           , bucket_name="dc-databucket"
                                           , obj_name=f"other/{dtt.get_current_date()}/{dtt.get_current_datetime()}_{file_name}")
if __name__ == "__main__":
    unittest.main()
