## How to publish to pypi
```bash
# set up pypi token
poetry config pypi-token.pypi my-token

# build the project
poetry build

# publish the project
poetry publish

# DONE
```

## Generate source code from protobuf
```bash
$ poetry add grpcio-tools
$ poetry add grpcio
$ cd sfdevtools/
$ poetry run python -m grpc_tools.protoc -I ./grpc_protos --python_out=./grpc_protos/ --grpc_python_out=./grpc_protos/ ./grpc_protos/peacock.proto
```

## Demo example
### Double check lock for singleton
```python
import sfdevtools.observability.log_helper as lh
import logging
logger = lh.init_logger(logger_name="sfdevtools_logger", is_json_output=False)
# create class X
class X(SDC):
    pass

# create class Y
class Y(SDC):
    pass

A1, A2 = X.instance(), X.instance()
B1, B2 = Y.instance(), Y.instance()

assert A1 is not B1
assert A1 is A2
assert B1 is B2

logger.info('A1 : {}'.format(A1))
logger.info('A2 : {}'.format(A2))
logger.info('B1 : {}'.format(B1))
logger.info('B2 : {}'.format(B2))
```

### Send log to logstash
```python
logger = lh.init_logger(logger_name="connection_tester_logger"
                        , is_json_output=False
                        , is_print_to_console=True
                        , is_print_to_logstash=True
                        , logstash_host="<the host name>"
                        , logstash_port=5960
                        , logstash_user_tags=["Test001", "Test002"])
logger.info("Test Message from test")
logger.error("Test Message from test")
logger.warning("Test Message from test")
```

### Simple function pool
```python
import sfdevtools.observability.log_helper as lh
import sfdevtools.devTools.FuncFifoQ as FuncFifoQ
from functools import partial
from time import sleep

logger = lh.init_logger(logger_name="test_func_fifo_q", is_print_to_console=True, is_json_output=False)
func_q: FuncFifoQ.FuncFifoQ = FuncFifoQ.FuncFifoQ(logger=logger, pool_size=10)
func_q.start_q()
for i in range(10):
    func_q.push_func(partial(self.__func_test_foo, i, "hi"))

logger.info("Before sleep")
sleep(2)
logger.info("After sleep")

func_q.stop_q()
```

Expected output:
```bash
2023-02-13 13:50:48,565 [INFO] [test_func_fifo_q] [test_sfdevtools.py:test_func_fifo_q:144] [MainThread:92105] Before sleep
2023-02-13 13:50:48,565 [INFO] [test_func_fifo_q] [test_sfdevtools.py:__func_test_foo:151] [Thread-4:92105] Hi from thread: 0
2023-02-13 13:50:48,565 [INFO] [test_func_fifo_q] [test_sfdevtools.py:__func_test_foo:151] [Thread-8:92105] Hi from thread: 1
2023-02-13 13:50:48,565 [INFO] [test_func_fifo_q] [test_sfdevtools.py:__func_test_foo:151] [Thread-3:92105] Hi from thread: 2
2023-02-13 13:50:48,565 [INFO] [test_func_fifo_q] [test_sfdevtools.py:__func_test_foo:151] [Thread-2:92105] Hi from thread: 3
2023-02-13 13:50:48,565 [INFO] [test_func_fifo_q] [test_sfdevtools.py:__func_test_foo:151] [Thread-9:92105] Hi from thread: 4
2023-02-13 13:50:48,565 [INFO] [test_func_fifo_q] [test_sfdevtools.py:__func_test_foo:151] [Thread-5:92105] Hi from thread: 5
2023-02-13 13:50:48,565 [INFO] [test_func_fifo_q] [test_sfdevtools.py:__func_test_foo:151] [Thread-7:92105] Hi from thread: 6
2023-02-13 13:50:48,565 [INFO] [test_func_fifo_q] [test_sfdevtools.py:__func_test_foo:151] [Thread-10:92105] Hi from thread: 7
2023-02-13 13:50:48,565 [INFO] [test_func_fifo_q] [test_sfdevtools.py:__func_test_foo:151] [Thread-6:92105] Hi from thread: 8
2023-02-13 13:50:48,565 [INFO] [test_func_fifo_q] [test_sfdevtools.py:__func_test_foo:151] [Thread-1:92105] Hi from thread: 9
2023-02-13 13:50:50,565 [INFO] [test_func_fifo_q] [test_sfdevtools.py:test_func_fifo_q:146] [MainThread:92105] After sleep
2023-02-13 13:50:50,566 [INFO] [test_func_fifo_q] [FuncFifoQ.py:main:56] [Thread-7:92105] End
2023-02-13 13:50:50,566 [INFO] [test_func_fifo_q] [FuncFifoQ.py:main:56] [Thread-5:92105] End
2023-02-13 13:50:50,566 [INFO] [test_func_fifo_q] [FuncFifoQ.py:main:56] [Thread-4:92105] End
2023-02-13 13:50:50,566 [INFO] [test_func_fifo_q] [FuncFifoQ.py:main:56] [Thread-10:92105] End
2023-02-13 13:50:50,567 [INFO] [test_func_fifo_q] [FuncFifoQ.py:main:56] [Thread-1:92105] End
2023-02-13 13:50:50,567 [INFO] [test_func_fifo_q] [FuncFifoQ.py:main:56] [Thread-3:92105] End
2023-02-13 13:50:50,567 [INFO] [test_func_fifo_q] [FuncFifoQ.py:main:56] [Thread-8:92105] End
2023-02-13 13:50:50,568 [INFO] [test_func_fifo_q] [FuncFifoQ.py:main:56] [Thread-6:92105] End
2023-02-13 13:50:50,568 [INFO] [test_func_fifo_q] [FuncFifoQ.py:main:56] [Thread-2:92105] End
2023-02-13 13:50:50,568 [INFO] [test_func_fifo_q] [FuncFifoQ.py:main:56] [Thread-9:92105] End
```
