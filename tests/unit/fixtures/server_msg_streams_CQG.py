#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 17:55:39 2026

@author: dexter
"""
import random
#from datetime import datetime, timezone
from collections import deque
from itertools import count
from typing import Optional
from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg
from EC_API.ext.common.shared_1_pb2 import OrderStatus, TransactionStatus
from EC_API.ext.WebAPI.webapi_2_pb2 import InformationReport as InfoRp
from tests.unit.fixtures.server_msg_builders_CQG import (
    build_logon_result_server_msg,
    build_pong_server_msg,
    build_restore_or_join_session_result_server_msg,
    build_logged_off_server_msg,
    
    build_symbol_resolution_report_server_msg,
    build_session_info_report_server_msg,
    build_historical_orders_report_server_msg,
    build_option_maturity_list_report_server_msg,
    build_instrument_group_report_server_msg,
    build_at_the_money_strike_report_server_msg,
    
    build_order_request_rejects_server_msg,
    build_order_request_acks_server_msg,
    build_account_summary_statuses_server_msg,
    build_go_flat_statuses_server_msg,
    build_trade_subscription_statuses_server_msg,
    
    build_real_time_market_data_server_msg,
    build_order_statuses_server_msg
)


def dummy_session_stream(pong_number: int = 1000) -> list[ServerMsg]:
    logon_msg = build_logon_result_server_msg()
    restore_msg = build_restore_or_join_session_result_server_msg()
    logoff_msg = build_logged_off_server_msg()
    
    return [logon_msg] + [build_pong_server_msg() for _ in range(pong_number)] + [restore_msg, logoff_msg]
    
    
def dummy_realtime_data_stream(
        total_msg_number: int = 10_000, 
        seed: int = 500
    ) -> list[ServerMsg]:
    rng = random.Random(seed)
    msgs = [
        build_real_time_market_data_server_msg(contract_id=rng.randrange(0, 100))
        for _ in range(total_msg_number)
    ]
    return msgs

def dummy_order_update_stream(
        extension: Optional[dict[int, list[OrderStatus.Status]]] = None
    ) -> list[ServerMsg]:
    
    inputs = {
        0: [OrderStatus.Status.IN_TRANSIT, 
            OrderStatus.Status.WORKING,
            OrderStatus.Status.WORKING,
            OrderStatus.Status.WORKING,
            OrderStatus.Status.FILLED],
         1: [OrderStatus.Status.IN_TRANSIT,
             OrderStatus.Status.IN_TRANSIT,
             OrderStatus.Status.IN_MODIFY,
             OrderStatus.Status.FILLED
             ],
         2: [OrderStatus.Status.IN_TRANSIT,
             OrderStatus.Status.IN_CANCEL,
             OrderStatus.Status.IN_CANCEL,
             OrderStatus.Status.DISCONNECTED
             ]
         }
    if extension:
        inputs = {**inputs, **extension}
    statuses = []
    for key, val in inputs.items():  
        statuses.extend(
            [
                build_order_statuses_server_msg(
                res = val[i],
                contract_id = key,
                sub_id = key,
                order_id= f"order_id_{key}",
                chain_order_id = f"chain_order_id_{key}"
                ) for i in range(len(val))
                ]
            )
            
    return statuses


def dummy_rpc_stream() -> list[ServerMsg]:
    order_request_rejects_msg = build_order_request_rejects_server_msg()
    order_request_acks_msg = build_order_request_acks_server_msg()
    account_summary_statuses_msg = build_account_summary_statuses_server_msg()
    go_flat_statuses_msg = build_go_flat_statuses_server_msg()
    
    trade_subscription_statuses_msg = build_trade_subscription_statuses_server_msg()

    
    return [trade_subscription_statuses_msg, order_request_rejects_msg,
            order_request_acks_msg, account_summary_statuses_msg,
            go_flat_statuses_msg
            ]

def dummy_info_stream(
        info_extension: Optional[list[tuple[int, str, str, str, str, str, str, str]]] = None
        ) -> list[ServerMsg]:
    inputs = [
        (1, "CLE", "1", "A", "id_1", "CLEXXX", "id_1", "Instrument_1"),
        (2, "HOE", "2", "B", "id_2", "HOEXXX", "id_2", "Instrument_2"),
        (3, "RBE", "3", "C", "id_3", "RBEXXX", "id_3", "Instrument_3"),
        (4, "QO", "4", "D", "id_4", "QOXXX", "id_4", "Instrument_4"),
        (5, "QP", "5", "E", "id_5", "QPXXX", "id_5", "Instrument_5"),
        (6, "VX", "6", "F", "id_6", "VXXXX", "id_6", "Instrument_6"),
        (7, "AUX", "7", "G", "id_7", "AUXXXX", "id_7", "Instrument_7"),
        (8, "AG", "8", "H", "id_8", "AGXXX", "id_8", "Instrument_8"),
        (9, "VC", "9", "I", "id_9", "VCXXX", "id_9", "Instrument_9"),
        (10, "EUR", "10", "J", "id_10", "EURXXX", "id_10", "Instrument_10"),
        (11, "YU", "11", "K", "id_11", "YUXXX", "id_11", "Instrument_11"),
        (12, "TAR", "12", "L", "id_12", "TARXXX", "id_12", "Instrument_12"),
        (13, "PEQ", "13", "M", "id_13", "PEQXXX", "id_13", "Instrument_13"),
    ] 
    if info_extension:
        inputs.extend(info_extension)
    # (contract_id, contract_name, order_id, chain_order_id,
    #  option_id, option_name, instrument_id, instrument_name)
    report_id = count(0)

    info = []
    for contract_id, contract_name, order_id, chain_order_id, \
        option_id, option_name, instrument_id, instrument_name in inputs:
 
        info.append(build_symbol_resolution_report_server_msg(
            res = InfoRp.StatusCode.STATUS_CODE_SUCCESS,
            report_id = next(report_id),
            cotract_id = contract_id,
            contract_symbol = contract_name))
        info.append(build_session_info_report_server_msg(
           res = InfoRp.StatusCode.STATUS_CODE_SUCCESS,
           report_id = next(report_id),
           ))
        info.append(build_historical_orders_report_server_msg(
           res = InfoRp.StatusCode.STATUS_CODE_SUCCESS,
           report_id = next(report_id),
           order_id = order_id,
           chain_order_id = chain_order_id
           ))
        info.append(build_option_maturity_list_report_server_msg(
           res = InfoRp.StatusCode.STATUS_CODE_SUCCESS,
           report_id = next(report_id),
           option_id = option_id,
           option_name = option_name
           ))
        info.append(build_instrument_group_report_server_msg(
           res = InfoRp.StatusCode.STATUS_CODE_SUCCESS,
           report_id = next(report_id),
           instrument_id = instrument_id,
           instrument_name = instrument_name
           ))
        info.append(build_at_the_money_strike_report_server_msg(
           res = InfoRp.StatusCode.STATUS_CODE_SUCCESS,
           report_id = next(report_id),
           ))
             
    return info

def dummy_mixed_full_stream(seed: int = 500) -> list[ServerMsg]:
    rng = random.Random(seed)
    # make a mixed stream with all dummy message streams
    # Set up like the following:
    # (1) session_stream first half, pong message all mixed in
    # (2) randomise info_stream, mix with realdata_stream
    # (3) rpc_stream mix in
    # (4) session_stream second half
    def mixer(session, orders, info, realdata, rpc) -> list[ServerMsg]:
        sources = [deque(session), 
                   deque(orders), 
                   deque(info), 
                   deque(realdata), 
                   deque(rpc)]
        
        bucket = []
        while sources:
               source = rng.choice(sources)              
               if not source:
                   sources.remove(source)
                   continue
               bucket.append(source.popleft())
        return bucket
    session_stream = dummy_session_stream()
    order_update_stream = dummy_order_update_stream()
    info_stream = dummy_info_stream()
    realdata_stream = dummy_realtime_data_stream()
    rpc_stream = dummy_rpc_stream()
    
    total_stream = []
    total_stream.append(session_stream[0]) # logon message
    total_stream.extend(
        mixer(session_stream[1:-1],
              order_update_stream,
              info_stream,
              realdata_stream, 
              rpc_stream)
        )
    total_stream.append(session_stream[-1]) # logoff message
    
    return total_stream

def stream_generator(stream: list[ServerMsg]):
    q = deque(stream)
    while q:
        yield q.popleft()#dummy_mixed_full_stream()