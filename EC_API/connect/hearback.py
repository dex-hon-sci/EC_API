#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 31 13:25:41 2025

@author: dexter
"""
import time
from typing import Callable
from google.protobuf import json_format
from EC_API.ext.WebAPI.webapi_2_pb2 import ClientMsg, ServerMsg
from EC_API.msg_validation.CQG_valid_msg_check import CQGValidMsgCheck

        
def hearback(func: Callable[str, int], 
             hearback_time: float = 30, *args, **kwargs): 
    client, client_msg = func(*args, **kwargs) 
    def wrapper() -> ServerMsg:  
        start_time = time.time()
        
        while True:
            server_msg = client.receive_server_message()
            # Msg Check 
            check = CQGValidMsgCheck(client_msg, server_msg)
            check.check_all()
            return_msg =  check.return_msg() 
            if return_msg is not None:
                return return_msg
            
            duration = time.time() - start_time
            if duration > hearback_time:
                return 
    return wrapper

def get_contract_metadata(func: Callable[str, int], 
                          *args, **kwargs):
    client, client_msg = func(*args, **kwargs)
    def wrapper() -> ServerMsg:
        # Check if client_msg is an information_request

        while True: # hearback loop
            server_msg = client.receive_server_message()
            check = CQGValidMsgCheck(client_msg, server_msg)
            check.check_all()
            return_msg =  check.return_msg() 
            if return_msg is not None:
                contract_metadata = server_msg.information_reports[0].symbol_resolution_report.contract_metadata
        return contract_metadata
    return wrapper
        

def render_json(server_msg: ServerMsg) -> str:
    json_string = json_format.MessageToJson(server_msg, indent=2)
    print(json_string)

    return json_string

# =============================================================================
#     # Check bool
#     status_check = False
#     trade_snapshot_check = False
#     result_check = False
# 
#     client.send_client_message(client_msg)
#     while True:
#         server_msg = client.receive_server_message()
#                 
# 
#         if server_msg.order_request_rejects is not None: # For catching error message
#             trade_snapshot_check = True 
# 
#         if server_msg.order_statuses is not None:
#             if len(server_msg.order_statuses)>0:
#                 print("recieved order_statues", len(server_msg.order_statuses))
#                 LIS = [server_msg.order_statuses[i].status 
#                        for i in range(len(server_msg.order_statuses))]
#                 print("LIS", LIS)
#                 LIS2 = [server_msg.order_statuses[i].order_id 
#                        for i in range(len(server_msg.order_statuses))]
#                 print("LIS2", LIS2)
#                 #print("TransactionStatus.Status.IN_CANCEL", TransactionStatus.Status.IN_CANCEL)
#                 match LIS[-1]:
#                     case OrderStatus.Status.SUSPENDED:
#                         print("SUSPENDED")
#                     case OrderStatus.Status.ACTIVEAT:
#                         print("ACTIVEAT")
#                         result_check = True
#                     case OrderStatus.Status.FILLED:
#                         result_check = True
#                         print("FILLED")
#                     
# 
#         if trade_snapshot_check and result_check:
#             return order_request, server_msg
# =============================================================================
     