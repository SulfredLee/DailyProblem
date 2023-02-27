from typing import List, Dict, Any
import logging
import threading
import signal

import sfdevtools.data_control.TSDataCtrl as TSDataCtrl
import sfdevtools.grpc_protos.ts_cop_pb2 as ts_cop_pb2
import sfdevtools.grpc_protos.ts_cop_pb2_grpc as ts_cop_pb2_grpc
from sfdevtools.data_cache.DComponents import StrategyInsight, TS_Order, TS_Trade
import sfdevtools.data_cache.DConverter as dconv
from sfdevtools.data_cache.DCacheManager import DCacheManager
from sfdevtools.devTools.AtomicData import AtomicData
from sfdevtools.devTools.DiscontinueSeelp import DiscontinueSeelp

class TSBackgroundCtrl(object):
    def __init__(self):
        self.__logger: logging.Logger = None
        self.__bg_cycle_sec: int = 600
        self.__bg_interval_sec: int = 20
        self.__dcache_m: DCacheManager = None
        self.__is_running: AtomicData = AtomicData()
        self.__is_running.save(user_data=False)
        self.__dsleep: DiscontinueSeelp = None
        self.__send_cop_fun: Any = None

        self.__page_list: List[Union[str, str]] = list()
        self.__strgy_list: List[str] = list()

        self.__bg_th: threading.Thread = threading.Thread(target=self.__main)

        signal.signal(signal.SIGINT, self.__cleanup)

    def init_component(self
                       , logger: logging.Logger
                       , dcache_m: DCacheManager
                       , send_cop_fun: Any
                       , bg_cycle_sec: int = 600
                       , bg_interval_sec: int = 20):
        self.__logger = logger
        self.__dcache_m = dcache_m
        self.__send_cop_fun = send_cop_fun
        self.__bg_cycle_sec = bg_cycle_sec
        self.__bg_interval_sec = bg_interval_sec
        self.__dsleep = DiscontinueSeelp(sleep_time_ms=self.__bg_interval_sec * 1000)

    def start_bg_cycle(self):
        self.__is_running.save(user_data=True)
        self.__bg_th.start()

    def stop_bg_cycle(self):
        self.__is_running.save(user_data=False)
        self.__bg_th.join()

    def __send_bg(self):
        if None is not self.__send_cop_fun:
            return
        # handle page
        if len(self.__page_list) == 0:
            self.__page_list = self.__dcache_m.get_page_name()

        num_page_needed_to_send = max(int(self.__dcache_m.get_total_page_count() / self.__bg_cycle_sec + 0.5), 1)
        for ele in self.__page_list[:num_page_needed_to_send]:
            cache_name = ele[0]
            page_id = ele[1]

            is_page_exist, dpage = self.__dcache_m.get_page(cache_name=cache_name
                                                            , page_id=page_id)
            if not is_page_exist:
                continue

            # convert page to cop
            cop = dconv.conv_page_2_cop(dpage=dpage)
            self.__send_cop_fun(msg_id=page_id, msg_type=ts_cop_pb2.Cop.MsgType.Listing, cop=cop)

        # hanlde strategy
        if len(self.__strgy_list) == 0:
            self.__strgy_list = self.__dcache_m.get_cache_name()

        num_strgy_needed_to_send = max(int(self.__dcache_m.get_total_cache_count() / self.__bg_cycle_sec + 0.5), 1)
        for cache_name in self.__strgy_list:
            is_strgy_exist, strgy = self.__dcache_m.get_strgy(cache_name=cache_name)

            if not is_strgy_exist:
                continue

            # convert strategy to cop
            cop = dconv.conv_strg_2_cop(strgy=strgy)
            self.__send_cop_fun(msg_id=cache_name, msg_type=ts_cop_pb2.Cop.MsgType.Strategy, cop=cop)

    def __main(self):
        self.__logger.info("Start")
        while self.__is_running.get():
            if not self.__is_running.get():
                break

            self.__dsleep.sleep(user_fun=self.__is_running.get)
            if not self.__is_running.get():
                break

            self.__send_bg()

        self.__logger.info("End")

    def __cleanup(self, signum, frame):
        self.stop_bg_cycle()
        exit(0)
