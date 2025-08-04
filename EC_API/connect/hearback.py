#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 31 13:25:41 2025

@author: dexter
"""
from EC_API.msg_validation.base import *
from EC_API.msg_validation.CQG_valid_msg_check import CQGValidMsgCheck

def hearback(client, hearback_time):
    # A decorator function in charge of hearing back a message after sending it
    
    while True:
        
        # Msg Check 
        pass
    return
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
     