import datetime
import json

import sfdevtools.grpc_protos.ts_cop_pb2 as ts_cop_pb2
import sfdevtools.grpc_protos.ts_cop_pb2_grpc as ts_cop_pb2_grpc
from sfdevtools.data_cache.DComponents import StrategyInsight, TS_Order, TS_Trade
from sfdevtools.data_cache.DPage import DPage
from sfdevtools.data_cache.DStrategy import DStrategy

def to_timestamp_safe(value) -> float:
    if isinstance(value, datetime.datetime):
        return value.timestamp()
    else:
        return value

def conv_strg_2_cop(strgy: DStrategy) -> ts_cop_pb2.Cop:
    cop: ts_cop_pb2.Cop = ts_cop_pb2.Cop()

    data_list: List[Union[int, Any]] = strgy.get_fids()
    # handle normal fids
    for ele in data_list:
        fid_num = ele[0]
        value = ele[1]

        if fid_num <= 20000:
            if fid_num <= 10000:
                cop.int32_map[fid_num] = value
            else:
                cop.int64_map[fid_num] = value
        elif fid_num <=40000:
            if fid_num <= 30000:
                cop.float_map[fid_num] = value
            else:
                cop.double_map[fid_num] = value
        elif fid_num <= 50000:
            cop.string_map[fid_num] = value
        elif fid_num <= 70000:
            cop.bool_map[fid_num] = value

    # ci
    for ci in strgy.get_all_ci():
        ci["created"] = to_timestamp_safe(ci["created"])
        ci["last_update"] = to_timestamp_safe(ci["last_update"])
        cop.ci_map[ts_cop_pb2.FidNum.CI].ci_list.append(ts_cop_pb2.CI(value=json.dumps(ci)))
    # si
    for si in strgy.get_all_si():
        si_ele = dconv.conv_SI_2_cop_si(si=si)
        cop.si_map[ts_cop_pb2.Cop.FidNum.SI].si_list.append(si_ele)
    # order
    for order in strgy.get_orders():
        ord_ele = dconv.conv_TS_Order_2_cop_order(order=order)
        cop.order_map[ts_cop_pb2.Cop.FidNum.Order].order_list.append(ord_ele)
    # trade
    for trd in strgy.get_trades():
        trd_ele = dconv.conv_TS_Trade_2_cop_trade(trd=trd)
        cop.trade_map[ts_cop_pb2.Cop.FidNum.Trade].trade_list.append(trd_ele)

    return cop

def conv_page_2_cop(dpage: DPage) -> ts_cop_pb2.Cop:
    cop: ts_cop_pb2.Cop = ts_cop_pb2.Cop()

    data_list: List[Union[int, Any]] = dpage.get_fids()
    for ele in data_list:
        fid_num = ele[0]
        value = ele[1]

        if fid_num <= 20000:
            if fid_num <= 10000:
                cop.int32_map[fid_num] = value
            else:
                cop.int64_map[fid_num] = value
        elif fid_num <=40000:
            if fid_num <= 30000:
                cop.float_map[fid_num] = value
            else:
                cop.double_map[fid_num] = value
        elif fid_num <= 50000:
            cop.string_map[fid_num] = value
        elif fid_num <= 70000:
            cop.bool_map[fid_num] = value

    return cop

def conv_TS_Order_2_cop_order(order: TS_Order) -> ts_cop_pb2.TSOrder:
    ord_ele = ts_cop_pb2.TSOrder()

    ord_ele.symbol = order.symbol
    ord_ele.symbol_id = order.symbol_id
    ord_ele.quantity = order.quantity
    ord_ele.fill_quantity = order.fill_quantity
    ord_ele.parent_id = order.parent_id
    ord_ele.order_id = order.order_id
    ord_ele.platform_order_id = order.platform_order_id
    ord_ele.created = to_timestamp_safe(order.created)
    ord_ele.last_update = to_timestamp_safe(order.last_update)
    ord_ele.strategy_name = order.strategy_name
    ord_ele.live_mode = order.live_mode
    ord_ele.strategy_id = order.strategy_id
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
    trd_ele.created = to_timestamp_safe(trd.created)
    trd_ele.last_update = to_timestamp_safe(trd.last_update)
    trd_ele.strategy_name = trd.strategy_name
    trd_ele.live_mode = trd.live_mode
    trd_ele.strategy_id = trd.strategy_id
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
    si_ele.created = to_timestamp_safe(si.created)
    si_ele.last_update = to_timestamp_safe(si.last_update)
    si_ele.strategy_name = si.strategy_name
    si_ele.live_mode = si.live_mode
    si_ele.strategy_id = si.strategy_id

    return si_ele

def conv_cop_order_2_TS_Order(ord_ele: ts_cop_pb2.TSOrder) -> TS_Order:
    order = TS_Order()

    order.symbol = ord_ele.symbol
    order.symbol_id = ord_ele.symbol_id
    order.quantity = ord_ele.quantity
    order.fill_quantity = ord_ele.fill_quantity
    order.parent_id = ord_ele.parent_id
    order.order_id = ord_ele.order_id
    order.platform_order_id = ord_ele.platform_order_id
    order.created = datetime.datetime.fromtimestamp(ord_ele.created)
    order.last_update = datetime.datetime.fromtimestamp(ord_ele.last_update)
    order.strategy_name = ord_ele.strategy_name
    order.live_mode = ord_ele.live_mode
    order.strategy_id = ord_ele.strategy_id
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
    trd.strategy_id = trd_ele.strategy_id
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
    si.strategy_id = si_ele.strategy_id

    return si
