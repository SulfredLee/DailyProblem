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
        self.live_mode: bool = False
        self.qc_strategy_id: str = ""

    def __eq__(self, other) -> bool:
        if isinstance(other, StrategyInsight):
            return self.symbol == other.symbol\
                and self.ratio == other.ratio
        else:
            return False

    def __str__(self):
        return f"{self.symbol},{self.ratio}"

class TS_Order(object):
    def __init__(self):
        self.symbol: str = ""
        self.symbol_id: str = ""
        self.quantity: float = 0
        self.fill_quantity: float = 0
        self.parent_id: str = ""
        self.order_id: str = ""
        self.qc_order_id: int = 0
        self.created: datetime = None
        self.last_update: datetime = None
        self.strategy_name: str = ""
        self.live_mode: bool = False
        self.qc_strategy_id: str = ""
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
            return self.order_id == other.order_id\
                and self.qc_order_id == other.qc_order_id
        else:
            return False

    def __str__(self):
        return f"{self.symbol},{self.quantity}"

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
        self.live_mode: bool = False
        self.qc_strategy_id: str = ""
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
        if isinstance(other, TS_Order):
            return self.order_id == other.order_id\
                and self.qc_order_id == other.qc_order_id
        else:
            return False

    def __str__(self):
        return f"{self.symbol},{self.quantity}"
