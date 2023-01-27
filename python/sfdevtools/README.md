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
