#region imports
from AlgorithmImports import *
#endregion

import logging
from typing import List, Dict, Any
import json
import datetime

import sfdevtools.data_control.TSDataCtrl as TSDataCtrl
import sfdevtools.data_control.TSBackgroundCtrl as TSBackgroundCtrl
from sfdevtools.data_cache.DCacheManager import DCacheManager
import sfdevtools.grpc_protos.ts_cop_pb2 as ts_cop_pb2
import sfdevtools.grpc_protos.ts_cop_pb2_grpc as ts_cop_pb2_grpc
from sfdevtools.data_cache.DComponents import StrategyInsight, TS_Order, TS_Trade
import sfdevtools.data_cache.DConverter as dconv

class TSDataManager(object):
    def __init__(self):
        self.__logger: logging.Logger = None
        self.__ts_datactrl_pub: TSDataCtrl = None
        self.__ts_datactrl_sub: TSDataCtrl = None
        self.__cop_cb = None
        self.__pub_topic: str = ""
        self.__output_dcache_m: DCacheManager = None
        self.__bg_ctrl: TSBackgroundCtrl.TSBackgroundCtrl = None
        self.__is_active_bg: bool = False

        self.__data_convert_map = {
            ts_cop_pb2.Cop.FidNum.SI: self.__convert_si
            , ts_cop_pb2.Cop.FidNum.Order: self.__convert_order
            , ts_cop_pb2.Cop.FidNum.Trade: self.__convert_trade
        }

    def init_component(self
                       , logger: logging.Logger
                       , ts_datactrl_pub: TSDataCtrl.TSDataCtrl
                       , sender_name: str
                       , pub_topic: str
                       , ts_datactrl_sub: TSDataCtrl.TSDataCtrl
                       , output_dcache_m: DCacheManager
                       , bg_ctrl: TSBackgroundCtrl.TSBackgroundCtrl
                       , is_active_bg: bool) -> None:
        self.__logger = logger
        # prepare publisher
        self.__ts_datactrl_pub = ts_datactrl_pub
        self.__sender_name = sender_name
        self.__pub_topic = pub_topic
        # prepare subscriber
        self.__ts_datactrl_sub = ts_datactrl_sub
        # prepare cache
        self.__output_dcache_m = output_dcache_m
        # prepare backgroup control
        self.__bg_ctrl = bg_ctrl
        self.__is_active_bg = is_active_bg

    def send_ci(self, msg_id: str, ci_list: List[Dict], is_save_to_cache: bool = True) -> None:
        cop = ts_cop_pb2.Cop()
        for ci in ci_list:
            cop.data_map[ts_cop_pb2.Cop.FidNum.CI].ci_data.ci_list.append(ts_cop_pb2.CI(value=json.dumps(ci)))

            if is_save_to_cache and self.__is_active_bg:
                # save to output cache
                self.__output_dcache_m.save_ci(cache_name=self.__sender_name, ci=ci)

        self.__ts_datactrl_pub.send_cop(msg_id=msg_id
                                        , msg_type=ts_cop_pb2.Cop.MsgType.Strategy
                                        , topic=self.__pub_topic
                                        , cop=cop)

    def send_si(self, msg_id:str, si_list: List[StrategyInsight], is_save_to_cache: bool = True) -> None:
        cop = ts_cop_pb2.Cop()
        for si in si_list:
            si_ele = dconv.conv_SI_2_cop_si(si=si)

            cop.data_map[ts_cop_pb2.Cop.FidNum.SI].si_data.si_list.append(si_ele)

        if is_save_to_cache and self.__is_active_bg:
            # save to output cache
            self.__output_dcache_m.save_si(cache_name=self.__sender_name, si=si_list)

        self.__ts_datactrl_pub.send_cop(msg_id=msg_id
                                        , msg_type=ts_cop_pb2.Cop.MsgType.Strategy
                                        , topic=self.__pub_topic
                                        , cop=cop)

    def send_order(self, msg_id: str, order_list: List[TS_Order], is_save_to_cache: bool = True) -> None:
        cop = ts_cop_pb2.Cop()
        for order in order_list:
            ord_ele = dconv.conv_TS_Order_2_cop_order(order=order)

            cop.data_map[ts_cop_pb2.Cop.FidNum.Order].order_data.order_list.append(ord_ele)

        if is_save_to_cache and self.__is_active_bg:
            # save to output cache
            self.__output_dcache_m.save_orders(cache_name=self.__sender_name, orders=order_list)

        self.__ts_datactrl_pub.send_cop(msg_id=msg_id
                                        , msg_type=ts_cop_pb2.Cop.MsgType.Strategy
                                        , topic=self.__pub_topic
                                        , cop=cop)

    def send_trade(self, msg_id: str, trade_list: List[TS_Trade], is_save_to_cache: bool = True) -> None:
        cop = ts_cop_pb2.Cop()
        for trd in trade_list:
            trd_ele = dconv.conv_TS_Trade_2_cop_trade(trd=trd)

            cop.data_map[ts_cop_pb2.Cop.FidNum.Trade].trade_data.trade_list.append(trd_ele)

        if is_save_to_cache and self.__is_active_bg:
            # save to output cache
            self.__output_dcache_m.save_trades(cache_name=self.__sender_name, trades=trade_list)

        self.__ts_datactrl_pub.send_cop(msg_id=msg_id
                                        , msg_type=ts_cop_pb2.Cop.MsgType.Strategy
                                        , topic=self.__pub_topic
                                        , cop=cop)

    def send_bg_cop(self, msg_id: str, msg_type: ts_cop_pb2.Cop.MsgType, cop: ts_cop_pb2.Cop) -> None:
        if not self.__is_active_bg:
            return
        self.__ts_datactrl_pub.send_cop(msg_id=msg_id
                                        , msg_type=msg_type
                                        , topic=self.__pub_topic
                                        , cop=cop)
    def send_int(self
                 , msg_id: str
                 , msg_type: ts_cop_pb2.Cop.MsgType
                 , fid_num: int
                 , fid_value: int
                 , time: datetime) -> None:
        cop = ts_cop_pb2.Cop()
        if 70001 <= fid_num and fid_num <= 80000:
            cop.data_map[fid_num].d_int32_data.value = fid_num
            cop.data_map[fid_num].d_int32_data.time = time.timestamp()
        elif 80001 <= fid_num and fid_num <= 90000:
            cop.data_map[fid_num].d_int64_data.value = fid_num
            cop.data_map[fid_num].d_int64_data.time = time.timestamp()
        else:
            return None

        self.__ts_datactrl_pub.send_cop(msg_id=msg_id
                                        , msg_type=msg_type
                                        , topic=self.__pub_topic
                                        , cop=cop)

    def send_double(self
                    , msg_id: str
                    , msg_type: ts_cop_pb2.Cop.MsgType
                    , fid_num: int
                    , fid_value: float
                    , time: datetime) -> None:
        cop = ts_cop_pb2.Cop()
        if 90001 <= fid_num and fid_num <= 100000:
            cop.data_map[fid_num].d_float_data.value = fid_num
            cop.data_map[fid_num].d_float_data.time = time.timestamp()
        elif 100001 <= fid_num and fid_num <= 110000:
            cop.data_map[fid_num].d_double_data.value = fid_num
            cop.data_map[fid_num].d_double_data.time = time.timestamp()
        else:
            return None

        self.__ts_datactrl_pub.send_cop(msg_id=msg_id
                                        , msg_type=msg_type
                                        , topic=self.__pub_topic
                                        , cop=cop)

    def send_string(self
                    , msg_id: str
                    , msg_type: ts_cop_pb2.Cop.MsgType
                    , fid_num: int
                    , fid_value: float
                    , time: datetime) -> None:
        cop = ts_cop_pb2.Cop()
        if 110001 <= fid_num and fid_num <= 120000:
            cop.data_map[fid_num].d_string_data.value = fid_num
            cop.data_map[fid_num].d_string_data.time = time.timestamp()
        else:
            return None

        self.__ts_datactrl_pub.send_cop(msg_id=msg_id
                                        , msg_type=msg_type
                                        , topic=self.__pub_topic
                                        , cop=cop)

    def send_bool(self
                  , msg_id: str
                  , msg_type: ts_cop_pb2.Cop.MsgType
                  , fid_num: int
                  , fid_value: float
                  , time: datetime) -> None:
        cop = ts_cop_pb2.Cop()
        if 120001 <= fid_num and fid_num <= 130000:
            cop.data_map[fid_num].d_bool_data.value = fid_num
            cop.data_map[fid_num].d_bool_data.time = time.timestamp()
        else:
            return None

        self.__ts_datactrl_pub.send_cop(msg_id=msg_id
                                        , msg_type=msg_type
                                        , topic=self.__pub_topic
                                        , cop=cop)

    def get_cur_sent_byte(self) -> int:
        return self.__ts_datactrl_pub.get_cur_sent_byte()

    def send_msg_list(self
                      , msg_id: str
                      , msg_type: ts_cop_pb2.Cop.MsgType
                      , fid_nums: List[int]
                      , fid_values: List[Any]
                      , time: datetime) -> None:
        # convert to cop format
        idx = 0
        for fid_num, fid_value in zip(fid_nums, fid_values):
            if fid_num in self.__data_convert_map:
                self.__data_convert_map[fid_num](fid_values=fid_values, idx=idx)

            idx += 1

        self.__ts_datactrl_pub.send_cop_list(msg_id=msg_id
                                             , msg_type=msg_type
                                             , fid_nums=fid_nums
                                             , fid_values=fid_values
                                             , topic=self.__pub_topic
                                             , timestamp=time.timestamp())

    def __convert_si(self, fid_values: List[Any], idx: int) -> None:
        fid_values[idx] = conv.conv_SI_2_cop_si(si=fid_values[idx])

    def __convert_order(self, fid_values: List[Any], idx: int):
        fid_values[idx] = conv.conv_TS_Order_2_cop_order(order=fid_values[idx])

    def __convert_trade(self, fid_values: List[Any], idx: int):
        fid_values[idx] = conv.conv_TS_Trade_2_cop_trade(trd=fid_values[idx])
