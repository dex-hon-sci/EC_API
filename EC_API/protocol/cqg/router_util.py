#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 06:21:10 2026

@author: dexter
"""
import logging
from typing import Any
from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg
from EC_API.protocol.cqg.mapping import (
    SERVER_MSG_FAMILY
    )
from EC_API.protocol.cqg.key_extractors import (
    extractors, RouterKey
    )
from EC_API.protocol.cqg.parser_util import (
    master_parsers
    )
from EC_API.exceptions import KeyExtractorError

logger = logging.getLogger(__name__)

def server_msg_type(msg: ServerMsg) -> list[str]:
    # extract the top level server msg field
    return [fd.name for fd, _ in msg.ListFields()]

# --- extractor and parser master functions
def extract_router_keys(
        server_msg: ServerMsg
    ) -> list[RouterKey]:
    
    msg_types = server_msg_type(server_msg)
    if not msg_types:
        raise KeyExtractorError("No Fields were found.")
        
    res: list[RouterKey] = []
    for msg_type in msg_types:
        family = SERVER_MSG_FAMILY.get(msg_type)
        if family is None:
            raise KeyExtractorError(
                f"{msg_type} not found in the avaliable message types."
                )
        
        extractor = extractors.get(family)
        if extractor is None:
            raise KeyExtractorError(
                f"Corresponding extractor for {msg_type} not found."
                )
        try:
            res.extend(extractor(server_msg, msg_type))
        except Exception as e:
            raise KeyExtractorError(
                f"Extractor failed (family={family}, mt={msg_type})"
                ) from e
    return res

# --- Parsers
def parse_server_msg(
        server_msg: ServerMsg
    ) -> list[Any]:
    # Dispatch to message specific parsers
    msg_types = server_msg_type(server_msg)
    res: list[RouterKey] = []
    for msg_type in msg_types:
        parser = master_parsers.get(msg_type)
        if parser is None:
            continue
        try:
            res.extend(parser(server_msg))
        except Exception:
            logger.info('')
            continue
    return res

# --- Message treatment utility
def split_server_msg(msg: ServerMsg, targets: list[str]):
    # Split message on the 
    res: list[ServerMsg] = []
    for target in targets:
        server_msg = ServerMsg()
        field_desc = msg.DESCRIPTOR.fields_by_name.get(target)
        
        if field_desc.is_repeated:
            getattr(server_msg, target).MergeFrom(getattr(msg, target))
        else:# singular field
            setattr(server_msg, target, getattr(server_msg, target))
        res.append(server_msg)
        
    return res

# --- Bool checks ----
def is_realtime_tick(field_name: str) -> bool:
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
