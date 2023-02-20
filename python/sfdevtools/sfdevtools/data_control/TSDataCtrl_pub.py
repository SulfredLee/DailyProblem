import logging
import os
import time

import sfdevtools.observability.log_helper as lh
import sfdevtools.data_control.TSDataCtrl as TSDataCtrl
import sfdevtools.grpc_protos.ts_cop_pb2 as ts_cop_pb2
import sfdevtools.grpc_protos.ts_cop_pb2_grpc as ts_cop_pb2_grpc

def main():
    logger: logging.Logger = lh.init_logger(logger_name="TSDataCtrl_pub_logger", is_json_output=False)
    env_v = {"proxy_host": os.getenv("P_HOST", default="0.0.0.0")
             , "proxy_in_port": os.getenv("P_IN_PORT", default="5557")
             , "proxy_out_port": os.getenv("P_OUT_PORT", default="5558")}
    logger.info(env_v)

    data_ctrl: TSDataCtrl = TSDataCtrl.TSDataCtrl()
    data_ctrl.init_component(logger=logger)
    data_ctrl.init_publish(pub_host=env_v["proxy_host"]
                           , pub_port=env_v["proxy_in_port"]
                           , sender_name="RSA_True"
                           , instance_id=1)

    num_count = 0
    while True:
        cop = ts_cop_pb2.Cop()
        cop.int32_map[1] = num_count
        num_count += 1
        logger.info(f"send cop: {cop}")
        data_ctrl.send_cop(topic="RSA_True", cop=cop)
        time.sleep(1)

if __name__ == '__main__':
    main()
