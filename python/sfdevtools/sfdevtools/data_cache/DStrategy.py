import logging
import threading
from typing import List, Dict, Tuple, Union, Any
import copy
import json
import hashlib

from sfdevtools.data_cache.DComponents import StrategyInsight, TS_Order, TS_Trade
from sfdevtools.data_cache.DPage import DPage
import sfdevtools.data_cache.DTimelyCache as TimelyCache
import sfdevtools.data_cache.DOrderCache as DOrderCache
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
        self.__order_cache: DOrderCache.DOrderCache = DOrderCache.DOrderCache()
        self.__trade_cache: TimelyCache.TimelyCache_Hist = TimelyCache.TimelyCache_Hist() # key: trade_id --- keep latest records in hash
        self.__ci_mutex: threading.Lock = threading.Lock()
        self.__si_mutex: threading.Lock = threading.Lock()
        self.__update_cb: Any = None
        self.__get_parent_dcache_fun: Any = None
        self.__strategy_name: str = None

        self.__strategy_page: DPage = DPage()

    def init_component(self
                       , logger: logging.Logger
                       , update_cb: Any
                       , strategy_name: str
                       , get_parent_dcache_fun: Any
                       , max_hist_orders: int = 1000
                       , max_hist_trades: int = 1000
                       , max_hist_si: int = 1000) -> None:
        self.__logger = logger
        self.__strategy_name = strategy_name
        self.__get_parent_dcache_fun = get_parent_dcache_fun
        self.__update_cb = update_cb
        self.__max_hist_orders = max_hist_orders
        self.__max_hist_trades = max_hist_trades
        self.__max_hist_si = max_hist_si
        self.__strategy_page.init_component(logger=self.__logger
                                            , update_cb=self.__update_cb
                                            , page_id=f"page.{self.__strategy_name}"
                                            , get_parent_dcache_fun=self.__get_parent_dcache_fun
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
        self.__order_cache.init_component(logger=self.__logger
                                              , order_hist=TimelyCache.TimelyCache_Hist()
                                              , order_snapshot=TimelyCache.TimelyCache_Snapshot()
                                              , db_id_hist=TimelyCache.TimelyCache_Hist())

    def save_si(self, si: List[StrategyInsight]) -> bool:
        if len(si) == 0:
            return True
        si_sorted = sorted(si, key=lambda x: x.symbol_id)
        is_new = self.__si_cache.upsert_ele(key=si_sorted[0].si_id, value=si_sorted)
        if is_new and self.__update_cb is not None:
            self.__update_cb(dcache=self.__get_parent_dcache_fun(), msg_id=self.__strategy_name, fid_num=ts_cop_pb2.Cop.FidNum.SI, fid_value=si_sorted)

        return True

    def is_latest_si(self, si: List[StrategyInsight]) -> bool:
        if self.__si_cache.size() < 1:
            return False
        return self.__is_same_si(si1=self.__si_cache.get_records_by_index(-1), si2=si)

    def is_ci_exist(self, ci: Dict[str, Any]) -> bool:
        return self.__ci_cache.is_exist(key=hashlib.md5(json.dumps(ci, sort_keys=True).encode("utf-8")).digest())

    def is_si_exist(self, si: List[StrategyInsight]) -> bool:
        if len(si) == 0:
            return False
        return self.__si_cache.is_exist(key=si[0].si_id)

    def get_si(self) -> List[StrategyInsight]:
        return self.__si_cache.get_records_by_index(-1)

    def get_all_si(self) -> List[List[StrategyInsight]]:
        return self.__si_cache.get_records_in_time_series()

    def save_ci(self, ci: Dict[str, Any]) -> None:
        is_new = self.__ci_cache.upsert_ele(key=hashlib.md5(json.dumps(ci
                                                                       , sort_keys=True).encode("utf-8")).digest()
                                            , value=json.dumps(ci, sort_keys=True))

        if is_new and self.__update_cb is not None:
            self.__update_cb(dcache=self.__get_parent_dcache_fun(), msg_id=self.__strategy_name, fid_num=ts_cop_pb2.Cop.FidNum.CI, fid_value=ci)

    def get_ci(self) -> Dict[str, Any]:
        if self.__ci_cache.size() < 1:
            return None
        return json.loads(self.__ci_cache.get_records_by_index(idx=-1))

    def get_all_ci(self) -> List[Dict[str, Any]]:
        return [json.loads(ci) for ci in self.__ci_cache.get_records_in_time_series()]

    def save_ci_id(self, ci_id: str) -> None:
        with self.__ci_mutex:
            self.__ci_id = ci_id

    def get_ci_id(self) -> str:
        with self.__ci_mutex:
            return self.__ci_id

    def save_trade(self, trade: TS_Trade) -> None:
        is_new = self.__trade_cache.upsert_ele(key=trade.trade_id, value=trade)
        if is_new and self.__update_cb is not None:
            self.__update_cb(dcache=self.__get_parent_dcache_fun(), msg_id=self.__strategy_name, fid_num=ts_cop_pb2.Cop.FidNum.Trade, fid_value=trade)

    def save_trades(self, trades: List[TS_Trade]) -> None:
        is_new_list: List[bool] = self.__trade_cache.upsert_multi(keys=[trade.trade_id for trade in trades], values=trades)
        if self.__update_cb is None:
            return None
        for is_new, trade in zip(is_new_list, trades):
            if is_new:
                self.__update_cb(dcache=self.__get_parent_dcache_fun(), msg_id=self.__strategy_name, fid_num=ts_cop_pb2.Cop.FidNum.Trade, fid_value=trade)

    def is_trade_exist(self, trade: TS_Trade) -> bool:
        return self.__trade_cache.is_exist(key=trade.trade_id)

    def get_trade(self, trade_id: str) -> Union[bool, TS_Trade]:
        trade = self.__trade_cache.get_ele(key=trade_id)
        if None is trade:
            return (False, None)
        else:
            return (True, trade)

    def get_trades(self, last_n: int) -> List[TS_Trade]:
        return self.__trade_cache.get_last_n_records_in_time_series(n=last_n)

    def save_orders(self, orders: List[TS_Order]) -> None:
        is_new_list: List[bool] = self.__order_cache.save_orders(orders=orders)
        if self.__update_cb is None:
            return None
        for is_new, order in zip(is_new_list, orders):
            if is_new:
                self.__update_cb(dcache=self.__get_parent_dcache_fun(), msg_id=self.__strategy_name, fid_num=ts_cop_pb2.Cop.FidNum.Order, fid_value=order)
                self.__update_cb(dcache=self.__get_parent_dcache_fun(), msg_id=self.__strategy_name, fid_num=ts_cop_pb2.Cop.FidNum.Order_Snap, fid_value=order)

    def save_order(self, order: TS_Order) -> None:
        is_new = self.__order_cache.save_order(order=order)
        if is_new and self.__update_cb is not None:
            self.__update_cb(dcache=self.__get_parent_dcache_fun(), msg_id=self.__strategy_name, fid_num=ts_cop_pb2.Cop.FidNum.Order, fid_value=order)
            self.__update_cb(dcache=self.__get_parent_dcache_fun(), msg_id=self.__strategy_name, fid_num=ts_cop_pb2.Cop.FidNum.Order_Snap, fid_value=order)

    def save_db_record_id(self, order: TS_Order, db_record_id: str) -> None:
        self.__order_cache.save_db_record_id(order=order, db_record_id=db_record_id)

    def is_order_exist(self, order: TS_Order) -> bool:
        return self.__order_cache.is_order_exist(order=order)

    def is_db_record_id_exist(self, order: TS_Order) -> bool:
        return self.__order_cache.is_db_record_id_exist(order=order)

    def get_strategy_name(self) -> str:
        return self.__strategy_name

    def get_order(self, order_id: str) -> Union[bool, TS_Order]:
        order = self.__order_cache.get_order(order_id=order_id)
        if None is order:
            return (False, None)
        else:
            return (True, order)

    def get_orders(self, last_n: int) -> List[TS_Order]:
        return self.__order_cache.get_orders(last_n=last_n)

    def get_order_latest_snapshot(self, platform_order_id: str) -> Union[bool, TS_Order]:
        order = self.__order_cache.get_order_latest_snapshot(platform_order_id=platform_order_id)
        if None is order:
            return (False, None)
        else:
            return (True, order)

    def get_db_record_id(self, platform_order_id: str) -> Union[bool, str]:
        db_record_id = self.__order_cache.get_db_record_id(platform_order_id=platform_order_id)
        if None is db_record_id:
            return (False, None)
        else:
            return (True, db_record_id)

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
