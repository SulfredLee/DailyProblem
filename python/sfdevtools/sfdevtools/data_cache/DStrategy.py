import logging
import threading
from typing import List, Dict, Tuple, Union, Any

from sfdevtools.data_cache.DComponents import StrategyInsight, TS_Order, TS_Trade
import sfdevtools.grpc_protos.ts_cop_pb2 as ts_cop_pb2
import sfdevtools.grpc_protos.ts_cop_pb2_grpc as ts_cop_pb2_grpc

class DStrategy(object):
    def __init__(self):
        self.__logger: logging.Logger = None
        self.__si: List[StrategyInsight] = list() # strategy insight
        self.__ci_list: List[Dict[str, Any]] = list() # calculation insight
        self.__ci: Dict[str, Any] = dict()
        self.__ci_id: str = ""
        self.__orders: Dict[int, TS_Order] = dict() # key: qc_order_id --- keep latest snapshot
        self.__order_list: List[TS_Order] = list() # store all historical orders
        self.__trade_list: List[TS_Trade] = list() # store all historical trades
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

    def init_component(self, logger: logging.Logger) -> None:
        self.__logger = logger

    def get_strategy_insight(self) -> List[StrategyInsight]:
        with self.__mutex:
            return self.__si

    def save_si(self, si: List[StrategyInsight]) -> bool:
        sorted_si = sorted(si, key=lambda x: x.symbol)
        with self.__mutex:
            if self.__is_same_si(si1=self.__si, si2=sorted_si):
                return False
            else:
                self.__si = sorted_si
                return True
        return False

    def get_si(self) -> List[StrategyInsight]:
        with self.__mutex:
            return self.__si

    def save_ci(self, ci: Dict[str, Any]) -> None:
        with self.__mutex:
            self.__ci = ci
            # self.__ci_list.append(ci)

    def get_ci(self) -> Dict[str, Any]:
        with self.__mutex:
            return self.__ci

    def save_ci_id(self, ci_id: str) -> None:
        with self.__mutex:
            self.__ci_id = ci_id

    def get_ci_id(self) -> str:
        with self.__mutex:
            return self.__ci_id

    def save_orders(self, orders: List[TS_Order]) -> None:
        with self.__mutex:
            for order in orders:
                self.__orders[order.qc_order_id] = order

            self.__order_list.extend(orders)

    def save_trades(self, trades: List[TS_Trade]) -> None:
        with self.__mutex:
            self.__trade_list.extend(trades)

    def get_trades(self) -> List[TS_Trade]:
        with self.__mutex:
            return self.__trade_list

    def get_order(self, qc_order_id: int) -> Union[bool, TS_Order]:
        with self.__mutex:
            if qc_order_id in self.__orders:
                return (True, self.__orders[qc_order_id])
            else:
                return (False, None)

    def get_orders(self) -> List[TS_Order]:
        with self.__mutex:
            return self.__order_list

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
        for a, b in zip(si1, si2):
            if a != b:
                return False
        return True
