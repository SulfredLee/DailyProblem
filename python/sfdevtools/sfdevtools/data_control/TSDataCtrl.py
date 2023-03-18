import logging
import zmq
import threading
import signal
import math
from typing import Any, List, Dict, Union
import json

import sfdevtools.grpc_protos.ts_cop_pb2 as ts_cop_pb2
import sfdevtools.grpc_protos.ts_cop_pb2_grpc as ts_cop_pb2_grpc
import sfdevtools.grpc_protos.cop_tools as ct

class TSDataCtrl(object):
    def __init__(self):
        self.__logger: logging.Logger = None
        self.__pub_mutex: threading.Lock = threading.Lock()
        self.__sub_mutex: threading.Lock = threading.Lock()
        self.__publisher: zmq.sugar.socket.Socket = None
        self.__subscriber: zmq.sugar.socket.Socket = None
        self.__sender_name: str = ""
        self.__instance_id: int = 0
        self.__strategy_id: str = None
        self.__seq_num: int = 0
        self.__cb_fun = None
        self.__sub_main_thread: threading.Thread = None
        self.__is_subscription_run: bool = False
        self.__sub_timeout_ms: int = 100
        self.__max_byte_limit: int = 1024 * 1024 * 100 # 100 MB
        self.__cur_byte_sent: int = 0
        self.__is_send_limit_alert: bool = True
        self.__is_limit_sending: bool = False

        self.__process_fid_map_smart = {
            7: self.__process_d_int32
            , 8: self.__process_d_int64
            , 9: self.__process_d_float
            , 10: self.__process_d_double
            , 11: self.__process_d_string
            , 12: self.__process_d_bool
            , ts_cop_pb2.Cop.FidNum.CI: self.__process_ci_smart
            , ts_cop_pb2.Cop.FidNum.SI: self.__process_si_smart
            , ts_cop_pb2.Cop.FidNum.Order: self.__process_order_smart
            , ts_cop_pb2.Cop.FidNum.Trade: self.__process_trade_smart
            , ts_cop_pb2.Cop.FidNum.Order_Snap: self.__process_order_smart
        }
        self.__put_value_2_cop_map = {
            7: self.__put_value_d_int32
            , 8: self.__put_value_d_int64
            , 0: self.__put_value_d_float
            , 10: self.__put_value_d_double
            , 11: self.__put_value_d_string
            , 12: self.__put_value_d_bool
            , ts_cop_pb2.Cop.FidNum.CI: self.__put_value_ci
            , ts_cop_pb2.Cop.FidNum.SI: self.__put_value_si
            , ts_cop_pb2.Cop.FidNum.Order: self.__put_value_order
            , ts_cop_pb2.Cop.FidNum.Trade: self.__put_value_trade
            , ts_cop_pb2.Cop.FidNum.Order_Snap: self.__put_value_order
        }
        self.__process_fid_map = {
            1: self.__process_int32
            , 2: self.__process_int64
            , 3: self.__process_float
            , 4: self.__process_double
            , 5: self.__process_string
            , 7: self.__process_bool
            , ts_cop_pb2.Cop.FidNum.CI: self.__process_ci
            , ts_cop_pb2.Cop.FidNum.SI: self.__process_si
            , ts_cop_pb2.Cop.FidNum.Order: self.__process_order
            , ts_cop_pb2.Cop.FidNum.Trade: self.__process_trade
            , ts_cop_pb2.Cop.FidNum.Order_Snap: self.__process_order
        }

    def init_component(self
                       , logger: logging.Logger):
        self.__logger = logger

    def init_publish(self
                     , pub_host: str
                     , pub_port: str
                     , sender_name: str
                     , strategy_id: str
                     , instance_id: int):
        ctx = zmq.Context.instance()
        self.__publisher = ctx.socket(zmq.PUB)
        publisher_url = f"tcp://{pub_host}:{pub_port}"
        self.__logger.info(f"publisher_url: {publisher_url}")
        self.__publisher.connect(publisher_url)
        self.__logger.info("socket connect done")

        self.__sender_name = sender_name
        self.__instance_id = instance_id
        self.__strategy_id = strategy_id

    def init_subscribe(self
                       , sub_host: str
                       , sub_port: str
                       , timeout_ms: int = 100):
        ctx = zmq.Context.instance()
        self.__subscriber = ctx.socket(zmq.SUB)
        subscriber_url = f"tcp://{sub_host}:{sub_port}"
        self.__logger.info(f"subscriber_url: {subscriber_url}")
        self.__subscriber.connect(subscriber_url)
        self.__logger.info("socket connect done")

        self.__sub_timeout_ms = timeout_ms

    def set_max_send_limit(self, max_limit: int) -> None:
        with self.__pub_mutex:
            self.__max_byte_limit = max_limit

    def reset_sent_byte(self) -> None:
        with self.__pub_mutex:
            self.__cur_byte_sent = 0

    def get_cur_sent_byte(self) -> int:
        with self.__pub_mutex:
            return self.__cur_byte_sent

    def reg_sub_topic(self, topic: str):
        self.__logger.info(f"Subscribe topic: {topic}")
        self.__subscriber.setsockopt(zmq.SUBSCRIBE, str.encode(topic))

    def start_subscription(self, mode: str = "simple"):
        with self.__sub_mutex:
            self.__is_subscription_run = True
            if mode == "simple":
                self.__sub_main_thread = threading.Thread(target=self.sub_main_simple)
            elif mode == "smart":
                self.__sub_main_thread = threading.Thread(target=self.sub_main_smart)
            else:
                self.__sub_main_thread = threading.Thread(target=self.sub_main_smart)
            self.__sub_main_thread.start()

            signal.signal(signal.SIGINT, self.__cleanup)

    def stop_subscription(self):
        with self.__sub_mutex:
            self.__is_subscription_run = False

        self.__sub_main_thread.join()

    def reg_callback(self, cb_fun):
        with self.__sub_mutex:
            self.__cb_fun = cb_fun

    def unreg_callback(self):
        with self.__sub_mutex:
            self.__cb_fun = None

    def send_cop(self, msg_id: str, msg_type: ts_cop_pb2.Cop.MsgType, topic: str, cop: ts_cop_pb2.Cop):
        cop.msg_id = msg_id
        cop.msg_type = msg_type
        cop.sender = self.__sender_name
        cop.instance_id = self.__instance_id
        cop.strategy_id = self.__strategy_id
        with self.__pub_mutex:
            cop.seq_num = self.__seq_num
            if self.__is_limit_sending and not self.__is_can_send(cop_size=cop.ByteSize()
                                                                  , max_byte=self.__max_byte_limit
                                                                  , cur_byte=self.__cur_byte_sent
                                                                  , is_send_alert=self.__is_send_limit_alert):
                return
            self.__cur_byte_sent += cop.ByteSize()

            self.__seq_num += 1
            self.__publisher.send_multipart([str.encode(topic), cop.SerializeToString()])

    def send_cop_list(self
                      , msg_id: str
                      , msg_type: ts_cop_pb2.Cop.MsgType
                      , fid_nums: List[int]
                      , fid_values: List[Any]
                      , topic: str
                      , timestamp: float) -> None:
        cop = ts_cop_pb2.Cop()
        cop.msg_id = msg_id
        cop.msg_type = msg_type
        cop.sender = self.__sender_name
        cop.instance_id = self.__instance_id
        cop.strategy_id = self.__strategy_id

        # put data into cop
        for fid_num, fid_value in zip(fid_nums, fid_values):
            if 50001 <= fid_num and fid_num <= 60000:
                if fid_num not in self.__put_value_2_cop_map:
                    continue
                self.__put_value_2_cop_map[fid_num](cop=cop, fid_num=fid_num, fid_value=fid_value)
            else:
                num = ct.get_fid_group_num(fid_num=fid_num)
                if num not in self.__process_fid_map_smart:
                    continue
                self.__put_value_2_cop_map[num](cop=cop, fid_num=fid_num, fid_value=fid_value, timestamp=timestamp)

        with self.__pub_mutex:
            cop.seq_num = self.__seq_num
            if self.__is_limit_sending and not self.__is_can_send(cop_size=cop.ByteSize()
                                                                  , max_byte=self.__max_byte_limit
                                                                  , cur_byte=self.__cur_byte_sent
                                                                  , is_send_alert=self.__is_send_limit_alert):
                return
            self.__cur_byte_sent += cop.ByteSize()

            self.__seq_num += 1
            self.__publisher.send_multipart([str.encode(topic), cop.SerializeToString()])

    def reset_msg_seq_num(self):
        with self.__pub_mutex:
            self.__seq_num = 0

    def sub_main_smart(self):
        self.__logger.info("Start")

        poller = zmq.Poller()
        poller.register(self.__subscriber, zmq.POLLIN)
        while self.__is_subscription():
            sockets = dict(poller.poll(self.__sub_timeout_ms))

            if not self.__is_subscription():
                break

            # get and process data
            if self.__subscriber in sockets:
                topic_encoded, data = self.__subscriber.recv_multipart()

                with self.__sub_mutex:
                    if self.__cb_fun is not None:
                        cop = ts_cop_pb2.Cop()
                        cop.ParseFromString(data)
                        topic = topic_encoded.decode("utf-8")

                        # tsdata
                        for fid_num, fid_value in cop.data_map.items():
                            if 50001 <= fid_num and fid_num <= 60000:
                                if fid_num not in self.__process_fid_map_smart:
                                    continue
                                self.__process_fid_map_smart[fid_num](topic=topic, cop=cop, fid_num=fid_num, fid_value=fid_value)
                            else:
                                num = ct.get_fid_group_num(fid_num=fid_num)
                                if num not in self.__process_fid_map_smart:
                                    continue
                                self.__process_fid_map_smart[num](topic=topic, cop=cop, fid_num=fid_num, fid_value=fid_value)

        self.__logger.info("End")

    def sub_main_extract(self):
        self.__logger.info("Start")

        poller = zmq.Poller()
        poller.register(self.__subscriber, zmq.POLLIN)
        while self.__is_subscription():
            sockets = dict(poller.poll(self.__sub_timeout_ms))

            if not self.__is_subscription():
                break

            # get and process data
            if self.__subscriber in sockets:
                topic_encoded, data = self.__subscriber.recv_multipart()

                with self.__sub_mutex:
                    if self.__cb_fun is not None:
                        cop = ts_cop_pb2.Cop()
                        cop.ParseFromString(data)
                        topic = topic_encoded.decode("utf-8")
                        # int32
                        for fid_num, fid_value in cop.int32_map.items():
                            self.__cb_fun(topic=topic, cop=cop, fid_num=fid_num, fid_value=fid_value)
                        # int64
                        for fid_num, fid_value in cop.int64_map.items():
                            self.__cb_fun(topic=topic, cop=cop, fid_num=fid_num, fid_value=fid_value)
                        # float
                        for fid_num, fid_value in cop.float_map.items():
                            self.__cb_fun(topic=topic, cop=cop, fid_num=fid_num, fid_value=fid_value)
                        # double
                        for fid_num, fid_value in cop.double_map.items():
                            self.__cb_fun(topic=topic, cop=cop, fid_num=fid_num, fid_value=fid_value)
                        # string
                        for fid_num, fid_value in cop.string_map.items():
                            self.__cb_fun(topic=topic, cop=cop, fid_num=fid_num, fid_value=fid_value)
                        # bool
                        for fid_num, fid_value in cop.bool_map.items():
                            self.__cb_fun(topic=topic, cop=cop, fid_num=fid_num, fid_value=fid_value)
                        # order
                        for fid_num, fid_value in cop.order_map.items():
                            self.__cb_fun(topic=topic, cop=cop, fid_num=fid_num, fid_value=fid_value)
                        # trade
                        for fid_num, fid_value in cop.trade_map.items():
                            self.__cb_fun(topic=topic, cop=cop, fid_num=fid_num, fid_value=fid_value)
                        # si
                        for fid_num, fid_value in cop.si_map.items():
                            self.__cb_fun(topic=topic, cop=cop, fid_num=fid_num, fid_value=fid_value)
                        # ci
                        for fid_num, fid_value in cop.ci_map.items():
                            self.__cb_fun(topic=topic, cop=cop, fid_num=fid_num, fid_value=fid_value)

        self.__logger.info("End")

    def sub_main_simple(self):
        self.__logger.info("Start")

        poller = zmq.Poller()
        poller.register(self.__subscriber, zmq.POLLIN)
        while self.__is_subscription():
            sockets = dict(poller.poll(self.__sub_timeout_ms))

            if not self.__is_subscription():
                break

            # get and process data
            if self.__subscriber in sockets:
                topic, data = self.__subscriber.recv_multipart()

                with self.__sub_mutex:
                    if self.__cb_fun is not None:
                        cop = ts_cop_pb2.Cop()
                        cop.ParseFromString(data)
                        self.__cb_fun(topic.decode("utf-8"), cop)

            if not self.__is_subscription():
                break

        self.__logger.info("End")

    def __process_int32(self, topic: str, cop: ts_cop_pb2.Cop, fid_num: int, fid_value: Any):
        self.__cb_fun(topic=topic, cop=cop, fid_num=fid_num, fid_value=fid_value.int32_data)

    def __process_int64(self, topic: str, cop: ts_cop_pb2.Cop, fid_num: int, fid_value: Any):
        self.__cb_fun(topic=topic, cop=cop, fid_num=fid_num, fid_value=fid_value.int64_data)

    def __process_float(self, topic: str, cop: ts_cop_pb2.Cop, fid_num: int, fid_value: Any):
        self.__cb_fun(topic=topic, cop=cop, fid_num=fid_num, fid_value=fid_value.float_data)

    def __process_double(self, topic: str, cop: ts_cop_pb2.Cop, fid_num: int, fid_value: Any):
        self.__cb_fun(topic=topic, cop=cop, fid_num=fid_num, fid_value=fid_value.double_data)

    def __process_string(self, topic: str, cop: ts_cop_pb2.Cop, fid_num: int, fid_value: Any):
        self.__cb_fun(topic=topic, cop=cop, fid_num=fid_num, fid_value=fid_value.string_data)

    def __process_bool(self, topic: str, cop: ts_cop_pb2.Cop, fid_num: int, fid_value: Any):
        self.__cb_fun(topic=topic, cop=cop, fid_num=fid_num, fid_value=fid_value.bool_data)

    def __process_d_int32(self, topic: str, cop: ts_cop_pb2.Cop, fid_num: int, fid_value: Any):
        self.__cb_fun(topic=topic, cop=cop, fid_num=fid_num, fid_value=fid_value)

    def __process_d_int64(self, topic: str, cop: ts_cop_pb2.Cop, fid_num: int, fid_value: Any):
        self.__cb_fun(topic=topic, cop=cop, fid_num=fid_num, fid_value=fid_value)

    def __process_d_float(self, topic: str, cop: ts_cop_pb2.Cop, fid_num: int, fid_value: Any):
        self.__cb_fun(topic=topic, cop=cop, fid_num=fid_num, fid_value=fid_value)

    def __process_d_double(self, topic: str, cop: ts_cop_pb2.Cop, fid_num: int, fid_value: Any):
        self.__cb_fun(topic=topic, cop=cop, fid_num=fid_num, fid_value=fid_value)

    def __process_d_string(self, topic: str, cop: ts_cop_pb2.Cop, fid_num: int, fid_value: Any):
        self.__cb_fun(topic=topic, cop=cop, fid_num=fid_num, fid_value=fid_value)

    def __process_d_bool(self, topic: str, cop: ts_cop_pb2.Cop, fid_num: int, fid_value: Any):
        self.__cb_fun(topic=topic, cop=cop, fid_num=fid_num, fid_value=fid_value)

    def __process_ci(self, topic: str, cop: ts_cop_pb2.Cop, fid_num: int, fid_value: Any):
        self.__cb_fun(topic=topic, cop=cop, fid_num=fid_num, fid_value=fid_value)

    def __process_si(self, topic: str, cop: ts_cop_pb2.Cop, fid_num: int, fid_value: Any):
        self.__cb_fun(topic=topic, cop=cop, fid_num=fid_num, fid_value=fid_value)

    def __process_order(self, topic: str, cop: ts_cop_pb2.Cop, fid_num: int, fid_value: Any):
        self.__cb_fun(topic=topic, cop=cop, fid_num=fid_num, fid_value=fid_value)

    def __process_trade(self, topic: str, cop: ts_cop_pb2.Cop, fid_num: int, fid_value: Any):
        self.__cb_fun(topic=topic, cop=cop, fid_num=fid_num, fid_value=fid_value)

    def __process_ci_smart(self, topic: str, cop: ts_cop_pb2.Cop, fid_num: int, fid_value: Any):
        self.__cb_fun(topic=topic, cop=cop, fid_num=fid_num, fid_value=fid_value.ci_data)

    def __process_si_smart(self, topic: str, cop: ts_cop_pb2.Cop, fid_num: int, fid_value: Any):
        self.__cb_fun(topic=topic, cop=cop, fid_num=fid_num, fid_value=fid_value.si_data)

    def __process_order_smart(self, topic: str, cop: ts_cop_pb2.Cop, fid_num: int, fid_value: Any):
        self.__cb_fun(topic=topic, cop=cop, fid_num=fid_num, fid_value=fid_value.order_data)

    def __process_trade_smart(self, topic: str, cop: ts_cop_pb2.Cop, fid_num: int, fid_value: Any):
        self.__cb_fun(topic=topic, cop=cop, fid_num=fid_num, fid_value=fid_value.trade_data)

    def __cleanup(self, signum, frame):
        self.stop_subscription()
        exit(0)

    def __is_subscription(self):
        with self.__sub_mutex:
            return self.__is_subscription_run

    def __is_can_send(self, cop_size: int, max_byte: int, cur_byte: int, is_send_alert: bool) -> bool:
        if cur_byte + cop_size > max_byte:
            if is_send_alert:
                self.__logger.error(f"Cannot send cop due to size limit. sent: {cur_byte} max_byte: {max_byte} cop_size: {cop_size}")
                is_send_alert = False
                return False
            else:
                return False
        else:
            return True

    def __put_value_d_int32(self, cop: ts_cop_pb2.Cop, fid_num: int, fid_value: int, timestamp: float):
        cop.data_map[fid_num].d_int32_data.time = timestamp
        cop.data_map[fid_num].d_int32_data.value = fid_value

    def __put_value_d_int64(self, cop: ts_cop_pb2.Cop, fid_num: int, fid_value: int, timestamp: float):
        cop.data_map[fid_num].d_int64_data.time = timestamp
        cop.data_map[fid_num].d_int64_data.value = fid_value

    def __put_value_d_float(self, cop: ts_cop_pb2.Cop, fid_num: int, fid_value: float, timestamp: float):
        cop.data_map[fid_num].d_float_data.time = timestamp
        cop.data_map[fid_num].d_float_data.value = fid_value

    def __put_value_d_double(self, cop: ts_cop_pb2.Cop, fid_num: int, fid_value: float, timestamp: float):
        cop.data_map[fid_num].d_double_data.time = timestamp
        cop.data_map[fid_num].d_double_data.value = fid_value

    def __put_value_d_string(self, cop: ts_cop_pb2.Cop, fid_num: int, fid_value: str, timestamp: float):
        cop.data_map[fid_num].d_string_data.time = timestamp
        cop.data_map[fid_num].d_string_data.value = fid_value

    def __put_value_d_bool(self, cop: ts_cop_pb2.Cop, fid_num: int, fid_value: Any, timestamp: float):
        cop.data_map[fid_num].d_bool_data.time = timestamp
        cop.data_map[fid_num].d_bool_data.value = fid_value

    def __put_value_ci(self, cop: ts_cop_pb2.Cop, fid_num: int, fid_value: List[Dict[Any, Any]]):
        for ci in fid_value: # ci_list:
            cop.data_map[fid_num].ci_data.ci_list.append(ts_cop_pb2.CI(value=json.dumps(ci)))

    def __put_value_si(self, cop: ts_cop_pb2.Cop, fid_num: int, fid_value: List[ts_cop_pb2.SI]):
        for si in fid_value: # si_list:
            cop.data_map[fid_num].si_data.si_list.append(si)

    def __put_value_order(self, cop: ts_cop_pb2.Cop, fid_num: int, fid_value: List[ts_cop_pb2.TSOrder]):
        for order in fid_value: # order_list:
            cop.data_map[fid_num].order_data.order_list.append(order)

    def __put_value_trade(self, cop: ts_cop_pb2.Cop, fid_num: int, fid_value: List[ts_cop_pb2.TSTrade]):
        for trd in fid_value: # trade_list:
            cop.data_map[fid_num].trade_data.trade_list.append(trd)
