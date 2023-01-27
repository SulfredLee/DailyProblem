import logging
from sfdevtools.observability.logging_json import JSONFormatter
from sfdevtools.observability.logstash.handler_tcp import TCPLogstashHandler
from sfdevtools.observability.logstash.handler_udp import UDPLogstashHandler, LogstashHandler
from logging.handlers import TimedRotatingFileHandler

def init_logger(logger_name: str = "default_logger"
                , log_level: int = logging.DEBUG
                , is_print_to_file: bool = False
                , log_file_root: str = "./"
                , is_print_to_console: bool = True
                , is_json_output: bool = True
                , is_print_to_logstash: bool = False
                , logstash_host: str = None
                , logstash_port: int = None
                , logstash_user_tags: list = None) -> logging.Logger:
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)

    formatter = logging.Formatter('%(asctime)s [%(levelname)s] [%(name)s] [%(filename)s:%(funcName)s:%(lineno)d] [%(threadName)s:%(process)d] %(message)s')
    if is_json_output:
        formatter = JSONFormatter(fields={
            "log_time": "asctime"
            , "level_name": "levelname"
            , "logger_name": "name"
            , "file_name": "filename"
            , "func_name": "funcName"
            , "line_no": "lineno"
            , "thread_name": "threadName"
            , "process_name": "process"
           })

    if is_print_to_file:
        fh = TimedRotatingFileHandler(f"{log_file_root}/{logger_name}.log"
                                      , when='h'
                                      , interval=1
                                      , backupCount=0
                                      , encoding=None
                                      , delay=False
                                      , utc=True
                                      )
        fh.setLevel(log_level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    if is_print_to_console:
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    if is_print_to_logstash:
        logger.addHandler(TCPLogstashHandler(logstash_host, logstash_port, tags=logstash_user_tags, version=1))

    return logger

