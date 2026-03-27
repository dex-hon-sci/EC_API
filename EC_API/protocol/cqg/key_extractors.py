#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 13 20:03:25 2026

@author: dexter
"""
from typing import Callable, Any, Iterable
from dataclasses import dataclass
from google.protobuf.message import Message
from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg
from EC_API.protocol.cqg.mapping import MAP_RESPONSES_TYPES_STR

RouterKey = tuple[str, str, str, int|str] # (msg_family, msg_type, id_field_name, id)
type Extractor_func = Callable[ServerMsg]
extractors: dict[str, Extractor_func] = {}
# =============================================================================
# 
# def extract_any(msg:ServerMsg):
#     res = []
#     TARGET = {}
#     def selector(fd, val) -> Iterable[keyHit]:
#         if fd.message_type is not None and and fd.name in TARGET:
#             yield KeyHit(fd.name, val, True, False)
#     return res
# 
# =============================================================================
KeyHit = tuple[str, int, bool, bool]

def register_extractor(msg_name: str):
    # decorator for registering extractors functions
    def decorator(func: Callable[..., None]):
        extractors[msg_name] = func
        return func
    return decorator

def walk_fields(
        msg: Message, 
        selector: Callable[[Any, Any], Iterable[KeyHit]],
        max_depth: int = 1,
    ) -> list[Any]:
    
    outs: list[KeyHit] = []

    def walk(cur: Any, depth: int) -> None:
        if depth > max_depth:
            return

        # Message: only iterate fields that are present
        if not isinstance(cur, Message):
            return 
        
        for fd, val in cur.ListFields():   
            #### Inject selection function, condition for taking record
            outs.extend(selector(fd, val))

            # Recursvie Descend
            if fd.message_type is not None:
                if fd.is_repeated:# repeated field
                    for elem in val:
                        walk(elem, depth + 1)
                else:# singular field
                    walk(val, depth + 1)
                    
    walk(msg, 0)
    return outs



@register_extractor('session')
def extract_session_router_keys(
        msg: ServerMsg, 
        msg_type: str
    )->list[RouterKey]:
    return [("session", msg_type, "single", 0)]


@register_extractor('info')
def extract_info_keys(
        msg: ServerMsg, 
        msg_type: str                      
    ) -> list[RouterKey]:
    
    TARGET = {                             
        "symbol_resolution_report",
        "session_information_report",
        "historical_orders_report",
        "option_maturity_list_report",
        "instrument_group_report",
        "at_the_money_strike_report"
    }
    
    MAP_RESPONSES_TYPES_STR.get("information_requests")
    
    def selector(fd, val) -> Iterable[KeyHit]:
        if fd.message_type is not None and (fd.name in TARGET or fd.name == "information_reports"):
            yield (fd.name, None, fd.is_repeated, True)
        
        else:
            if fd.name == 'id' and not fd.is_repeated:             
                yield (fd.name, val, fd.is_repeated, False)

    outs = walk_fields(msg, selector, max_depth=1)
    
    report_type, request_id = None, None  
    sub_report_type = ""
    for hit in outs:
        if report_type is None and hit[0] == "information_reports":
            report_type = hit[0]
        if sub_report_type == "" and hit[0] in TARGET:
            sub_report_type = ":"+hit[0]
        if request_id is None and hit[0] == 'id':
            request_id = hit[1]

    if report_type is None or request_id is None:
        return []

    return [("info", report_type+sub_report_type, 
             "id", request_id)]

@register_extractor("rpc_reqid")
def extract_rpc_reqid_router_keys(
        msg: ServerMsg, 
        msg_type: str                      
    ) -> list[RouterKey]:
    
    TARGET = {
        "order_request_rejects", 
        "order_request_acks",
        "go_flat_statuses",
        "time_and_sales_reports",
        "time_bar_reports",
        "volume_profile_reports",
        "non_timed_bar_reports"
    }
    
    def selector(fd, val) -> Iterable[KeyHit]:
        if fd.message_type is not None and fd.name in TARGET:
            yield (fd.name, None, fd.is_repeated, True)
        else:
            if fd.name == 'request_id' and not fd.is_repeated:        
                yield (fd.name, val, fd.is_repeated, False)
    
    outs = walk_fields(msg, selector, max_depth=2)
    
    report_type, request_id = None, None  
    for hit in outs:
        if report_type is None and hit[0] in TARGET:
            report_type = hit[0]
        if request_id is None and hit[0] == 'request_id':
            request_id = hit[1]

    if report_type is None or request_id is None:
        return []

    return [("rpc_reqid", report_type, "request_id", request_id)]

@register_extractor('sub')
def extract_sub_router_keys(
        msg: ServerMsg, 
        msg_type: str                      
    ) -> list[RouterKey]: 
    
    TARGET = {
        "trade_subscription_statuses",
        "trade_snapshot_completions"
        }
    
    def selector(fd, val)-> Iterable[KeyHit]:
        if fd.message_type is not None and fd.name in TARGET:
            yield (fd.name, None, fd.is_repeated, True)
        
        else:
            if fd.name in {'id', 'subscription_id'} and not fd.is_repeated:             
                yield (fd.name, val, fd.is_repeated, False)

    outs = walk_fields(msg, selector, max_depth=2)
    report_type, request_id_name, request_id_val = None, None, None
    
    for hit in outs:
        if report_type is None and hit[0] in TARGET:
            report_type = hit[0]
        if request_id_name is None and hit[0] in {'id', 'subscription_id'}:
            request_id_name = hit[0] 
            request_id_val = hit[1]

    if report_type is None or request_id_name is None:
        return []
    
    return [('sub', report_type, request_id_name, request_id_val)]

@register_extractor('substream')
def extract_substream_router_keys(
        msg: ServerMsg, 
        msg_type: str                      
    )->list[RouterKey]: 
    TARGET = {
        "order_statuses",
        "position_statuses", 
        "account_summary_statuses"
        }
    IDs = {
        'order_statuses': 'order_id',
        'position_statuses': 'contract_id'
        }
    
    def selector(fd, val)-> Iterable[KeyHit]:
        if fd.message_type is not None and fd.name in TARGET:
            yield (fd.name, None, fd.is_repeated, True)
        elif fd.name in {'order_id', 'contract_id'} and not fd.is_repeated:
            yield (fd.name, val, fd.is_repeated, False)

    outs = walk_fields(msg, selector, max_depth=6)

    keys = []
    report_type, request_id_name, request_id_val = None, None, None
    for hit in outs:
        if report_type is None and hit[0] in TARGET:
            report_type = hit[0]
            
            # Handle account_summary no-id behaviour
            if  hit[0] == "account_summary_statuses":
                keys.append(('substream', report_type, 'single', 0))
            continue
        
        expected_id = IDs.get(report_type)
        if request_id_name is None and expected_id is not None and hit[0] == expected_id:
            request_id_name = hit[0]
            request_id_val = hit[1]
        
        if report_type and request_id_name and request_id_val is not None:
            keys.append(('substream', report_type, request_id_name, request_id_val))
            request_id_name, request_id_val = None, None
    return keys

@register_extractor('md')
def extract_market_data_router_keys(
        msg: ServerMsg, 
        msg_type: str                      
    ):
    TARGET = {
        "market_data_subscription_statuses", 
        "real_time_market_data"
        }
    def selector(fd, val)-> Iterable[KeyHit]:
        if fd.message_type is not None and fd.name in TARGET:
            yield (fd.name, None, fd.is_repeated, True)
        elif fd.name in {'contract_id'} and not fd.is_repeated:
            yield (fd.name, val, fd.is_repeated, False)
    
    outs = walk_fields(msg, selector, max_depth=6)
    
    keys = []
    report_type, request_id_name, request_id_val = None, None, None
    for hit in outs:
        if report_type is None and hit[0] in TARGET:
            report_type = hit[0]

        if request_id_name is None and hit[0] == "contract_id":
            request_id_name = hit[0]
            request_id_val = hit[1]
        
        if report_type and request_id_name and request_id_val is not None:
            keys.append(('md', report_type, request_id_name, request_id_val))
            request_id_name, request_id_val = None, None
    return keys


def extract_market_data_contract_id(       
        msg: ServerMsg,
        msg_type: str                      
        )-> int:
    # fast extraction. Use only when we know there is real
    return msg.real_time_market_data[0].contract_id
