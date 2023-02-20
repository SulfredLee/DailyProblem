import logging
import threading
from typing import List, Dict, Tuple, Union, Any

from sfdevtools.data_cache.DPage import DPage
from sfdevtools.data_cache.DStrategy import DStrategy
from sfdevtools.data_cache.DComponents import StrategyInsight, TS_Order, TS_Trade
import sfdevtools.grpc_protos.ts_cop_pb2 as ts_cop_pb2
import sfdevtools.grpc_protos.ts_cop_pb2_grpc as ts_cop_pb2_grpc

class DCache(object):
    def __init__(self):
        self.__logger: logging.Logger = None
        self.__pages: Dict[str, DPage] = None # key: QC Symbol ID, value: data page
        self.__strategy: DStrategy = DStrategy()
        self.__page_mutex: threading.Lock = threading.Lock()

    def init_component(self, logger: logging.Logger):
        self.__logger = logger
        self.__strategy.init_component(logger=self.__logger)

    def get_strategy_insight(self) -> List[StrategyInsight]:
        return self.__strategy.get_strategy_insight()

    def save_si(self, si: List[StrategyInsight]) -> bool:
        return self.__strategy.save_si(si=si)

    def get_ci_id(self) -> str:
        return self.__strategy.get_ci_id()

    def get_order(self, qc_order_id: int) -> Union[bool, TS_Order]:
        return self.__strategy.get_order(qc_order_id=qc_order_id)

    def save_ci(self, ci: Dict[str, Any]) -> None:
        self.__strategy.save_ci(ci=ci)

    def save_ci_id(self, ci_id: str) -> None:
        self.__strategy.save_ci_id(ci_id=ci_id)

    def save_orders(self, orders: List[TS_Order]) -> None:
        self.__strategy.save_orders(orders=orders)

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

        # handle extra strategy level
        if fid_num == ts_cop_pb2.FidNum.CI:
            for ci in fid_value:
                self.save_ci(ci=ci)
        elif fid_num == ts_cop_pb2.FidNum.SI:
            self.save_si(si=fid_value)
        elif fid_num == ts_cop_pb2.FidNum.Order:
            self.save_orders(orders=fid_value)
        elif fid_num == ts_cop_pb2.FidNum.Trade:
            self.save_trades(trades=fid_value)

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

    def get_create_dpage(self, page_id: str) -> DPage:
        with self.__page_mutex:
            if page_id in self.__pages:
                return self.__pages[page_id]
            else:
                return self.__create_dpage(page_id=page_id)

    def __create_dpage(self, page_id: str) -> DPage:
        with self.__page_mutex:
            new_dpage = DPage()
            new_dpage.init_component(logger=self.__logger)
            self.__create_dpage[page_id] = new_dpage
            return new_dpage
