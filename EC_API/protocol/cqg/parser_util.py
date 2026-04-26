#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 27 12:12:27 2025

@author: dexter
"""
# this parser function is needed to handle mixed sub message type in 
# information report, realtimedata and 
from typing import Callable, Any, Optional, Iterable
from google.protobuf.json_format import MessageToDict
from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg
from EC_API.protocol.cqg.router_util import server_msg_type
from EC_API.exceptions import MsgParserError
from EC_API._typing import Parser_func

def walk_fields(
        msg: ServerMsg, 
        selector: Callable[[Any], Any],
        max_depth: int=2
    ) -> list[Any]:
    
    outs: list[Any] = []
    def walk(cur, depth):
        if depth > max_depth:
            return outs
        
        for fd, val in cur.ListFields():
            # do something according to the field
            outs.extend(selector(fd,val))
            
            if fd.message_type is not None:
                if fd.is_repeated:
                    for ele in val:
                        walk(ele, depth+1)
                else:
                    walk(val, depth+1)
    walk(msg, 0)
    return outs
    
# ---- Parsers ----
def parse_server_msg(
        server_msg: ServerMsg,
        parsers: dict[str, Parser_func]
    ) -> list[dict[str, Any]]:
    # Dispatch to message specific parsers
    msg_types = server_msg_type(server_msg)

    if not msg_types:
        raise MsgParserError("Cannot resolve server message type.")
    
    # --- parsing
    res: list[Optional[dict[str, Any]]] = []
    errors: list[str] = []
    for msg_type in msg_types:
        parser = parsers.get(msg_type)

        if parser is None:
            errors.append(
                f"Parser of message type: {msg_type} does not exist."
                )
            continue
        try:
            res.extend(parser(server_msg))
        except Exception as e:
            errors.append(
                f"Failed to parse server message: {e}."
                )
            #continue
    if not res and errors:
        raise MsgParserError("; ".join(errors))
        
    return res
