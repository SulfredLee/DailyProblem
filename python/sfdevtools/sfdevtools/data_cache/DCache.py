import logging
import threading
from typing import List, Dict, Tuple, Union, Any

from sfdevtools.data_cache.DPage import DPage
from sfdevtools.data_cache.DStrategy import DStrategy
from sfdevtools.data_cache.DComponents import StrategyInsight, TS_Order, TS_Trade
import sfdevtools.data_cache.DTimelyCache as TimelyCache
import sfdevtools.grpc_protos.ts_cop_pb2 as ts_cop_pb2
import sfdevtools.grpc_protos.ts_cop_pb2_grpc as ts_cop_pb2_grpc

class DCache(object):
    def __init__(self):
        self.__logger: logging.Logger = None
        self.__pages: Dict[str, DPage] = None # key: QC Symbol ID, value: data page
        self.__strategy: DStrategy = DStrategy()
        self.__page_mutex: threading.Lock = threading.Lock()
        self.__update_cb: Any = None
        self.__cache_name: str = None

    def init_component(self
                       , logger: logging.Logger
                       , update_cb
                       , cache_name: str
                       , max_hist_orders: int = 1000
                       , max_hist_trades: int = 1000
                       , max_hist_si: int = 1000) -> None:
        self.__logger = logger
        self.__cache_name = cache_name
        self.__update_cb = update_cb
        self.__strategy.init_component(logger=self.__logger
                                       , update_cb=self.__update_cb
                                       , strategy_name=cache_name
                                       , get_parent_dcache_fun=self.__get_self
                                       , max_hist_orders=max_hist_orders
                                       , max_hist_si=max_hist_si
                                       , max_hist_trades=max_hist_trades)
        self.__pages = dict()

    def save_si(self, si: List[StrategyInsight]) -> bool:
        return self.__strategy.save_si(si=si)

    def is_latest_si(self, si: List[StrategyInsight]) -> bool:
        return self.__strategy.is_latest_si(si=si)

    def is_si_exist(self, si: List[StrategyInsight]) -> bool:
        return self.__strategy.is_si_exist(si=si)

    def is_ci_exist(self, ci: Dict[str, Any]) -> bool:
        return self.__strategy.is_ci_exist(ci=ci)

    def get_ci(self) -> Dict[str, Any]:
        return self.__strategy.get_ci()

    def get_ci_id(self) -> str:
        return self.__strategy.get_ci_id()

    def is_order_exist(self, order: TS_Order) -> bool:
        return self.__strategy.is_order_exist(order=order)

    def is_db_record_id_exist(self, order: TS_Order) -> bool:
        return self.__strategy.is_db_record_id_exist(order=order)

    def get_order_latest_snapshot(self, platform_order_id: str) -> Union[bool, TS_Order]:
        return self.__strategy.get_order_latest_snapshot(platform_order_id=platform_order_id)

    def get_db_record_id(self, platform_order_id: str) -> Union[bool, str]:
        return self.__strategy.get_db_record_id(platform_order_id=platform_order_id)

    def get_order(self, order_id: str) -> Union[bool, TS_Order]:
        return self.__strategy.get_order(order_id=order_id)

    def save_ci(self, ci: Dict[str, Any]) -> None:
        self.__strategy.save_ci(ci=ci)

    def save_ci_id(self, ci_id: str) -> None:
        self.__strategy.save_ci_id(ci_id=ci_id)

    def save_order(self, order: TS_Order) -> None:
        self.__strategy.save_order(order=order)

    def save_orders(self, orders: List[TS_Order]) -> None:
        self.__strategy.save_orders(orders=orders)

    def save_db_record_id(self, order: TS_Order, db_record_id: str) -> None:
        self.__strategy.save_db_record_id(order=order, db_record_id=db_record_id)

    def is_trade_exist(self, trade: TS_Trade) -> bool:
        return self.__strategy.is_trade_exist(trade=trade)

    def get_trade(self, trade_id: str) -> Union[bool, TS_Trade]:
        return self.__strategy.get_trade(trade_id=trade_id)

    def save_trade(self, trade: TS_Trade) -> None:
        self.__strategy.save_trade(trade=trade)

    def save_trades(self, trades: List[TS_Trade]) -> None:
        self.__strategy.save_trades(trades=trades)

    def save_fid(self
                 , msg_id: str
                 , msg_type: ts_cop_pb2.Cop.MsgType
                 , fid_num: int
                 , fid_value: Any) -> None:

        # handle strategy level
        if msg_type == ts_cop_pb2.Cop.MsgType.Strategy:
            self.__strategy.save_fid(fid_num=fid_num, fid_value=fid_value)
            return

        # handle page level
        dpage = self.get_create_dpage(page_id=msg_id)
        dpage.save_fid(fid_num=fid_num, fid_value=fid_value)

    def get_cache_name(self) -> str:
        return self.__cache_name

    def get_page_fids(self
                 , page_id: str) -> List[Union[int, Any]]:
        dpage = self.get_create_dpage(page_id=msg_id)
        return dpage.get_fids()

    def get_strategy_fids(self) -> List[Union[int, Any]]:
        return self.__strategy.get_fids()

    def get_fid(self
                , msg_id: str
                , msg_type: ts_cop_pb2.Cop.MsgType
                , fid_num: int) -> Union[bool, Union[bool, Any]]:
        # handle strategy level
        if msg_type == ts_cop_pb2.Cop.MsgType.Strategy:
            return self.__strategy.get_fid(fid_num=fid_num)

        # handle page level
        dpage = self.get_create_dpage(page_id=msg_id)
        return dpage.get_fid(fid_num=fid_num)

    def get_page_name(self) -> List[str]:
        with self.__page_mutex:
            return [page_id for page_id, page in self.__pages.items()]

    def get_page_count(self) -> int:
        with self.__page_mutex:
            return len(self.__pages)

    def get_strgy(self) -> DStrategy:
        return self.__strategy

    def get_create_dpage(self, page_id: str) -> DPage:
        with self.__page_mutex:
            if page_id in self.__pages:
                return self.__pages[page_id]
            else:
                new_dpage = DPage()
                new_dpage.init_component(logger=self.__logger
                                         , update_cb=self.__update_cb
                                         , page_id=page_id
                                         , get_parent_dcache_fun=self.__get_self
                                         , save_other_map=dict()
                                         , get_other_map=dict())
                self.__pages[page_id] = new_dpage
                return new_dpage

    def __get_self(self) -> Any:
        return self
