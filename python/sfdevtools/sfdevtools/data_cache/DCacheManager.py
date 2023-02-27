import logging
import threading
from typing import List, Dict, Tuple, Union, Any

from sfdevtools.data_cache.DCache import DCache
from sfdevtools.data_cache.DPage import DPage
from sfdevtools.data_cache.DStrategy import DStrategy
from sfdevtools.data_cache.DComponents import StrategyInsight, TS_Order, TS_Trade
import sfdevtools.data_cache.DTimelyCache as TimelyCache
import sfdevtools.grpc_protos.ts_cop_pb2 as ts_cop_pb2
import sfdevtools.grpc_protos.ts_cop_pb2_grpc as ts_cop_pb2_grpc

class DCacheManager(object):
    def __init__(self):
        self.__logger: logging.Logger = None
        self.__dcache: Dict[str, DCache] = dict() # key: cache name, value: dcache
        self.__mutex: threading.Lock = threading.Lock()

    def init_component(self
                       , logger: logging.Logger
                       , max_hist_orders: int = 1000
                       , max_hist_si: int = 1000
                       , max_hist_trades: int = 1000) -> None:
        self.__logger = logger
        self.__max_hist_orders = max_hist_orders
        self.__max_hist_si = max_hist_si
        self.__max_hist_trades = max_hist_trades

    def create_cache(self
                     , cache_name: str) -> DCache:
        with self.__mutex:
            if cache_name not in self.__dcache:
                self.__logger.info(f"Create DCache with name: {cache_name}")
                new_dcache = DCache()
                self.__dcache[cache_name] = new_dcache
                new_dcache.init_component(logger=self.__logger
                                          , max_hist_orders=self.__max_hist_orders
                                          , max_hist_si=self.__max_hist_si
                                          , max_hist_trades=self.__max_hist_trades)
                return new_dcache
            else:
                return self.__dcache[cache_name]

    def get_cache_name(self) -> List[str]:
        with self.__mutex:
            return [k for k, v in self.__dcache.items()]

    def get_total_cache_count(self) -> int:
        with self.__mutex:
            return len(self.__dcache)

    def get_page_name(self) -> List[Union[str, str]]:
        with self.__mutex:
            all_page_name: List[Union[str, str]] = list()
            for cache_name, dcache in self.__dcache.items():
                page_names = dcache.get_page_name()

                all_page_name.extend([(cache_name, page_name) for page_name in page_names])

            return all_page_name

    def get_page(self
                 , cache_name: str
                 , page_id: str) -> Union[bool, DPage]:
        ret, dcache = self.get_cache(cache_name=cache_name)
        if not ret:
            return (False, None)
        return (True, dcache.get_create_dpage(page_id=page_id))

    def get_total_page_count(self) -> int:
        with self.__mutex:
            total_count = 0
            for cache_name, dcache in self.__dcache.items():
                total_count += dcache.get_page_count()

            return total_count

    def get_strgy(self
                  , cache_name: str) -> Union[bool, DStrategy]:
        ret, dcache = self.get_cache(cache_name=cache_name)
        if not ret:
            return (False, None)
        return (True, dcache.get_strgy())

    def get_cache(self, cache_name: str) -> Union[bool, DCache]:
        with self.__mutex:
            if cache_name in self.__dcache:
                return (True, self.__dcache[cache_name])
            else:
                return (False, None)

    def save_si(self
                , cache_name: str
                , si: List[StrategyInsight]) -> Union[bool, bool]:
        dcache = self.create_cache(cache_name=cache_name)
        return (True, dcache.save_si(si=si))

    def is_latest_si(self, cache_name: str, si: List[StrategyInsight]) -> Union[bool, bool]:
        ret, dcache = self.get_cache(cache_name=cache_name)
        if not ret:
            return (False, None)
        return (True, dcache.is_latest_si(si=si))

    def is_si_exist(self, cache_name: str, si_id: str) -> Union[bool, bool]:
        ret, dcache = self.get_cache(cache_name=cache_name)
        if not ret:
            return (False, None)
        return (True, dcache.is_si_exist(si_id=si_id))

    def is_ci_exist(self, cache_name: str, ci: Dict[str, Any]) -> Union[bool, bool]:
        ret, dcache = self.get_cache(cache_name=cache_name)
        if not ret:
            return (False, None)
        return (True, dcache.is_ci_exist(ci=ci))

    def get_ci(self, cache_name: str) -> Union[bool, Dict[str, Any]]:
        ret, dcache = self.get_cache(cache_name=cache_name)
        if not ret:
            return (False, None)
        return (True, dcache.get_ci())

    def get_ci_id(self, cache_name: str) -> Union[bool, str]:
        ret, dcache = self.get_cache(cache_name=cache_name)
        if not ret:
            return (False, None)
        return (True, dcache.get_ci_id())

    def is_order_exist(self, cache_name: str, platform_order_id: str) -> Union[bool, bool]:
        ret, dcache = self.get_cache(cache_name=cache_name)
        if not ret:
            return (False, None)
        return (True, dcache.is_order_exist(platform_order_id=platform_order_id))

    def get_trade(self, cache_name: str, trade_id: str) -> Union[bool, Union[bool, TS_Trade]]:
        ret, dcache = self.get_cache(cache_name=cache_name)
        if not ret:
            return (False, (False, None))
        return (True, dcache.get_trade(trade_id=trade_id))

    def get_order(self, cache_name: str, platform_order_id: str) -> Union[bool, Union[bool, TS_Order]]:
        ret, dcache = self.get_cache(cache_name=cache_name)
        if not ret:
            return (False, (False, None))
        return (True, dcache.get_order(platform_order_id=platform_order_id))

    def save_ci(self, cache_name: str, ci: Dict[str, Any]) -> bool:
        dcache = self.create_cache(cache_name=cache_name)
        dcache.save_ci(ci=ci)
        return True

    def save_ci_id(self, cache_name: str, ci_id: str) -> bool:
        dcache = self.create_cache(cache_name=cache_name)
        dcache.save_ci_id(ci_id=ci_id)
        return True

    def save_order(self, cache_name: str, order: TS_Order) -> bool:
        dcache = self.create_cache(cache_name=cache_name)
        dcache.save_order(order=order)
        return True

    def save_orders(self, cache_name: str, orders: List[TS_Order]) -> bool:
        dcache = self.create_cache(cache_name=cache_name)
        dcache.save_orders(orders=orders)
        return True

    def is_trade_exist(self, cache_name: str, trade_id: str) -> Union[bool, bool]:
        ret, dcache = self.get_cache(cache_name=cache_name)
        if not ret:
            return (False, None)
        return (True, dcache.is_trade_exist(trade_id=trade_id))

    def save_trade(self, cache_name: str, trade: TS_Trade) -> None:
        dcache = self.create_cache(cache_name=cache_name)
        dcache.save_trade(trade=trade)
        return None

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

    def get_fids(self
                 , cache_name: str
                 , page_id: str) -> Union[bool, Union[bool, List[Union[int, Any]]]]:
        ret, dcache = self.get_cache(cache_name=cache_name)
        if not ret:
            return (False, (False, None))
        return (True, dcache.get_fids(page_id=page_id))

    def get_fid(self
                , cache_name: str
                , msg_id: str
                , msg_type: ts_cop_pb2.Cop.MsgType
                , fid_num: int) -> Union[bool, Union[bool, Union[bool, Any]]]:
        ret, dcache = self.get_cache(cache_name=cache_name)
        if not ret:
            return (False, (False, None))
        return (True, dcache.get_fid(msg_id=msg_id
                                     , msg_type=msg_type
                                     , fid_num=fid_num))
    def get_order_snapshot_cache(self
                                 , cache_name: str) -> TimelyCache.TimelyCache_Snapshot:
        dcache = self.create_cache(cache_name=cache_name)
        return dcache.get_order_snapshot_cache()

    def get_order_hist_cache(self
                             , cache_name: str) -> TimelyCache.TimelyCache_Hist:
        dcache = self.create_cache(cache_name=cache_name)
        return dcache.get_order_hist_cache()
