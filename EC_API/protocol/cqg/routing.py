#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 29 10:11:09 2025

@author: dexter
"""

# EC_API/protocol/cqg/routing.py
from dataclasses import dataclass
from __future__ import annotations
from typing import Optional, Tuple
from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg
from google.protobuf.descriptor import FieldDescriptor

Key = Tuple[str, int]

@dataclass(frozen=True)
class RouterKey:
    msg_type: str
# Message type mapping
# 
@dataclass(frozen=True)
class RidHit:
    rid: int
    path: Tuple[str, ...]      # e.g. ("information_reports", "historical_orders_report", "request_id")
    leaf_parent: str           # message type name that owns request_id (descriptor.name)
    
def extract_info_keys(mt, payload_list) -> list[tuple]:
    out = []
    for info in payload_list:
        info_id = getattr(info, "id", 0)
        present = [fd.name for fd, _ in info.ListFields()]
        typed = [n for n in present if n.endswith("_report") or n.endswith("_information_report")]
        if not typed:
            if info_id:
                out.append(("report", "information_reports", "info_id", int(info_id)))
            continue
        for sub in typed:
            if info_id:
                out.append(("report", f"information_reports:{sub}", "info_id", int(info_id)))
            else:
                out.append(("report", f"information_reports:{sub}", "none", 0))
    return out

def server_msg_type(msg: ServerMsg) -> str:
    return msg.WhichOneof("message")  # CQG oneof "message"

# Table-driven request_id extraction for RPC replies
def extract_router_key(msg: ServerMsg) -> Optional[Key]:
    
    keys: list[tuple[str, int]] = []

    for top_fd, top_val in msg.ListFields():
        top = top_fd.name  # e.g. "information_reports"
        if top_fd.type != FieldDescriptor.TYPE_MESSAGE:
            continue
    
        # gather all request_id hits with paths
        hits: list[RidHit] = []
        if top_fd.label == FieldDescriptor.LABEL_REPEATED:
            for item in top_val:
                hits.extend(_walk_request_ids(item, (top,)))
        else:
            hits.extend(_walk_request_ids(top_val, (top,)))
    # recursive extraction of the header of the server_msg

# =============================================================================
#     # Only include RPC-ish reply types here
#     if mt == "information_reports":
#         # Often list; take first item for request_id
#         if len(msg.information_reports) == 0:
#             return None
#         rid = msg.information_reports[0].request_id
#         return (mt, rid)
# 
#     if mt == "user_session_statuses":
#         return (mt, msg.user_session_statuses.request_id)
# 
#     if mt == "market_data_subscription_statuses":
#         return (mt, msg.market_data_subscription_statuses.request_id)
# 
#     if mt == "trade_subscription_statuses":
#         return (mt, msg.trade_subscription_statuses.request_id)
# 
#     if mt == "order_statuses":
#         return (mt, msg.order_statuses.request_id)
# 
# =============================================================================
    # add more as needed
    return None



