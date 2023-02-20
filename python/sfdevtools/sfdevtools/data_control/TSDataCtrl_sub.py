import logging
import os
import time

import sfdevtools.observability.log_helper as lh
import sfdevtools.data_control.TSDataCtrl as TSDataCtrl
import sfdevtools.grpc_protos.ts_cop_pb2 as ts_cop_pb2
import sfdevtools.grpc_protos.ts_cop_pb2_grpc as ts_cop_pb2_grpc


def test_cb(topic: str, cop: ts_cop_pb2.Cop):
    logger: logging.Logger = lh.init_logger(logger_name="TSDataCtrl_sub_logger", is_json_output=False)

    logger.info(f"topic: {topic} cop: {cop}")

def main():
    logger: logging.Logger = lh.init_logger(logger_name="TSDataCtrl_sub_logger", is_json_output=False)
    env_v = {"proxy_host": os.getenv("P_HOST", default="0.0.0.0")
             , "proxy_in_port": os.getenv("P_IN_PORT", default="5557")
             , "proxy_out_port": os.getenv("P_OUT_PORT", default="5558")}
    logger.info(env_v)

    data_ctrl: TSDataCtrl = TSDataCtrl.TSDataCtrl()
    data_ctrl.init_component(logger=logger)
    data_ctrl.init_subscribe(sub_host=env_v["proxy_host"]
                             , sub_port=env_v["proxy_out_port"])
    data_ctrl.reg_sub_topic("RSA_True")
    data_ctrl.reg_callback(cb_fun=test_cb)
    data_ctrl.start_subscription()

    num_count = 0
    while True:
        time.sleep(1)

    data_ctrl.stop_subscription()
    data_ctrl.reg_callback(cb_fun=None)

if __name__ == '__main__':
    main()
