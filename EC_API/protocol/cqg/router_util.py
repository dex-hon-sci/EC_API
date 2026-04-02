#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 06:21:10 2026

@author: dexter
"""
import logging
#from google.protobuf.descriptor import Descriptor, FieldDescriptor
from google.protobuf.internal.containers import (
    RepeatedScalarFieldContainer, 
    RepeatedCompositeFieldContainer
)
from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg
from EC_API.protocol.cqg.mapping import MAP_RESPONSES_TYPES_STR, SERVER_MSG_FAMILY
from EC_API.protocol.cqg.key_extractors import (
    extractors, RouterKey
)
logger = logging.getLogger(__name__)

def server_msg_type(msg: ServerMsg) -> list[str]:
    # extract the top level server msg field
    return [fd.name for fd, _ in msg.ListFields()]

def extract_router_keys(
        server_msg: ServerMsg
    ) -> list[RouterKey]:
    msg_types = server_msg_type(server_msg)
    res = []
    for msg_type in msg_types:
        family = SERVER_MSG_FAMILY.get(msg_type)
        if family is None:
            logger.info(f"{msg_type} not found in the avaliable message types.")
            continue
        
        extractor = extractors.get(family)
        if extractor is None:
            logger.info(f"Corresponding extractor for {msg_type} not found.")
            continue
        try:
            res.extend(extractor(server_msg, msg_type))
        except Exception:
            logger.info(f"Extractor failed (family={family}, mt={msg_type})")
            continue
    return res

def split_server_msg(msg: ServerMsg, targets: list[str]):
    res = []
    for target in targets:
        server_msg = ServerMsg()
        field_desc = msg.DESCRIPTOR.fields_by_name.get(target)
        #if field_desc.label == field_desc.LABEL_REPEATED:# repeated field
        if field_desc.is_repeated:
            getattr(server_msg, target).MergeFrom(getattr(msg, target))
        else:# singular field
            setattr(server_msg, target, getattr(server_msg, target))
        res.append(server_msg)

    return res

# --- Bool checks ----
def is_realtime_tick(field_name: str) -> bool: # msg: ServerMsg) -> bool:
    #for fd_name in server_msg_type(msg):
    #return True if fd_name in {"real_time_market_data"} else False
    return True if field_name in {"real_time_market_data"} else False

def is_order_update_stream(field_name: str) -> bool:
    return True if field_name in {"order_statuses"} else False

def is_trade_history(field_name: str) -> bool:
    return True if field_name in {"InformationReport:historical_orders_report"} else False

def is_symbol_resolution(field_name: str) -> bool:
    return True if field_name in {"InformationReport:symbol_resolution_report"} else False

# --- id extractor ---
def realtime_tick_contract_id(msg: ServerMsg) -> int:
    return msg.real_time_market_data[0].contract_id

def order_statuses_order_id(msg: ServerMsg) -> str:
    return msg.order_statuses[0].chain_order_id

