import copy
import datetime

def to_timestamp_safe(value) -> float:
    if isinstance(value, datetime.datetime):
        return value.timestamp()
    else:
        return value

class StrategyInsight(object):
    def __init__(self, symbol: str, ratio: float):
        self.symbol: str = symbol
        self.symbol_id: str = ""
        self.ratio: float = ratio
        self.parent_id: str = ""
        self.si_id: str = ""
        self.created: datetime = None
        self.last_update: datetime = None
        self.strategy_name: str = ""
        self.parent_strategy_name: str = ""
        self.live_mode: bool = False
        self.strategy_id: str = ""

    def __eq__(self, other) -> bool:
        if isinstance(other, StrategyInsight):
            return self.symbol == other.symbol\
                and self.symbol_id == other.symbol_id\
                and self.ratio == other.ratio\
                and self.parent_id == other.parent_id\
                and self.si_id == other.si_id\
                and self.created == other.created\
                and self.last_update == other.last_update\
                and self.strategy_name == other.strategy_name\
                and self.parent_strategy_name == other.parent_strategy_name\
                and self.live_mode == other.live_mode\
                and self.strategy_id == other.strategy_id
        else:
            return False

    def __str__(self):
        return f"{self.symbol},{self.ratio}"

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        special_fields = set(["created", "last_update"])
        for k, v in self.__dict__.items():
            if k in special_fields:
                setattr(result, k, datetime.datetime.fromtimestamp(to_timestamp_safe(v)))
            else:
                setattr(result, k, copy.deepcopy(v, memo))

        return result

class TS_Order(object):
    def __init__(self):
        self.symbol: str = ""
        self.symbol_id: str = ""
        self.quantity: float = 0
        self.fill_quantity: float = 0
        self.parent_id: str = ""
        self.order_id: str = ""
        self.platform_order_id: int = 0
        self.created: datetime = None
        self.last_update: datetime = None
        self.strategy_name: str = ""
        self.parent_strategy_name: str = ""
        self.live_mode: bool = False
        self.strategy_id: str = ""
        # https://github.com/QuantConnect/Lean/blob/master/Common/Orders/OrderTypes.cs#L107
        self.order_status: str = ""
        self.execution_broker: str = ""
        self.clearing_broker: str = ""
        self.account: str = ""
        self.price: float = 0
        self.fee: float = 0
        self.fee_ccy: str = ""
        self.exchange: str = ""
        self.ccy: str = ""

    def __eq__(self, other) -> bool:
        if isinstance(other, TS_Order):
            return self.symbol == other.symbol\
                and self.symbol_id == other.symbol_id\
                and self.quantity == other.quantity\
                and self.fill_quantity == other.fill_quantity\
                and self.parent_id == other.parent_id\
                and self.order_id == other.order_id\
                and self.platform_order_id == other.platform_order_id\
                and self.created == other.created\
                and self.last_update == other.last_update\
                and self.strategy_name == other.strategy_name\
                and self.parent_strategy_name == other.parent_strategy_name\
                and self.live_mode == other.live_mode\
                and self.strategy_id == other.strategy_id\
                and self.order_status == other.order_status\
                and self.execution_broker == other.execution_broker\
                and self.clearing_broker == other.clearing_broker\
                and self.account == other.account\
                and self.price == other.price\
                and self.fee == other.fee\
                and self.fee_ccy == other.fee_ccy\
                and self.exchange == other.exchange\
                and self.ccy == other.ccy
        else:
            return False

    def __str__(self):
        return f"{self.symbol},{self.quantity},{self.fill_quantity}"

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        special_fields = set(["created", "last_update"])
        for k, v in self.__dict__.items():
            if k in special_fields:
                setattr(result, k, datetime.datetime.fromtimestamp(to_timestamp_safe(v)))
            else:
                setattr(result, k, copy.deepcopy(v, memo))

        return result

class TS_Trade(object):
    def __init__(self):
        self.symbol: str = ""
        self.symbol_id: str = ""
        self.quantity: float = 0
        self.parent_id: str = ""
        self.trade_id: str = ""
        self.created: datetime = None
        self.last_update: datetime = None
        self.strategy_name: str = ""
        self.parent_strategy_name: str = ""
        self.live_mode: bool = False
        self.strategy_id: str = ""
        # https://github.com/QuantConnect/Lean/blob/master/Common/Orders/OrderTypes.cs#L107
        self.trade_status: str = ""
        self.execution_broker: str = ""
        self.clearing_broker: str = ""
        self.settlement_date: datetime = None
        self.fx_ratio: float = 0
        self.account: str = ""
        self.price: float = 0
        self.fee: float = 0
        self.fee_ccy: str = ""
        self.exchange: str = ""
        self.ccy: str = ""

    def __eq__(self, other) -> bool:
        if isinstance(other, TS_Trade):
            return self.symbol == other.symbol\
                and self.symbol_id == other.symbol_id\
                and self.quantity == other.quantity\
                and self.parent_id == other.parent_id\
                and self.trade_id == other.trade_id\
                and self.created == other.created\
                and self.last_update == other.last_update\
                and self.strategy_name == other.strategy_name\
                and self.parent_strategy_name == other.parent_strategy_name\
                and self.live_mode == other.live_mode\
                and self.strategy_id == other.strategy_id\
                and self.trade_status == other.trade_status\
                and self.execution_broker == other.execution_broker\
                and self.clearing_broker == other.clearing_broker\
                and self.settlement_date == other.settlement_date\
                and self.fx_ratio == other.fx_ratio\
                and self.account == other.account\
                and self.price == other.price\
                and self.fee == other.fee\
                and self.fee_ccy == other.fee_ccy\
                and self.exchange == other.exchange\
                and self.ccy == other.ccy
        else:
            return False

    def __str__(self):
        return f"{self.symbol},{self.quantity}"

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        special_fields = set(["created", "last_update", "settlement_date"])
        for k, v in self.__dict__.items():
            if k in special_fields:
                setattr(result, k, datetime.datetime.fromtimestamp(to_timestamp_safe(v)))
            else:
                setattr(result, k, copy.deepcopy(v, memo))

        return result
