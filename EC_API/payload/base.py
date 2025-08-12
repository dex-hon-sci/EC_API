#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 14 19:37:54 2025

@author: dexter
"""
import datetime
from datetime import timezone
from typing import Protcol
from dataclasses import dataclass, field

from EC_API.ext.WebAPI.order_2_pb2 import Order as Ord 
from EC_API.connect.base import ConnectCQG
from EC_API.ordering.CQGLiveOrder import CQGLiveOrder
from EC_API.paylaod.enums import PayloadStatus
from EC_API.ordering.enums import RequestType
from EC_API.payload.safety import PayloadFormatCheck

@dataclass
class Payload(object):
    # An object ready to send out to the trade engine
    # Only the Trade Engine can read the Payload object
    # The Payload Object should contains all the necessary information for 
    # Sending the order.
    # Payload only concern itself with whether the order is sent or not, 
    # it does not tell you the order status (filled or not)
    # Payload check the format coming from Signals
    # One Payload is suppose to be one order request 
    # (New, modify, cancel, activate, cancelall,liquateall, goflat)
    account_id: int = 0
    request_id: int = 0
    status: PayloadStatus = PayloadStatus.PENDING
    order_request_type: RequestType = RequestType.NEW_ORDER
    start_time: datetime.datetime = datetime.datetime.now(timezone.utc)\
                                    + datetime.timedelta(days=1)# In long text format
    end_time: datetime.datetime = datetime.datetime.now(timezone.utc)\
                                    + datetime.timedelta(days=2) # In long text format
    order_info: dict = field(default_factory=dict)
    check_method: PayloadFormatCheck = PayloadFormatCheck
    
    def __post_id__(self) -> None:
        # Check the order instructions based on the order type
        # import checking classes and func specific for CQG type orders
        check_obj = self.check_method(self.order_request_type, 
                                      self.order_info)
        check_obj.run()
        

class ExecutePayload_CQG(object):
    # Execution object for CQG trade rounting connection
    def __init__(self, 
                 connect: ConnectCQG, 
                 payload: Payload,
                 request_id: int,
                 account_id: int):
        self._connect = connect 
        self._payload = payload
        self.account_id = account_id
        self.request_id = request_id
        
    def change_payload_status(server_msg):
        pass
    
    def unload(self) -> None:
        """
        Sending order request base on the payload type

        """
        # Only send payload that is pending.
        if self._payload.status == PayloadStatus.PENDING:
            CLOrder = CQGLiveOrder(self._connect, 
                                   symbol_name = self._payload.order_info['symbol_name'], 
                                   request_id = self.request_id, 
                                   account_id = self.account_id)
            server_msg = CLOrder.send(request_type = self._payload.order_request_type, 
                                      request_details = self._payload.order_info)
            # Check if the order is successfuly sent
            #if server_msg #If it is in accept status, change payload status to 
            # SENT, if not, ARCHIEVED
            
        else:
            raise Exception("Only pending payloads can be unloaded.")

### Usage #############################################################
### construct order_info
# order_info = {
#    "symbol_name": "CLEV25",
#    "cl_order_id": "1231314",
#    "order_type": ORDER_TYPE_LMT, 
#    "duration": DURATION_GTC, 
#    "side": SIDE_BUY,
#    "qty_significant": 2,
#    "qty_exponent": 0, 
#    "is_manual": False,
#    "scaled_limit_price": 1000,
#    "good_thru_date": datetime.datetime(2025,9,9),
#    "exec_instructions": EXEC_INSTRUCTION_AON
#     }
#
### Make Payload ######################################################
# Payload(
#   account_id = account_id,
#   request_id = int(random_strin(length=10)),
#   status = PayloadStatus.PENDING,
#   order_request_type = RequestType.NEW_ORDER,
#   start_time = datetime.datetime.now(timezone.utc) + datetime.timedelta(minutes=5)
#   end_time = datetime.datetime.now(timezone.utc) + datetime.timedelta(days=1)
#   order_info = order_info,
#   
#   )
#
### ExecutePayload #####################################################