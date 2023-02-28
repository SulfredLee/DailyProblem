#region imports
from AlgorithmImports import *
#endregion

import logging
from typing import List, Dict, Any
import json

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
            cop.ci_map[ts_cop_pb2.Cop.FidNum.CI].ci_list.append(ts_cop_pb2.CI(value=json.dumps(ci)))

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

            cop.si_map[ts_cop_pb2.Cop.FidNum.SI].si_list.append(si_ele)

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

            cop.order_map[ts_cop_pb2.Cop.FidNum.Order].order_list.append(ord_ele)

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

            cop.trade_map[ts_cop_pb2.Cop.FidNum.Trade].trade_list.append(trd_ele)

        if is_save_to_cache and self.__is_active_bg:
            # save to output cache
            self.__output_dcache_m.save_trades(cache_name=self.__sender_name, trades=trade_list)

        self.__ts_datactrl_pub.send_cop(msg_id=msg_id
                                        , msg_type=ts_cop_pb2.Cop.MsgType.Strategy
                                        , topic=self.__pub_topic
                                        , cop=cop)

    def send_bg_cop(self, msg_id: str, msg_type: ts_cop_pb2.Cop.MsgType, cop: ts_cop_pb2.Cop,) -> None:
        if not self.__is_active_bg:
            return
        self.__ts_datactrl_pub.send_cop(msg_id=msg_id
                                        , msg_type=msg_type
                                        , topic=self.__pub_topic
                                        , cop=cop)
