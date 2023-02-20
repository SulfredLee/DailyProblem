import datetime

import sfdevtools.grpc_protos.ts_cop_pb2 as ts_cop_pb2
import sfdevtools.grpc_protos.ts_cop_pb2_grpc as ts_cop_pb2_grpc
from sfdevtools.data_cache.DComponents import StrategyInsight, TS_Order, TS_Trade

def conv_TS_Order_2_cop_order(order: TS_Order) -> ts_cop_pb2.TSOrder:
    ord_ele = ts_cop_pb2.TSOrder()

    ord_ele.symbol = order.symbol
    ord_ele.symbol_id = order.symbol_id
    ord_ele.quantity = order.quantity
    ord_ele.fill_quantity = order.fill_quantity
    ord_ele.parent_id = order.parent_id
    ord_ele.order_id = order.order_id
    ord_ele.qc_order_id = order.qc_order_id
    ord_ele.created = int(order.created.timestamp())
    ord_ele.last_update = int(order.last_update.timestamp())
    ord_ele.strategy_name = order.strategy_name
    ord_ele.live_mode = order.live_mode
    ord_ele.qc_strategy_id = order.qc_strategy_id
    ord_ele.order_status = order.order_status
    ord_ele.execution_broker = order.execution_broker
    ord_ele.clearing_broker = order.clearing_broker
    ord_ele.account = order.account
    ord_ele.price = order.price
    ord_ele.fee = order.fee
    ord_ele.fee_ccy = order.fee_ccy
    ord_ele.exchange = order.exchange
    ord_ele.ccy = order.ccy

    return ord_ele

def conv_TS_Trade_2_cop_trade(trd: TS_Trade) -> ts_cop_pb2.TSTrade:
    trd_ele = ts_cop_pb2.TSTrade()

    trd_ele.symbol = trd.symbol
    trd_ele.symbol_id = trd.symbol_id
    trd_ele.quantity = trd.quantity
    trd_ele.parent_id = trd.parent_id
    trd_ele.trade_id = trd.trade_id
    trd_ele.created = int(trd.created.timestamp())
    trd_ele.last_update = int(trd.last_update.timestamp())
    trd_ele.strategy_name = trd.strategy_name
    trd_ele.live_mode = trd.live_mode
    trd_ele.qc_strategy_id = trd.qc_strategy_id
    trd_ele.trade_status = trd.trade_status
    trd_ele.execution_broker = trd.execution_broker
    trd_ele.clearing_broker = trd.clearing_broker
    # trd_ele.settlement_date = trd.settlement_date # we don't have information from QC for now
    trd_ele.fx_ratio = trd.fx_ratio
    trd_ele.account = trd.account
    trd_ele.price = trd.price
    trd_ele.fee = trd.fee
    trd_ele.fee_ccy = trd.fee_ccy
    trd_ele.exchange = trd.exchange
    trd_ele.ccy = trd.ccy

    return trd_ele

def conv_SI_2_cop_si(si: StrategyInsight) -> ts_cop_pb2.SI:
    si_ele = ts_cop_pb2.SI()

    si_ele.symbol = si.symbol
    si_ele.symbol_id = si.symbol_id
    si_ele.ratio = si.ratio
    si_ele.parent_id = si.parent_id
    si_ele.si_id = si.si_id
    si_ele.created = int(si.created.timestamp())
    si_ele.last_update = int(si.last_update.timestamp())
    si_ele.strategy_name = si.strategy_name
    si_ele.live_mode = si.live_mode
    si_ele.qc_strategy_id = si.qc_strategy_id

    return si_ele

def conv_cop_order_2_TS_Order(ord_ele: ts_cop_pb2.TSOrder) -> TS_Order:
    order = TS_Order()

    order.symbol = ord_ele.symbol
    order.symbol_id = ord_ele.symbol_id
    order.quantity = ord_ele.quantity
    order.fill_quantity = ord_ele.fill_quantity
    order.parent_id = ord_ele.parent_id
    order.order_id = ord_ele.order_id
    order.qc_order_id = ord_ele.qc_order_id
    order.created = datetime.datetime.fromtimestamp(ord_ele.created)
    order.last_update = datetime.datetime.fromtimestamp(ord_ele.last_update)
    order.strategy_name = ord_ele.strategy_name
    order.live_mode = ord_ele.live_mode
    order.qc_strategy_id = ord_ele.qc_strategy_id
    order.order_status = ord_ele.order_status
    order.execution_broker = ord_ele.execution_broker
    order.clearing_broker = ord_ele.clearing_broker
    order.account = ord_ele.account
    order.price = ord_ele.price
    order.fee = ord_ele.fee
    order.fee_ccy = ord_ele.fee_ccy
    order.exchange = ord_ele.exchange
    order.ccy = ord_ele.ccy

    return order

def conv_cop_trade_2_TS_Trade(trd_ele: ts_cop_pb2.TSTrade) -> TS_Trade:
    trd = TS_Trade()

    trd.symbol = trd_ele.symbol
    trd.symbol_id = trd_ele.symbol_id
    trd.quantity = trd_ele.quantity
    trd.parent_id = trd_ele.parent_id
    trd.trade_id = trd_ele.trade_id
    trd.created = datetime.datetime.fromtimestamp(trd_ele.created)
    trd.last_update = datetime.datetime.fromtimestamp(trd_ele.last_update)
    trd.strategy_name = trd_ele.strategy_name
    trd.live_mode = trd_ele.live_mode
    trd.qc_strategy_id = trd_ele.qc_strategy_id
    trd.trade_status = trd_ele.trade_status
    trd.execution_broker = trd_ele.execution_broker
    trd.clearing_broker = trd_ele.clearing_broker
    trd.fx_ratio = trd_ele.fx_ratio
    trd.account = trd_ele.account
    trd.price = trd_ele.price
    trd.fee = trd_ele.fee
    trd.fee_ccy = trd_ele.fee_ccy
    trd.exchange = trd_ele.exchange
    trd.ccy = trd_ele.ccy

    return trd

def conv_cop_si_2_SI(si_ele: ts_cop_pb2.SI) -> StrategyInsight:
    si = StrategyInsight(symbol=si_ele.symbol, ratio=si_ele.ratio)

    si.symbol = si_ele.symbol
    si.symbol_id = si_ele.symbol_id
    si.ratio = si_ele.ratio
    si.parent_id = si_ele.parent_id
    si.si_id = si_ele.si_id
    si.created = datetime.datetime.fromtimestamp(si_ele.created / 1000)
    si.last_update = datetime.datetime.fromtimestamp(si_ele.last_update / 1000)
    si.strategy_name = si_ele.strategy_name
    si.live_mode = si_ele.live_mode
    si.qc_strategy_id = si_ele.qc_strategy_id

    return si
