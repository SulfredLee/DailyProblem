import logging
import zmq
import threading
import signal

import sfdevtools.grpc_protos.ts_cop_pb2 as ts_cop_pb2
import sfdevtools.grpc_protos.ts_cop_pb2_grpc as ts_cop_pb2_grpc

class TSDataCtrl(object):
    def __init__(self):
        self.__logger: logging.Logger = None
        self.__pub_mutex: threading.Lock = threading.Lock()
        self.__sub_mutex: threading.Lock = threading.Lock()
        self.__publisher: zmq.sugar.socket.Socket = None
        self.__subscriber: zmq.sugar.socket.Socket = None
        self.__sender_name: str = ""
        self.__instance_id: int = 0
        self.__seq_num: int = 0
        self.__cb_fun = None
        self.__sub_main_thread: threading.Thread = None
        self.__is_subscription_run: bool = False
        self.__sub_timeout_ms: int = 100

    def init_component(self
                       , logger: logging.Logger):
        self.__logger = logger

    def init_publish(self
                     , pub_host: str
                     , pub_port: str
                     , sender_name: str
                     , instance_id: int):
        ctx = zmq.Context.instance()
        self.__publisher = ctx.socket(zmq.PUB)
        publisher_url = f"tcp://{pub_host}:{pub_port}"
        self.__logger.info(f"publisher_url: {publisher_url}")
        self.__publisher.connect(publisher_url)
        self.__logger.info("socket connect done")

        self.__sender_name = sender_name
        self.__instance_id = instance_id

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

    def reg_sub_topic(self, topic: str):
        self.__logger.info(f"Subscribe topic: {topic}")
        self.__subscriber.setsockopt(zmq.SUBSCRIBE, str.encode(topic))

    def start_subscription(self, mode: str = "simple"):
        with self.__sub_mutex:
            self.__is_subscription_run = True
            if mode == "simple":
                self.__sub_main_thread = threading.Thread(target=self.sub_main_simple)
            else:
                self.__sub_main_thread = threading.Thread(target=self.sub_main_extract)
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
        with self.__pub_mutex:
            cop.msg_id = msg_id
            cop.msg_type = msg_type
            cop.sender = self.__sender_name
            cop.instance_id = self.__instance_id
            cop.seq_num = self.__seq_num
            self.__seq_num += 1
            self.__publisher.send_multipart([str.encode(topic), cop.SerializeToString()])

    def reset_msg_seq_num(self):
        with self.__pub_mutex:
            self.__seq_num = 0

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

    def __cleanup(self, signum, frame):
        self.stop_subscription()
        exit(0)

    def __is_subscription(self):
        with self.__sub_mutex:
            return self.__is_subscription_run
