#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 06:21:10 2026

@author: dexter
"""
import logging
#from google.protobuf.descriptor import Descriptor, FieldDescriptor
from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg
from EC_API.protocol.cqg.mapping import MAP_RESPONSES_TYPES_STR
from EC_API.protocol.cqg.key_extractors import (
    SERVER_MSG_FAMILY, _extractors, RouterKey
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
        
        extractor = _extractors.get(family)
        if extractor is None:
            logger.info(f"Corresponding extractor for {msg_type} not found.")
            continue
        try:
            res.extend(extractor(server_msg, msg_type))
        except:
            logger.info(f"Extractor failed (family={family}, mt={msg_type})")
            continue
    return res

##########
# Streaming classifiers (examples)
def is_realtime_tick(msg: ServerMsg) -> bool:
    return server_msg_type(msg) in {"real_time_market_data"}

def is_order_update_stream(msg: ServerMsg) -> bool:
    return server_msg_type(msg) in MAP_RESPONSES_TYPES_STR.get('order_requests')

def is_trade_history(msg: ServerMsg) -> bool:
    return server_msg_type(msg) in {"InformationReport:historical_orders_report"}

def is_symbol_resolution(msg: ServerMsg) -> bool:
    return server_msg_type(msg) in {"InformationReport:symbol_resolution_report"}
