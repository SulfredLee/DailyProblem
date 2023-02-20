# poetry run python -m unittest

# Imports
import unittest
import logging
import pandas as pd
import inspect
from functools import partial
from time import sleep
import datetime
from typing import List, Dict, Any

from sfdevtools.devTools.SingletonDoubleChecked import SDC
import sfdevtools.observability.log_helper as lh
import sfdevtools.storage.objectStorage.AWSObjectStorage as aws_obj_storage
import sfdevtools.storage.relationalDBStorage.PostgresDBCtrl as postDBCtrl
import sfdevtools.devTools.DatetimeTools as dtt
import sfdevtools.devTools.FuncFifoQ as FuncFifoQ
from sfdevtools.data_cache.DStrategy import DStrategy
from sfdevtools.data_cache.DComponents import StrategyInsight
from sfdevtools.data_cache.DCacheManager import DCacheManager
from sfdevtools.data_cache.DCache import DCache
import sfdevtools.grpc_protos.ts_cop_pb2 as ts_cop_pb2
import sfdevtools.grpc_protos.ts_cop_pb2_grpc as ts_cop_pb2_grpc
import sfdevtools.data_cache.DConverter as dconv

# Functions
class Test_peacock(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.__logger = lh.init_logger(logger_name="sfdevtools_logger", is_json_output=False)

        self.__test_config = {
            "test_example": False
            , "test_demo_SDC": False
            , "test_demo_logger_to_logstash": False
            , "test_demo_logger_with_json_output": False
            , "test_save_file_to_cloud": False
            , "test_db_connection": False
            , "test_func_fifo_q": False
            , "test_dcache": True
            , "test_ts_cop": False
            , "test_pg": False
        }

        if not self.__test_config[self._testMethodName]:
            self.__logger.info(f"Skip test {self._testMethodName}")
            return

    def tearDown(self):
        pass

    def test_example(self):
        """! Example Test funtions
        """
        if not self.__test_config[inspect.stack()[0][3]]:
            return
        self.assertEqual("test".upper(), "TEST")

    def test_demo_SDC(self):
        """! Demo double check lock class
        """
        if not self.__test_config[inspect.stack()[0][3]]:
            return
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
        if not self.__test_config[inspect.stack()[0][3]]:
            return
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
        if not self.__test_config[inspect.stack()[0][3]]:
            return
        logger = lh.init_logger(logger_name="connection_tester_logger"
                                , is_json_output=True
                                , is_print_to_console=True
                                , is_print_to_logstash=False)
        logger.info("Test Message from test")
        logger.error("Test Message from test")
        logger.warning("Test Message from test")

    def test_save_file_to_cloud(self):
        if not self.__test_config[inspect.stack()[0][3]]:
            return
        header = ["H_1", "H_2", "H_3"]
        content = [["r1 c1", "r1 c2", "r1 c3"]
                   , ["r2 c1", "r2 c2", "r2 c3"]]
        df = pd.DataFrame(content, columns=header)
        logger = lh.init_logger(logger_name="s3_tester_logger", is_print_to_console=True)
        s3_storage = aws_obj_storage.AWSObjectStorage(logger=logger)
        file_name = "test_file_name.csv"
        s3_storage.upload_file_from_memory(file_name=file_name
                                           , file_content=df.to_csv()
                                           , bucket_name="dc-databucket"
                                           , obj_name=f"other/{dtt.get_current_date()}/{dtt.get_current_datetime()}_{file_name}")

    def test_db_connection(self):
        if not self.__test_config[inspect.stack()[0][3]]:
            return
        db_ctrl = postDBCtrl.PostgresDBCtrl(db_user=os.getenv("DB_USER", default="postgres")
                                            , db_pw=os.getenv("DB_PW", default="dummy pw")
                                            , db_host=os.getenv("DB_HOST", default="dummy host")
                                            , db_port=os.getenv("DB_PORT", default="5432")
                                            , db_name=os.getenv("DB_NAME", default="postgres")
                                            , db_schema=os.getenv("DB_SCHEMA", default="refdb")
                                            , logger=self.__logger)

        # self.__logger.info(type(db_ctrl.get_classes()))
        # self.__logger.info(type(db_ctrl.get_tables()))
        # self.__logger.info(type(db_ctrl.get_session()))

    def test_func_fifo_q(self):
        if not self.__test_config[inspect.stack()[0][3]]:
            return

        logger = lh.init_logger(logger_name="test_func_fifo_q", is_print_to_console=True, is_json_output=False)
        func_q: FuncFifoQ.FuncFifoQ = FuncFifoQ.FuncFifoQ(logger=logger, pool_size=10)
        func_q.start_q()
        for i in range(10):
            func_q.push_func(partial(self.__func_test_foo, i, "hi"))

        logger.info("Before sleep")
        sleep(2)
        logger.info("After sleep")

        func_q.stop_q()

    def __func_test_foo(self, a: int, b: str):
        logger = lh.init_logger(logger_name="test_func_fifo_q", is_print_to_console=True, is_json_output=False)
        logger.info(f"Hi from thread: {a}")

    def __cop_callback(self
                       , topic: str
                       , cop: ts_cop_pb2.Cop
                       , fid_num: int
                       , fid_value: Any) -> None:
        logger = lh.init_logger(logger_name="test_dcache", is_print_to_console=True, is_json_output=False)
        logger.info(f"topic: {topic}, fid_num: {fid_num}, fid_value: {fid_value}")
        dcache_manager = DCacheManager()
        dcache_manager.init_component(logger=logger)
        dcache = dcache_manager.create_cache(cache_name="Test_True")

        # save to cache
        dcache_manager.save_fid(cache_name=cop.sender
                                , msg_id=cop.msg_id
                                , msg_type=cop.msg_type
                                , fid_num=fid_num
                                , fid_value=fid_value)

        dcache_ret = dcache.get_fid(msg_id=cop.msg_id
                                    , msg_type=cop.msg_type
                                    , fid_num=fid_num)
        manager_ret = dcache_manager.get_fid(cache_name=cop.sender
                                             , msg_id=cop.msg_id
                                             , msg_type=cop.msg_type
                                             , fid_num=fid_num)

        self.assertEqual((True, (True, fid_value)), dcache_ret)
        self.assertEqual((True, (True, (True, fid_value))), manager_ret)
        logger.info(dcache_ret)
        if fid_num == ts_cop_pb2.Cop.FidNum.SI\
           or fid_num == ts_cop_pb2.Cop.FidNum.Order:
            for si_ele in dcache_ret[1][1]:
                logger.info(si_ele)

    def test_dcache(self):
        if not self.__test_config[inspect.stack()[0][3]]:
            return

        logger = lh.init_logger(logger_name="test_dcache", is_print_to_console=True, is_json_output=False)
        # prepare cop
        cop = ts_cop_pb2.Cop()
        cop.msg_id = "Test_True"
        cop.msg_type = ts_cop_pb2.Cop.MsgType.Strategy
        cop.sender = "Test_True"
        cop.instance_id = 1
        cop.seq_num = 1
        cop.created_time = datetime.datetime.utcnow().timestamp()

        # ci
        cop.ci_map[ts_cop_pb2.Cop.FidNum.CI].ci_list.append(ts_cop_pb2.CI(value="hello world"))
        cop.ci_map[ts_cop_pb2.Cop.FidNum.CI].ci_list.append(ts_cop_pb2.CI(value="hello world 2"))
        # si
        si_ele = ts_cop_pb2.SI()
        si_ele.symbol = "Symbol A";
        si_ele.ratio = 10.01
        si_ele.parent_id = "ci.adfavniIdh12N";
        si_ele.si_id = "si.aivahmnvsao123hdnK";
        si_ele.created = datetime.datetime.utcnow().timestamp()
        si_ele.last_update = si_ele.created
        si_ele.strategy_name = "Test"
        si_ele.live_mode = True
        si_ele.execution_id = "sadfihzv987yasdf"
        si_ele.symbol_id = "Symbol A ID";
        cop.si_map[ts_cop_pb2.Cop.FidNum.SI].si_list.append(si_ele)
        si_ele2 = ts_cop_pb2.SI()
        si_ele2.symbol = "Symbol B";
        si_ele2.ratio = 11.01
        si_ele2.parent_id = "ci.adfavniIdh12N";
        si_ele2.si_id = "si.aivahmnvsao123hdnK";
        si_ele2.created = datetime.datetime.utcnow().timestamp()
        si_ele2.last_update = si_ele.created
        si_ele2.strategy_name = "Test"
        si_ele2.live_mode = True
        si_ele2.execution_id = "sadfihzv987yasdf"
        si_ele2.symbol_id = "Symbol B ID";
        cop.si_map[ts_cop_pb2.Cop.FidNum.SI].si_list.append(si_ele2)
        # orders
        ord_ele = ts_cop_pb2.TSOrder()
        ord_ele.symbol = "Symbol A"
        ord_ele.quantity = 100
        ord_ele.fill_quantity = 50
        ord_ele.parent_id = "si.aivahmnvsao123hdnK"
        ord_ele.order_id = "ord.cxivhsdfn234h"
        ord_ele.qc_order_id = 1
        ord_ele.created = datetime.datetime.utcnow().timestamp()
        ord_ele.last_update = ord_ele.created
        ord_ele.strategy_name = "Test"
        ord_ele.live_mode = True
        ord_ele.execution_id = "sadfihzv987yasdf";
        ord_ele.order_status = "PFilled";
        ord_ele.execution_broker = "IB";
        ord_ele.clearing_broker = "IB";
        ord_ele.account = "Dummy";
        ord_ele.price = 10.9;
        ord_ele.fee = 0.01;
        ord_ele.exchange = "US";
        ord_ele.ccy = "USD";
        ord_ele.fee_ccy = "USD";
        ord_ele.symbol_id = "Symbol A ID";
        cop.order_map[ts_cop_pb2.Cop.FidNum.Order].order_list.append(ord_ele)
        # trades
        trd_ele = ts_cop_pb2.TSTrade()
        trd_ele.symbol = "Symbol A"
        trd_ele.quantity = 50
        trd_ele.parent_id = "ord.cxivhsdfn234h"
        trd_ele.trade_id = "trd.dksiv93DJvn"
        trd_ele.created = datetime.datetime.utcnow().timestamp()
        trd_ele.last_update = trd_ele.created
        trd_ele.strategy_name = "Test"
        trd_ele.live_mode = True
        trd_ele.execution_id = "sadfihzv987yasdf"
        trd_ele.trade_status = "PFilled"
        trd_ele.execution_broker = "IB"
        trd_ele.clearing_broker = "IB"
        trd_ele.fx_ratio = 0.19
        trd_ele.account = "IB"
        trd_ele.price = 10.98;
        trd_ele.fee = 0.01;
        trd_ele.exchange = "US";
        trd_ele.ccy = "USD";
        trd_ele.fee_ccy = "USD";
        trd_ele.symbol_id = "Symbol A ID";
        cop.trade_map[ts_cop_pb2.Cop.FidNum.Trade].trade_list.append(trd_ele)

        topic = "Test_True"
        # int32
        for fid_num, fid_value in cop.int32_map.items():
            self.__cop_callback(topic=topic, cop=cop, fid_num=fid_num, fid_value=fid_value)
        # int64
        for fid_num, fid_value in cop.int64_map.items():
            self.__cop_callback(topic=topic, cop=cop, fid_num=fid_num, fid_value=fid_value)
        # float
        for fid_num, fid_value in cop.float_map.items():
            self.__cop_callback(topic=topic, cop=cop, fid_num=fid_num, fid_value=fid_value)
        # double
        for fid_num, fid_value in cop.double_map.items():
            self.__cop_callback(topic=topic, cop=cop, fid_num=fid_num, fid_value=fid_value)
        # string
        for fid_num, fid_value in cop.string_map.items():
            self.__cop_callback(topic=topic, cop=cop, fid_num=fid_num, fid_value=fid_value)
        # bool
        for fid_num, fid_value in cop.bool_map.items():
            self.__cop_callback(topic=topic, cop=cop, fid_num=fid_num, fid_value=fid_value)
        # order
        for fid_num, fid_value in cop.order_map.items():
            ts_orders = [dconv.conv_cop_order_2_TS_Order(ord_ele=ele) for ele in fid_value.order_list]
            self.__cop_callback(topic=topic, cop=cop, fid_num=fid_num, fid_value=ts_orders)
        # trade
        for fid_num, fid_value in cop.trade_map.items():
            ts_trades = [dconv.conv_cop_trade_2_TS_Trade(trd_ele=ele) for ele in fid_value.trade_list]
            self.__cop_callback(topic=topic, cop=cop, fid_num=fid_num, fid_value=ts_trades)
        # si
        for fid_num, fid_value in cop.si_map.items():
            si_list = [dconv.conv_cop_si_2_SI(si_ele=ele) for ele in fid_value.si_list]
            self.__cop_callback(topic=topic, cop=cop, fid_num=fid_num, fid_value=si_list)
        # ci
        for fid_num, fid_value in cop.ci_map.items():
            for ci in fid_value.ci_list:
                self.__cop_callback(topic=topic, cop=cop, fid_num=fid_num, fid_value=ci.value)

    def test_ts_cop(self):
        if not self.__test_config[inspect.stack()[0][3]]:
            return

        logger = lh.init_logger(logger_name="test_ts_cop", is_print_to_console=True, is_json_output=False)

        cop = ts_cop_pb2.Cop()
        int32_map = cop.int32_map
        int32_map[10] = 20
        ci_map = cop.ci_map
        ele = ts_cop_pb2.CI(value="hello")
        ele2 = ts_cop_pb2.CI()
        ele2.value = "world"
        # insert data to repeated map
        ci_map[200].ci_list.append(ele)
        ci_map[200].ci_list.append(ele2)

        logger.info(int32_map)
        logger.info(ci_map)

        # get data from repeated map
        for k, v in ci_map.items():
            logger.info(k)
            for ele in v.ci_list:
                logger.info(ele)

    def test_pg(self):
        if not self.__test_config[inspect.stack()[0][3]]:
            return

        logger = lh.init_logger(logger_name="test_pg", is_print_to_console=True, is_json_output=False)

        def is_float(num: str) -> bool:
            try:
                float(num)
                return True
            except ValueError:
                return False

        fee = "3.001 USD"
        parts = fee.split(" ")
        if is_float(parts[0]):
            logger.info(float(parts[0]))
        if not is_float(parts[1]):
            logger.info(parts[1])

if __name__ == "__main__":
    unittest.main()
