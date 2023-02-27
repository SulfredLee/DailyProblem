import logging
import threading
from typing import List, Dict, Tuple, Union, Any
import copy
import json
import hashlib

from sfdevtools.data_cache.DComponents import StrategyInsight, TS_Order, TS_Trade
import sfdevtools.data_cache.DTimelyCache as TimelyCache
import sfdevtools.grpc_protos.ts_cop_pb2 as ts_cop_pb2
import sfdevtools.grpc_protos.ts_cop_pb2_grpc as ts_cop_pb2_grpc

class DStrategy(object):
    def __init__(self):
        self.__logger: logging.Logger = None
        self.__max_hist_orders: int = 1000
        self.__max_hist_trades: int = 1000
        self.__max_hist_si: int = 1000
        self.__si_dict: Dict[str, List[StrategyInsight]] = dict() # key: si_id
        self.__si_list: List[str] = list() # List of si_id
        self.__ci_id: str = ""
        self.__ci_cache: TimelyCache.TimelyCache_Hist = TimelyCache.TimelyCache_Hist() # key: ci_id --- keep a limited list of latest records
        self.__order_cache: TimelyCache.TimelyCache_Snapshot = TimelyCache.TimelyCache_Snapshot() # key: platform_order_id --- keep latest snapshot
        self.__trade_cache: TimelyCache.TimelyCache_Hist = TimelyCache.TimelyCache_Hist() # key: trade_id --- keep latest records in hash
        self.__mutex: threading.Lock = threading.Lock()

        self.__int_mutex: threading.Lock = threading.Lock()
        self.__float_mutex: threading.Lock = threading.Lock()
        self.__str_mutex: threading.Lock = threading.Lock()
        self.__bool_mutex: threading.Lock = threading.Lock()
        self.__other_mutex: threading.Lock = threading.Lock()
        self.__int32_map: Dict[int, int] = dict()
        self.__int64_map: Dict[int, int] = dict()
        self.__float_map: Dict[int, float] = dict()
        self.__double_map: Dict[int, float] = dict()
        self.__string_map: Dict[int, str] = dict()
        self.__bool_map: Dict[int, bool] = dict()

        self.__save_map: Dict[int, Any] = {
            0: self.__save_fid_int32
            , 1: self.__save_fid_int64
            , 2: self.__save_fid_float
            , 3: self.__save_fid_double
            , 4: self.__save_fid_string
            , 5: self.__save_fid_other
            , 6: self.__save_fid_bool
        }
        self.__get_map: Dict[int, Any] = {
            0: self.__get_fid_int32
            , 1: self.__get_fid_int64
            , 2: self.__get_fid_float
            , 3: self.__get_fid_double
            , 4: self.__get_fid_string
            , 5: self.__get_fid_other
            , 6: self.__get_fid_bool
        }
        self.__save_other_map: Dict[int, Any] = {
            ts_cop_pb2.Cop.FidNum.CI: self.save_ci
            , ts_cop_pb2.Cop.FidNum.SI: self.save_si
            , ts_cop_pb2.Cop.FidNum.Order: self.save_orders
            , ts_cop_pb2.Cop.FidNum.Trade: self.save_trades
        }
        self.__get_other_map: Dict[int, Any] = {
            ts_cop_pb2.Cop.FidNum.CI: self.get_ci
            , ts_cop_pb2.Cop.FidNum.SI: self.get_si
            , ts_cop_pb2.Cop.FidNum.Order: self.get_orders
            , ts_cop_pb2.Cop.FidNum.Trade: self.get_trades
        }
        self.__bucket_size = 10000

    def init_component(self
                       , logger: logging.Logger
                       , max_hist_orders: int = 1000
                       , max_hist_trades: int = 1000
                       , max_hist_si: int = 1000) -> None:
        self.__logger = logger
        self.__max_hist_orders = max_hist_orders
        self.__max_hist_trades = max_hist_trades
        self.__max_hist_si = max_hist_si

    def get_strategy_insight(self) -> List[StrategyInsight]:
        with self.__mutex:
            return self.__si_list

    def save_si(self, si: List[StrategyInsight]) -> bool:
        with self.__mutex:
            if len(si) == 0:
                return True

            self.__si_list.append(si[0].si_id)
            self.__si_dict[si[0].si_id] = si

            # remove old records
            if len(self.__si_list) > self.__max_hist_si:
                extra_records = len(self.__si_list) - self.__max_hist_si
                # remove records from dictionary
                for old_si_id in self.__si_list[:extra_records]:
                    if old_si_id in self.__si_dict:
                        del self.__si_dict[old_si_id]

                # remove records from list
                del self.__si_list[:extra_records]

            return True
        return False

    def is_latest_si(self, si: List[StrategyInsight]) -> bool:
        with self.__mutex:
            return self.__is_same_si(si1=self.__si_list, si2=si)

    def is_ci_exist(self, ci: Dict[str, Any]) -> bool:
        return self.__ci_cache.is_exist(key=hashlib.md5(json.dumps(ci, sort_keys=True).encode("utf-8")).digest())

    def is_si_exist(self, si_id: str) -> bool:
        with self.__mutex:
            return si_id in self.__si_dict

    def get_si(self) -> List[StrategyInsight]:
        with self.__mutex:
            return self.__si_dict[self.__si_list[-1]] # get latest si_id from self.__si_list

    def save_ci(self, ci: Dict[str, Any]) -> None:
        self.__ci_cache.upsert_ele(key=hashlib.md5(json.dumps(ci, sort_keys=True).encode("utf-8")).digest(), value=ci)

    def get_ci(self) -> Dict[str, Any]:
        return self.__ci_cache.get_records_by_index(idx=-1)

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

    def __remove_old_orders(self
                            , order_list: List[TS_Order]
                            , order_dict: Dict[str, TS_Order]
                            , max_records: int) -> None:
        if len(order_dict) > max_records:
            # find old records
            extra_records = len(order_dict) - max_records
            old_record_count = 0
            old_idx_from_list = 0
            old_ids: List[str] = list()
            # find old order_id from order_list
            while old_record_count <= extra_records:
                for idx, old_record in enumerate(order_list):
                    if old_record.order_id == cur_order_id:
                        continue
                    else:
                        cur_order_id = old_record.order_id
                        old_record_count += 1
                        if old_record_count <= extra_records:
                            old_ids.append(cur_order_id)
                            old_idx_from_list = idx
                        break
            # remove records from dictionary
            for old_order_id in old_ids:
                if old_order_id in order_dict:
                    del order_dict[old_order_id]
            # remove records from list
            del order_list[:old_idx_from_list + 1]

    def save_trade(self, trade: TS_Trade) -> None:
        self.__trade_cache.upsert_ele(key=trade.trade_id, value=trade)

    def save_trades(self, trades: List[TS_Trade]) -> None:
        self.__trade_cache.upsert_multi(keys=[trade.trade_id for trade in trades], values=trades)

    def __remove_old_trades(self
                            , trade_list: List[TS_Trade]
                            , trade_dict: Dict[str, TS_Trade]
                            , max_records: int) -> None:
        # remove old records
        if len(trade_list) > max_records:
            extra_records = len(trade_list) - max_records
            # remove records from dictionary
            for old_record in trade_list[:extra_records]:
                if old_record.trade_id in trade_dict:
                    del trade_dict[old_record.trade_id]
            # remove records from list
            del trade_list[:extra_records]

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
        bucket_num = int((fid_num - 1) / self.__bucket_size)
        if bucket_num not in self.__save_map:
            return None
        self.__save_map[bucket_num](fid_num=fid_num, fid_value=fid_value)

    def get_fid(self, fid_num: int) -> Union[bool, Any]:
        bucket_num = int((fid_num - 1) / self.__bucket_size)
        if bucket_num not in self.__get_map:
            return (False, None)

        return (True, self.__get_map[bucket_num](fid_num=fid_num))

    def __save_fid_int32(self, fid_num: int, fid_value: int) -> None:
        with self.__int_mutex:
            self.__int32_map[fid_num] = fid_value

    def __save_fid_int64(self, fid_num: int, fid_value: int) -> None:
        with self.__int_mutex:
            self.__int64_map[fid_num] = fid_value

    def __save_fid_float(self, fid_num: int, fid_value: float) -> None:
        with self.__float_mutex:
            self.__float_map[fid_num] = fid_value

    def __save_fid_double(self, fid_num: int, fid_value: float) -> None:
        with self.__float_mutex:
            self.__double_map[fid_num] = fid_value

    def __save_fid_string(self, fid_num: int, fid_value: str) -> None:
        with self.__str_mutex:
            self.__string_map[fid_num] = fid_value

    def __save_fid_bool(self, fid_num: int, fid_value: float) -> None:
        with self.__bool_mutex:
            self.__bool_map[fid_num] = fid_value

    def __save_fid_other(self, fid_num: int, fid_value: Any) -> None:
        with self.__other_mutex:
            if fid_num not in self.__save_other_map:
                return None

            self.__save_other_map[fid_num](fid_value)
            return None

    def __get_fid_int32(self, fid_num: int) -> Union[bool, int]:
        with self.__int_mutex:
            if fid_num in self.__int32_map:
                return (True, self.__int32_map[fid_num])
            else:
                return (False, None)

    def __get_fid_int64(self, fid_num: int) -> Union[bool, int]:
        with self.__int_mutex:
            if fid_num in self.__int64_map:
                return (True, self.__int64_map[fid_num])
            else:
                return (False, None)

    def __get_fid_float(self, fid_num: int) -> Union[bool, float]:
        with self.__float_mutex:
            if fid_num in self.__float_map:
                return (True, self.__float_map[fid_num])
            else:
                return (False, None)

    def __get_fid_double(self, fid_num: int) -> Union[bool, float]:
        with self.__float_mutex:
            if fid_num in self.__double_map:
                return (True, self.__double_map[fid_num])
            else:
                return (False, None)

    def __get_fid_string(self, fid_num: int) -> Union[bool, str]:
        with self.__str_mutex:
            if fid_num in self.__str_map:
                return (True, self.__str_map[fid_num])
            else:
                return (False, None)

    def __get_fid_bool(self, fid_num: int) -> Union[bool, bool]:
        with self.__bool_mutex:
            if fid_num in self.__bool_map:
                return (True, self.__bool_map[fid_num])
            else:
                return (False, None)

    def __get_fid_other(self, fid_num: int) -> Union[bool, Any]:
        with self.__other_mutex:
            if fid_num in self.__get_other_map:
                return (True, self.__get_other_map[fid_num]())
            else:
                return (False, None)

    def __is_same_si(self, si1: List[StrategyInsight], si2: List[StrategyInsight]) -> bool:
        if len(si1) != len(si2):
            return False

        si1_sorted = sorted(si1, key=lambda x: x.symbol_id)
        si2_sorted = sorted(si2, key=lambda x: x.symbol_id)
        for a, b in zip(si1_sorted, si2_sorted):
            if a != b:
                return False
        return True
