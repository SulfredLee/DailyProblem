import logging
import threading
from typing import List, Dict, Tuple, Union, Any

from sfdevtools.data_cache.DCache import DCache
from sfdevtools.data_cache.DComponents import StrategyInsight, TS_Order, TS_Trade
import sfdevtools.grpc_protos.ts_cop_pb2 as ts_cop_pb2
import sfdevtools.grpc_protos.ts_cop_pb2_grpc as ts_cop_pb2_grpc

class DCacheManager(object):
    def __init__(self):
        self.__logger: logging.Logger = None
        self.__dcache: Dict[str, DCache] = dict() # key: cache name, value: dcache
        self.__mutex: threading.Lock = threading.Lock()

    def init_component(self, logger: logging.Logger) -> None:
        self.__logger = logger

    def create_cache(self, cache_name: str) -> DCache:
        with self.__mutex:
            if cache_name not in self.__dcache:
                self.__logger.info(f"Create DCache with name: {cache_name}")
                new_dcache = DCache()
                self.__dcache[cache_name] = new_dcache
                new_dcache.init_component(self.__logger)
                return new_dcache
            else:
                return self.__dcache[cache_name]

    def get_cache(self, cache_name: str) -> Union[bool, DCache]:
        with self.__mutex:
            if cache_name in self.__dcache:
                return (True, self.__dcache[cache_name])
            else:
                return (False, None)

    def get_strategy_insight(self, cache_name: str) -> Union[bool, List]:
        with self.__mutex:
            if cache_name in self.__dcache:
                return (True, self.__dcache[cache_name].get_strategy_insight())
            else:
                return (False, None)

    def save_si(self
                                , cache_name: str
                                , si: List[StrategyInsight]) -> Union[bool, bool]:
        dcache = self.create_cache(cache_name=cache_name)
        return (True, dcache.save_si(si=si))

    def get_ci_id(self, cache_name: str) -> Union[bool, str]:
        with self.__mutex:
            if cache_name in self.__dcache:
                return (True, self.__dcache[cache_name].get_ci_id())
            else:
                return (False, None)

    def get_order(self, cache_name: str, qc_order_id: int) -> Union[bool, bool, TS_Order]:
        with self.__mutex:
            if cache_name in self.__dcache:
                return (True, self.__dcache[cache_name].get_order(qc_order_id=qc_order_id))
            else:
                return (False, False, None)

    def save_ci(self, cache_name: str, ci: Dict[str, Any]) -> bool:
        dcache = self.create_cache(cache_name=cache_name)
        dcache.save_ci(ci=ci)
        return True

    def save_ci_id(self, cache_name: str, ci_id: str) -> bool:
        dcache = self.create_cache(cache_name=cache_name)
        dcache.save_ci_id(ci_id=ci_id)
        return True

    def save_orders(self, cache_name: str, orders: List[TS_Order]) -> bool:
        dcache = self.create_cache(cache_name=cache_name)
        dcache.save_orders(orders=orders)
        return True

    def save_trades(self, cache_name: str, trades: List[TS_Trade]) -> None:
        dcache = self.create_cache(cache_name=cache_name)
        dcache.save_trades(trades=trades)
        return None

    def save_fid(self
                 , cache_name: str
                 , msg_id: str
                 , msg_type: ts_cop_pb2.Cop.MsgType
                 , fid_num: int
                 , fid_value: Any) -> None:
        dcache = self.create_cache(cache_name=cache_name)
        dcache.save_fid(msg_id=msg_id, msg_type=msg_type, fid_num=fid_num, fid_value=fid_value)

    def get_fid(self
                , cache_name: str
                , msg_id: str
                , msg_type: ts_cop_pb2.Cop.MsgType
                , fid_num: int) -> Union[bool, Union[bool, Union[bool, Any]]]:
        with self.__mutex:
            if cache_name in self.__dcache:
                return (True, self.__dcache[cache_name].get_fid(msg_id=msg_id
                                                                , msg_type=msg_type
                                                                , fid_num=fid_num))
            else:
                return (False, None, None)
