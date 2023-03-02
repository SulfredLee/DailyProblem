import logging
import threading
from typing import List, Dict, Tuple, Union, Any
import copy
import json
import hashlib

from sfdevtools.data_cache.DComponents import StrategyInsight, TS_Order, TS_Trade
from sfdevtools.data_cache.DPage import DPage
import sfdevtools.data_cache.DTimelyCache as TimelyCache
import sfdevtools.grpc_protos.ts_cop_pb2 as ts_cop_pb2
import sfdevtools.grpc_protos.ts_cop_pb2_grpc as ts_cop_pb2_grpc

class DStrategy(object):
    def __init__(self):
        self.__logger: logging.Logger = None
        self.__max_hist_orders: int = 1000
        self.__max_hist_trades: int = 1000
        self.__max_hist_si: int = 1000
        self.__si_cache: TimelyCache.TimelyCache_Hist = TimelyCache.TimelyCache_Hist() # key: si_id --- keep a limited list of latest records
        self.__ci_id: str = ""
        self.__ci_cache: TimelyCache.TimelyCache_Hist = TimelyCache.TimelyCache_Hist() # key: ci_id --- keep a limited list of latest records
        self.__order_cache: TimelyCache.TimelyCache_Snapshot = TimelyCache.TimelyCache_Snapshot() # key: platform_order_id --- keep latest snapshot
        self.__trade_cache: TimelyCache.TimelyCache_Hist = TimelyCache.TimelyCache_Hist() # key: trade_id --- keep latest records in hash
        self.__mutex: threading.Lock = threading.Lock()

        self.__strategy_page: DPage = DPage()

    def init_component(self
                       , logger: logging.Logger
                       , max_hist_orders: int = 1000
                       , max_hist_trades: int = 1000
                       , max_hist_si: int = 1000) -> None:
        self.__logger = logger
        self.__max_hist_orders = max_hist_orders
        self.__max_hist_trades = max_hist_trades
        self.__max_hist_si = max_hist_si
        self.__strategy_page.init_component(logger=self.__logger
                                            , save_other_map={
                                                ts_cop_pb2.Cop.FidNum.CI: self.save_ci
                                                , ts_cop_pb2.Cop.FidNum.SI: self.save_si
                                                , ts_cop_pb2.Cop.FidNum.Order: self.save_orders
                                                , ts_cop_pb2.Cop.FidNum.Trade: self.save_trades
                                            }
                                            , get_other_map={
                                                ts_cop_pb2.Cop.FidNum.CI: self.get_ci
                                                , ts_cop_pb2.Cop.FidNum.SI: self.get_si
                                                , ts_cop_pb2.Cop.FidNum.Order: self.get_orders
                                                , ts_cop_pb2.Cop.FidNum.Trade: self.get_trades
                                            })

    def save_si(self, si: List[StrategyInsight]) -> bool:
        if len(si) == 0:
            return True
        self.__si_cache.upsert_ele(key=si[0].si_id, value=si)
        return True

    def is_latest_si(self, si: List[StrategyInsight]) -> bool:
        if self.__si_cache.size() < 1:
            return False
        return self.__is_same_si(si1=self.__si_cache.get_records_by_index(-1), si2=si)

    def is_ci_exist(self, ci: Dict[str, Any]) -> bool:
        return self.__ci_cache.is_exist(key=hashlib.md5(json.dumps(ci, sort_keys=True).encode("utf-8")).digest())

    def is_si_exist(self, si_id: str) -> bool:
        return self.__si_cache.is_exist(key=si_id)

    def get_si(self) -> List[StrategyInsight]:
        return self.__si_cache.get_records_by_index(-1)

    def get_all_si(self) -> List[List[StrategyInsight]]:
        return self.__si_cache.get_records_in_time_series()

    def save_ci(self, ci: Dict[str, Any]) -> None:
        self.__ci_cache.upsert_ele(key=hashlib.md5(json.dumps(ci, sort_keys=True).encode("utf-8")).digest(), value=ci)

    def get_ci(self) -> Dict[str, Any]:
        if self.__ci_cache.size() < 1:
            return None
        return self.__ci_cache.get_records_by_index(idx=-1)

    def get_all_ci(self) -> List[Dict[str, Any]]:
        return self.__ci_cache.get_records_in_time_series()

    def save_ci_id(self, ci_id: str) -> None:
        with self.__mutex:
            self.__ci_id = ci_id

    def get_ci_id(self) -> str:
        with self.__mutex:
            return self.__ci_id

    def save_order(self, order: TS_Order) -> None:
        self.__order_cache.upsert_ele(key=order.platform_order_id, value=order)

    def save_orders(self, orders: List[TS_Order]) -> None:
        self.__order_cache.upsert_multi(keys=[order.platform_order_id for order in orders], values=orders)

    def save_trade(self, trade: TS_Trade) -> None:
        self.__trade_cache.upsert_ele(key=trade.trade_id, value=trade)

    def save_trades(self, trades: List[TS_Trade]) -> None:
        self.__trade_cache.upsert_multi(keys=[trade.trade_id for trade in trades], values=trades)

    def is_trade_exist(self, trade_id: str) -> bool:
        return self.__trade_cache.is_exist(key=trade_id)

    def get_trade(self, trade_id: str) -> Union[bool, TS_Trade]:
        trade = self.__trade_cache.get_ele(key=trade_id)
        if None is trade:
            return (False, None)
        else:
            return (True, trade)

    def get_trades(self) -> List[TS_Trade]:
        return self.__trade_cache.get_records_in_time_series()

    def get_order(self, platform_order_id: str) -> Union[bool, TS_Order]:
        order = self.__order_cache.get_ele(key=platform_order_id)
        if None is order:
            return (False, None)
        else:
            return (True, order)

    def is_order_exist(self, platform_order_id: str) -> bool:
        return self.__order_cache.is_exist(key=platform_order_id)

    def get_orders(self) -> List[TS_Order]:
        return self.__order_cache.get_records_in_time_series()

    def save_fid(self, fid_num: int, fid_value: Any) -> None:
        self.__strategy_page.save_fid(fid_num=fid_num, fid_value=fid_value)

    def get_fids(self) -> List[Union[int, Any]]:
        return self.__strategy_page.get_fids()

    def get_fid(self, fid_num: int) -> Union[bool, Any]:
        return self.__strategy_page.get_fid(fid_num=fid_num)

    def __is_same_si(self, si1: List[StrategyInsight], si2: List[StrategyInsight]) -> bool:
        if len(si1) != len(si2):
            return False

        si1_sorted = sorted(si1, key=lambda x: x.symbol_id)
        si2_sorted = sorted(si2, key=lambda x: x.symbol_id)
        for a, b in zip(si1_sorted, si2_sorted):
            if a != b:
                return False
        return True
