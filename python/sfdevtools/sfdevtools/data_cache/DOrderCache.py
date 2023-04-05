import logging
import threading
from typing import List, Dict, Any, Union

import sfdevtools.data_cache.DTimelyCache as TimelyCache
from sfdevtools.data_cache.DComponents import TS_Order

class DOrderCache(object):
    def __init__(self):
        self.__logger: logging.Logger = None
        self.__mutex: threading.Lock = None
        self.__db_id_hist: TimelyCache.TimelyCache_Hist = None # key: platform_order_id, value: db_record_id
        self.__order_hist: TimelyCache.TimelyCache_Hist = None # key: order_id, value: TS_Order
        self.__order_snapshot: TimelyCache.TimelyCache_Snapshot = None # key: platform_order_id, value: TS_Order
        self.__eq_fun: Any = None

    def init_component(self
                       , logger: logging.Logger
                       , order_hist: TimelyCache.TimelyCache_Hist
                       , order_snapshot: TimelyCache.TimelyCache_Snapshot
                       , db_id_hist: TimelyCache.TimelyCache_Hist
                       , eq_fun: Any = None) -> None:
        self.__logger = logger
        self.__order_hist = order_hist
        self.__order_snapshot = order_snapshot
        self.__db_id_hist = db_id_hist
        self.__mutex = threading.Lock()
        self.__eq_fun = eq_fun

    def save_orders(self, orders=List[TS_Order]) -> List[bool]:
        is_new_list: List[bool] = list()
        if len(orders) == 0:
            return [False]

        with self.__mutex:
            is_need_full_update = False
            for order in orders:
                is_new_list.append(self.__save_order_imp(order=order))
                if is_new_list[-1]:
                    is_need_full_update = True

            if is_need_full_update:
                for order in orders:
                    self.__order_snapshot.upsert_ele(key=order.platform_order_id, value=order)

            return is_new_list
        return [False] * len(orders)

    def save_order(self, order: TS_Order) -> bool:
        with self.__mutex:
            is_new = self.__save_order_imp(order=order)
            if is_new:
                self.__order_snapshot.upsert_ele(key=order.platform_order_id, value=order)

            return is_new
        return False

    def save_db_record_id(self, order: TS_Order, db_record_id: str) -> bool:
        is_new = False

        with self.__mutex:
            if not self.__db_id_hist.is_exist(key=order.platform_order_id):
                # found new record
                is_new = True

                self.__db_id_hist.upsert_ele(key=order.platform_order_id, value=db_record_id)
            else:
                if self.__db_id_hist.get_ele(key=order.platform_order_id) == db_record_id:
                    # found old record
                    is_new = False
                else:
                    # found new record
                    is_new = True

                    self.__db_id_hist.upsert_ele(key=order.platform_order_id, value=db_record_id)

        return is_new

    def is_order_exist(self, order: TS_Order) -> bool:
        with self.__mutex:
            return self.__order_hist.is_exist(key=order.order_id)

    def is_db_record_id_exist(self, order: TS_Order) -> bool:
        with self.__mutex:
            if self.__db_id_hist.is_exist(key=order.platform_order_id)\
               and self.__db_id_hist.get_ele(key=order.platform_order_id) is not None:
                return True
            else:
                return False

    def get_order(self, order_id: int) -> TS_Order:
        with self.__mutex:
            if self.__order_hist.is_exist(key=order_id):
                return self.__order_hist.get_ele(key=order_id)
            else:
                return None

    def get_orders(self, last_n: int = 10) -> List[TS_Order]:
        with self.__mutex:
            return self.__order_hist.get_last_n_records_in_time_series(n=last_n)

    def get_order_latest_snapshot(self, platform_order_id: str) -> TS_Order:
        with self.__mutex:
            if self.__order_snapshot.is_exist(key=platform_order_id):
                return self.__order_snapshot.get_ele(key=platform_order_id)
            else:
                return None

    def get_db_record_id(self, platform_order_id: str) -> str:
        with self.__mutex:
            if self.__db_id_hist.is_exist(key=platform_order_id):
                return self.__db_id_hist.get_ele(key=platform_order_id)
            else:
                return None

    def __save_order_imp(self, order: TS_Order) -> bool:
        is_new = False
        if not self.__order_hist.is_exist(key=order.order_id):
            # found new record
            is_new = True

            self.__order_hist.upsert_ele(key=order.order_id, value=order)
        else:
            if (self.__eq_fun is not None and self.__eq_fun(first=self.__order_hist.get_ele(key=order.order_id), second=order)\
                or self.__order_hist.get_ele(key=order.order_id) == order):
                # found old record
                is_new = False
            else:
                # found new record
                is_new = True

                self.__order_hist.upsert_ele(key=order.order_id, value=order)

        return is_new
