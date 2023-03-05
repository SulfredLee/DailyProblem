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
from pathlib import Path
import json
import copy

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
            "test_dcache": False
            , "test_ts_cop": False
            , "test_ci_update_check": False
            , "test_si_update_check": False
            , "test_order_update_check": False
            , "test_trade_update_check": False
            , "test_fid_update_check": True
        }

        if not self.__test_config[self._testMethodName]:
            self.__logger.info(f"Skip test {self._testMethodName}")
            return

    def tearDown(self):
        pass

    def __func_test_foo(self, a: int, b: str):
        logger = lh.init_logger(logger_name="test_func_fifo_q", is_print_to_console=True, is_json_output=False)
        logger.info(f"Hi from thread: {a}")

    def __cop_callback(self
                       , topic: str
                       , cop: ts_cop_pb2.Cop
                       , fid_num: int
                       , fid_value: Any) -> None:
        process_cop_map = {
            ts_cop_pb2.Cop.FidNum.SI: self.__process_cop_si
            , ts_cop_pb2.Cop.FidNum.Order: self.__process_cop_order
            , ts_cop_pb2.Cop.FidNum.Trade: self.__process_cop_trade
            , ts_cop_pb2.Cop.FidNum.CI: self.__process_cop_ci
        }
        if fid_num in process_cop_map:
            process_cop_map[fid_num](topic=topic, cop=cop, fid_num=fid_num, fid_value=fid_value)

    def __process_cop_ci(self, topic: str, cop: ts_cop_pb2.Cop, fid_num: ts_cop_pb2.Cop.FidNum, fid_value: Any):
        logger = lh.init_logger(logger_name="test_dcache", is_print_to_console=True, is_json_output=False)
        dcache_manager = DCacheManager()
        dcache_manager.init_component(logger=logger)
        dcache = dcache_manager.create_cache(cache_name=topic)

        for ci in fid_value.ci_list:
            # save to cache
            dcache_manager.save_fid(cache_name=cop.sender
                                    , msg_id=cop.msg_id
                                    , msg_type=cop.msg_type
                                    , fid_num=fid_num
                                    , fid_value=ci.value)

            dcache_ret = dcache.get_fid(msg_id=cop.msg_id
                                        , msg_type=cop.msg_type
                                        , fid_num=fid_num)
            manager_ret = dcache_manager.get_fid(cache_name=cop.sender
                                                 , msg_id=cop.msg_id
                                                 , msg_type=cop.msg_type
                                                 , fid_num=fid_num)

            self.assertEqual((True, (True, ci.value)), dcache_ret)
            self.assertEqual((True, (True, (True, ci.value))), manager_ret)
            logger.info(dcache_ret)
            if fid_num == ts_cop_pb2.Cop.FidNum.SI\
               or fid_num == ts_cop_pb2.Cop.FidNum.Order:
                for si_ele in dcache_ret[1][1]:
                    logger.info(si_ele)

    def __process_cop_si(self, topic: str, cop: ts_cop_pb2.Cop, fid_num: ts_cop_pb2.Cop.FidNum, fid_value: Any):
        logger = lh.init_logger(logger_name="test_dcache", is_print_to_console=True, is_json_output=False)
        dcache_manager = DCacheManager()
        dcache_manager.init_component(logger=logger)
        dcache = dcache_manager.create_cache(cache_name=topic)

        # save to cache
        dcache_manager.save_fid(cache_name=cop.sender
                                , msg_id=cop.msg_id
                                , msg_type=cop.msg_type
                                , fid_num=fid_num
                                , fid_value=[dconv.conv_cop_si_2_SI(si_ele=ele) for ele in fid_value.si_list])
        dcache_ret = dcache.get_fid(msg_id=cop.msg_id
                                    , msg_type=cop.msg_type
                                    , fid_num=fid_num)
        manager_ret = dcache_manager.get_fid(cache_name=cop.sender
                                             , msg_id=cop.msg_id
                                             , msg_type=cop.msg_type
                                             , fid_num=fid_num)

        self.assertEqual((True, (True, [dconv.conv_cop_si_2_SI(si_ele=ele) for ele in fid_value.si_list])), dcache_ret)
        self.assertEqual((True, (True, (True, [dconv.conv_cop_si_2_SI(si_ele=ele) for ele in fid_value.si_list]))), manager_ret)
        for ele in dcache_ret[1][1]:
            logger.info(ele)

    def __process_cop_order(self, topic: str, cop: ts_cop_pb2.Cop, fid_num: ts_cop_pb2.Cop.FidNum, fid_value: Any):
        logger = lh.init_logger(logger_name="test_dcache", is_print_to_console=True, is_json_output=False)
        dcache_manager = DCacheManager()
        dcache_manager.init_component(logger=logger)
        dcache = dcache_manager.create_cache(cache_name=topic)

        # save to cache
        dcache_manager.save_fid(cache_name=cop.sender
                                , msg_id=cop.msg_id
                                , msg_type=cop.msg_type
                                , fid_num=fid_num
                                , fid_value=[dconv.conv_cop_order_2_TS_Order(ord_ele=ele) for ele in fid_value.order_list])

        dcache_ret = dcache.get_fid(msg_id=cop.msg_id
                                    , msg_type=cop.msg_type
                                    , fid_num=fid_num)
        manager_ret = dcache_manager.get_fid(cache_name=cop.sender
                                             , msg_id=cop.msg_id
                                             , msg_type=cop.msg_type
                                             , fid_num=fid_num)

        self.assertEqual((True, (True, [dconv.conv_cop_order_2_TS_Order(ord_ele=ele) for ele in fid_value.order_list])), dcache_ret)
        self.assertEqual((True, (True, (True, [dconv.conv_cop_order_2_TS_Order(ord_ele=ele) for ele in fid_value.order_list]))), manager_ret)
        for ele in dcache_ret[1][1]:
            logger.info(ele)

    def __process_cop_trade(self, topic: str, cop: ts_cop_pb2.Cop, fid_num: ts_cop_pb2.Cop.FidNum, fid_value: Any):
        logger = lh.init_logger(logger_name="test_dcache", is_print_to_console=True, is_json_output=False)
        dcache_manager = DCacheManager()
        dcache_manager.init_component(logger=logger)
        dcache = dcache_manager.create_cache(cache_name=topic)

        # save to cache
        dcache_manager.save_fid(cache_name=cop.sender
                                , msg_id=cop.msg_id
                                , msg_type=cop.msg_type
                                , fid_num=fid_num
                                , fid_value=[dconv.conv_cop_trade_2_TS_Trade(trd_ele=ele) for ele in fid_value.trade_list])

        dcache_ret = dcache.get_fid(msg_id=cop.msg_id
                                    , msg_type=cop.msg_type
                                    , fid_num=fid_num)
        manager_ret = dcache_manager.get_fid(cache_name=cop.sender
                                             , msg_id=cop.msg_id
                                             , msg_type=cop.msg_type
                                             , fid_num=fid_num)

        self.assertEqual((True, (True, [dconv.conv_cop_trade_2_TS_Trade(trd_ele=ele) for ele in fid_value.trade_list])), dcache_ret)
        self.assertEqual((True, (True, (True, [dconv.conv_cop_trade_2_TS_Trade(trd_ele=ele) for ele in fid_value.trade_list]))), manager_ret)
        for ele in dcache_ret[1][1]:
            logger.info(ele)

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
        si_ele.strategy_id = "sadfihzv987yasdf"
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
        si_ele2.strategy_id = "sadfihzv987yasdf"
        si_ele2.symbol_id = "Symbol B ID";
        cop.si_map[ts_cop_pb2.Cop.FidNum.SI].si_list.append(si_ele2)
        # orders
        ord_ele = ts_cop_pb2.TSOrder()
        ord_ele.symbol = "Symbol A"
        ord_ele.quantity = 100
        ord_ele.fill_quantity = 50
        ord_ele.parent_id = "si.aivahmnvsao123hdnK"
        ord_ele.order_id = "ord.cxivhsdfn234h"
        ord_ele.platform_order_id = "dsifj"
        ord_ele.created = datetime.datetime.utcnow().timestamp()
        ord_ele.last_update = ord_ele.created
        ord_ele.strategy_name = "Test"
        ord_ele.live_mode = True
        ord_ele.strategy_id = "sadfihzv987yasdf";
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
        trd_ele.strategy_id = "sadfihzv987yasdf"
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

        # serialize example
        with open(Path.joinpath(Path(__file__).parent.absolute(), "cop_file"), "wb") as FH:
            FH.write(cop.SerializeToString())

        with open(Path.joinpath(Path(__file__).parent.absolute(), "cop_file"), "rb") as FH:
            cop.ParseFromString(FH.read())

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
            self.__cop_callback(topic=topic, cop=cop, fid_num=fid_num, fid_value=fid_value)
        # trade
        for fid_num, fid_value in cop.trade_map.items():
            self.__cop_callback(topic=topic, cop=cop, fid_num=fid_num, fid_value=fid_value)
        # si
        for fid_num, fid_value in cop.si_map.items():
            self.__cop_callback(topic=topic, cop=cop, fid_num=fid_num, fid_value=fid_value)
        # ci
        for fid_num, fid_value in cop.ci_map.items():
            self.__cop_callback(topic=topic, cop=cop, fid_num=fid_num, fid_value=fid_value)

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

    def __update_cb(self, fid_num: ts_cop_pb2.Cop.FidNum, fid_value: Any):
        logger = lh.init_logger(logger_name="test_ci_update_check", is_print_to_console=True, is_json_output=False)
        if fid_num == ts_cop_pb2.Cop.FidNum.SI:
            for ele in fid_value:
                logger.info(ele)
        else:
            logger.info(f"Get update: {fid_num} {fid_value}")

    def test_si_update_check(self):
        if not self.__test_config[inspect.stack()[0][3]]:
            return

        logger = lh.init_logger(logger_name="test_si_update_check", is_print_to_console=True, is_json_output=False)

        # prepare cop
        cop = ts_cop_pb2.Cop()
        cop.msg_id = "Test_True"
        cop.msg_type = ts_cop_pb2.Cop.MsgType.Strategy
        cop.sender = "Test_True"
        cop.instance_id = 1
        cop.seq_num = 1
        cop.created_time = datetime.datetime.utcnow().timestamp()

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
        si_ele.strategy_id = "sadfihzv987yasdf"
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
        si_ele2.strategy_id = "sadfihzv987yasdf"
        si_ele2.symbol_id = "Symbol B ID";
        cop.si_map[ts_cop_pb2.Cop.FidNum.SI].si_list.append(si_ele2)

        dcache_manager = DCacheManager()
        dcache_manager.init_component(logger=logger
                                      , update_cb=self.__update_cb)
        dcache = dcache_manager.create_cache(cache_name=cop.sender)

        # si
        for fid_num, fid_value in cop.si_map.items():
            # save to cache
            dcache_manager.save_fid(cache_name=cop.sender
                                    , msg_id=cop.msg_id
                                    , msg_type=cop.msg_type
                                    , fid_num=fid_num
                                    , fid_value=[dconv.conv_cop_si_2_SI(si_ele=si_ele) for si_ele in fid_value.si_list])

            is_cache_exist, is_si_exist = dcache_manager.is_si_exist(cache_name=cop.sender, si=[dconv.conv_cop_si_2_SI(si_ele=si_ele) for si_ele in fid_value.si_list])
            self.assertEqual(True, is_si_exist)

        # si
        for fid_num, fid_value in cop.si_map.items():
            # save to cache
            dcache_manager.save_fid(cache_name=cop.sender
                                    , msg_id=cop.msg_id
                                    , msg_type=cop.msg_type
                                    , fid_num=fid_num
                                    , fid_value=[dconv.conv_cop_si_2_SI(si_ele=si_ele) for si_ele in fid_value.si_list])

            is_cache_exist, is_si_exist = dcache_manager.is_si_exist(cache_name=cop.sender, si=[dconv.conv_cop_si_2_SI(si_ele=si_ele) for si_ele in fid_value.si_list])
            self.assertEqual(True, is_si_exist)

    def test_fid_update_check(self):
        if not self.__test_config[inspect.stack()[0][3]]:
            return

        logger = lh.init_logger(logger_name="test_fid_update_check", is_print_to_console=True, is_json_output=False)

        # prepare cop
        cop = ts_cop_pb2.Cop()
        cop.msg_id = "Symbol A"
        cop.msg_type = ts_cop_pb2.Cop.MsgType.Listing
        cop.sender = "Test_True"
        cop.instance_id = 1
        cop.seq_num = 1
        cop.created_time = datetime.datetime.utcnow().timestamp()
        topic = "Test_True"

        cop.int32_map[1] = 10
        cop.int64_map[10001] = 20

        dcache_manager = DCacheManager()
        dcache_manager.init_component(logger=logger
                                      , update_cb=self.__update_cb)
        dcache = dcache_manager.create_cache(cache_name=cop.sender)

        # int32
        for fid_num, fid_value in cop.int32_map.items():
            # save to cache
            dcache_manager.save_fid(cache_name=cop.sender
                                    , msg_id=cop.msg_id
                                    , msg_type=cop.msg_type
                                    , fid_num=fid_num
                                    , fid_value=fid_value)
            ret = dcache_manager.get_fid(cache_name=cop.sender
                                         , msg_id=cop.msg_id
                                         , msg_type=cop.msg_type
                                         , fid_num=fid_num)
            self.assertEqual((True, (True, (True, fid_value))), ret)

        # int32
        for fid_num, fid_value in cop.int64_map.items():
            # save to cache
            dcache_manager.save_fid(cache_name=cop.sender
                                    , msg_id=cop.msg_id
                                    , msg_type=cop.msg_type
                                    , fid_num=fid_num
                                    , fid_value=fid_value)
            ret = dcache_manager.get_fid(cache_name=cop.sender
                                         , msg_id=cop.msg_id
                                         , msg_type=cop.msg_type
                                         , fid_num=fid_num)
            self.assertEqual((True, (True, (True, fid_value))), ret)

        cop.int32_map[1] = 11
        # int32
        for fid_num, fid_value in cop.int32_map.items():
            # save to cache
            dcache_manager.save_fid(cache_name=cop.sender
                                    , msg_id=cop.msg_id
                                    , msg_type=cop.msg_type
                                    , fid_num=fid_num
                                    , fid_value=fid_value)
            ret = dcache_manager.get_fid(cache_name=cop.sender
                                         , msg_id=cop.msg_id
                                         , msg_type=cop.msg_type
                                         , fid_num=fid_num)
            self.assertEqual((True, (True, (True, fid_value))), ret)

    def test_trade_update_check(self):
        if not self.__test_config[inspect.stack()[0][3]]:
            return

        logger = lh.init_logger(logger_name="test_trade_update_check", is_print_to_console=True, is_json_output=False)

        # prepare cop
        cop = ts_cop_pb2.Cop()
        cop.msg_id = "Test_True"
        cop.msg_type = ts_cop_pb2.Cop.MsgType.Strategy
        cop.sender = "Test_True"
        cop.instance_id = 1
        cop.seq_num = 1
        cop.created_time = datetime.datetime.utcnow().timestamp()
        topic = "Test_True"

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
        trd_ele.strategy_id = "sadfihzv987yasdf"
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

        dcache_manager = DCacheManager()
        dcache_manager.init_component(logger=logger
                                      , update_cb=self.__update_cb)
        dcache = dcache_manager.create_cache(cache_name=cop.sender)

        # trade
        for fid_num, fid_value in cop.trade_map.items():
            # save to cache
            dcache_manager.save_fid(cache_name=cop.sender
                                    , msg_id=cop.msg_id
                                    , msg_type=cop.msg_type
                                    , fid_num=fid_num
                                    , fid_value=[dconv.conv_cop_trade_2_TS_Trade(trd_ele=ele) for ele in fid_value.trade_list])

            for trade in fid_value.trade_list:
                is_cache_exist, is_trd_exist = dcache_manager.is_trade_exist(cache_name=cop.sender, trade=trade)
                self.assertEqual(True, is_trd_exist)

        # trade
        for fid_num, fid_value in cop.trade_map.items():
            # save to cache
            dcache_manager.save_fid(cache_name=cop.sender
                                    , msg_id=cop.msg_id
                                    , msg_type=cop.msg_type
                                    , fid_num=fid_num
                                    , fid_value=[dconv.conv_cop_trade_2_TS_Trade(trd_ele=ele) for ele in fid_value.trade_list])

            for trade in fid_value.trade_list:
                is_cache_exist, is_trd_exist = dcache_manager.is_trade_exist(cache_name=cop.sender, trade=trade)
                self.assertEqual(True, is_trd_exist)

    def test_order_update_check(self):
        if not self.__test_config[inspect.stack()[0][3]]:
            return

        logger = lh.init_logger(logger_name="test_order_update_check", is_print_to_console=True, is_json_output=False)

        # prepare cop
        cop = ts_cop_pb2.Cop()
        cop.msg_id = "Test_True"
        cop.msg_type = ts_cop_pb2.Cop.MsgType.Strategy
        cop.sender = "Test_True"
        cop.instance_id = 1
        cop.seq_num = 1
        cop.created_time = datetime.datetime.utcnow().timestamp()

        # orders
        ord_ele = ts_cop_pb2.TSOrder()
        ord_ele.symbol = "Symbol A"
        ord_ele.quantity = 100
        ord_ele.fill_quantity = 50
        ord_ele.parent_id = "si.aivahmnvsao123hdnK"
        ord_ele.order_id = "ord.cxivhsdfn234h"
        ord_ele.platform_order_id = "dsifj"
        ord_ele.created = datetime.datetime.utcnow().timestamp()
        ord_ele.last_update = ord_ele.created
        ord_ele.strategy_name = "Test"
        ord_ele.live_mode = True
        ord_ele.strategy_id = "sadfihzv987yasdf"
        ord_ele.order_status = "PFilled"
        ord_ele.execution_broker = "IB"
        ord_ele.clearing_broker = "IB"
        ord_ele.account = "Dummy"
        ord_ele.price = 10.9
        ord_ele.fee = 0.01
        ord_ele.exchange = "US"
        ord_ele.ccy = "USD"
        ord_ele.fee_ccy = "USD"
        ord_ele.symbol_id = "Symbol A ID"

        ord_ele2 = ts_cop_pb2.TSOrder()
        ord_ele2.symbol = "Symbol B"
        ord_ele2.quantity = 100
        ord_ele2.fill_quantity = 50
        ord_ele2.parent_id = "si.aivahmnvsao123hdnK"
        ord_ele2.order_id = "ord.cxivhsdfn235h"
        ord_ele2.platform_order_id = "dsifj2"
        ord_ele2.created = datetime.datetime.utcnow().timestamp()
        ord_ele2.last_update = ord_ele.created
        ord_ele2.strategy_name = "Test"
        ord_ele2.live_mode = True
        ord_ele2.strategy_id = "sadfihzv987yasdf"
        ord_ele2.order_status = "PFilled"
        ord_ele2.execution_broker = "IB"
        ord_ele2.clearing_broker = "IB"
        ord_ele2.account = "Dummy"
        ord_ele2.price = 12.9
        ord_ele2.fee = 0.01
        ord_ele2.exchange = "US"
        ord_ele2.ccy = "USD"
        ord_ele2.fee_ccy = "USD"
        ord_ele2.symbol_id = "Symbol B ID"

        ord_ele3 = copy.deepcopy(ord_ele)
        ord_ele3.fill_quantity = 100
        ord_ele3.order_id = "ord.cxivhsdfn236h"
        cop.order_map[ts_cop_pb2.Cop.FidNum.Order].order_list.append(ord_ele2)
        cop.order_map[ts_cop_pb2.Cop.FidNum.Order].order_list.append(ord_ele3)

        dcache_manager = DCacheManager()
        dcache_manager.init_component(logger=logger
                                      , update_cb=self.__update_cb)
        dcache = dcache_manager.create_cache(cache_name=cop.sender)

        # order
        for fid_num, fid_value in cop.order_map.items():
            # save to cache
            dcache_manager.save_fid(cache_name=cop.sender
                                    , msg_id=cop.msg_id
                                    , msg_type=cop.msg_type
                                    , fid_num=fid_num
                                    , fid_value=[dconv.conv_cop_order_2_TS_Order(ord_ele=ele) for ele in fid_value.order_list])

            for order in fid_value.order_list:
                is_cache_exist, is_ord_exist = dcache_manager.is_order_exist(cache_name=cop.sender, order=order)
                self.assertEqual(True, is_ord_exist)

        # add the first order again - expect we get one update and the latest snapshot didn't change
        cop.order_map[ts_cop_pb2.Cop.FidNum.Order].order_list.append(ord_ele)
        cop.order_map[ts_cop_pb2.Cop.FidNum.Order].order_list.append(ord_ele2)
        cop.order_map[ts_cop_pb2.Cop.FidNum.Order].order_list.append(ord_ele3)
        # order
        for fid_num, fid_value in cop.order_map.items():
            # save to cache
            dcache_manager.save_fid(cache_name=cop.sender
                                    , msg_id=cop.msg_id
                                    , msg_type=cop.msg_type
                                    , fid_num=fid_num
                                    , fid_value=[dconv.conv_cop_order_2_TS_Order(ord_ele=ele) for ele in fid_value.order_list])

            for order in fid_value.order_list:
                is_cache_exist, is_ord_exist = dcache_manager.is_order_exist(cache_name=cop.sender, order=order)
                self.assertEqual(True, is_ord_exist)

    def test_ci_update_check(self):
        if not self.__test_config[inspect.stack()[0][3]]:
            return

        logger = lh.init_logger(logger_name="test_ci_update_check", is_print_to_console=True, is_json_output=False)

        # prepare cop
        cop = ts_cop_pb2.Cop()
        cop.msg_id = "Test_True"
        cop.msg_type = ts_cop_pb2.Cop.MsgType.Strategy
        cop.sender = "Test_True"
        cop.instance_id = 1
        cop.seq_num = 1
        cop.created_time = datetime.datetime.utcnow().timestamp()

        # ci
        cop.ci_map[ts_cop_pb2.Cop.FidNum.CI].ci_list.append(ts_cop_pb2.CI(value=json.dumps({"aa": "hello_world", "00": "hhee"})))
        cop.ci_map[ts_cop_pb2.Cop.FidNum.CI].ci_list.append(ts_cop_pb2.CI(value=json.dumps({"aa": "hello_world 2"})))

        dcache_manager = DCacheManager()
        dcache_manager.init_component(logger=logger
                                      , update_cb=self.__update_cb)
        dcache = dcache_manager.create_cache(cache_name=cop.sender)

        # ci
        for fid_num, fid_value in cop.ci_map.items():
            for ci in fid_value.ci_list:
                # save to cache
                dcache_manager.save_fid(cache_name=cop.sender
                                        , msg_id=cop.msg_id
                                        , msg_type=cop.msg_type
                                        , fid_num=fid_num
                                        , fid_value=json.loads(ci.value))

                is_cache_exist, is_ci_exist = dcache_manager.is_ci_exist(cache_name=cop.sender, ci=json.loads(ci.value))
                self.assertEqual(True, is_ci_exist)

        # add one more record with different orders
        cop.ci_map[ts_cop_pb2.Cop.FidNum.CI].ci_list.append(ts_cop_pb2.CI(value=json.dumps({"00": "hhee", "aa": "hello_world"})))
        for fid_num, fid_value in cop.ci_map.items():
            for ci in fid_value.ci_list:
                # save to cache
                dcache_manager.save_fid(cache_name=cop.sender
                                        , msg_id=cop.msg_id
                                        , msg_type=cop.msg_type
                                        , fid_num=fid_num
                                        , fid_value=json.loads(ci.value))

                is_cache_exist, is_ci_exist = dcache_manager.is_ci_exist(cache_name=cop.sender, ci=json.loads(ci.value))
                self.assertEqual(True, is_ci_exist)

if __name__ == "__main__":
    unittest.main()
