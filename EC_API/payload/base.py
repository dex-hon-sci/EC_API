#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 14 19:37:54 2025

@author: dexter
"""
import datetime
from typing import Protcol
from dataclasses import dataclass, field

from EC_API.ext.WebAPI.order_2_pb2 import Order as Ord 
from EC_API.connect.base import ConnectCQG
from EC_API.ordering.CQGLiveOrder import CQGLiveOrder
from EC_API.paylaod.enums import PayloadStatus
from EC_API.ordering.enums import RequestType

class PayloadFormatCheck(Protcol):
    def __init__(self, order_request_type, order_info):
        self.order_request_type = order_request_type
        
    def check(self):
        pass

class CQGFormatCheck(PayloadFormatCheck):
    def __init__(self, 
                 order_request_type: RequestType, 
                 order_info: dict):
        self.order_request_type = order_request_type
        self.order_info = order_info
        
    def check(self):
        # Check account_id
        #self._symbol_name = symbol_name
        #self.request_id = request_id
        #self.account_id = account_id
        #self.sub_scope = sub_scope

        # Check trade_sub

        # Check order request input formats for essential fields
        match self.order_request_type:
            case RequestType.NEW_ORDER:
                
                essentials_field_types = {
                    'contract_id': int, 
                    'cl_order_id': str, 
                    'duration': Ord.Duration,
                    'order_type': Ord.OrderType, 
                    'side': Ord.Side, 
                    'qty_significant': int,
                    }
                
                optional_field_types = {  
                    'when_utc_time': datetime.datetime,
                    'exec_instructions': Ord.ExecInstruction,
                    'good_thru_date': int,
                    'scaled_limit_price': int,
                    'scaled_stop_price': int,
                    'extra_attributes': dict,
                    'scaled_trail_offset': int,
                    'suspend': bool,
                    'algo_strategy': str,
                    'remove_activation_time': bool,
                    'remove_suspension_utc_time': bool,
                    }
                
                # Null checks
                for key in list(essentials_field_types.keys()):
                    if self.order_info.get(key) is None:
                        raise AttributeError(f"Essential parameter(s):\
                                             {key} is missing.")
    
                # Type checks
                for key, value in essentials_field_types:
                    if type(self.order_info[key]) is not self.order_info[key]:
                        raise TypeError(f"Type Error, {key} must be:\
                                        {self.order_info[key]}")
                                        
                # Specific requirements check
                specific_order_field_types = {
                    "scaled_limit_price": int,
                    "scaled_stop_price": int,
                                        }

                ## Order types check
                # For LMT orders
                if self.order_info['order_type'] is Ord.OrderType.ORDER_TYPE_LMT:
                    # Check for scaled limited price
                    if self.order_info.get("scaled_limit_price") is None:
                        raise AttributeError("For LMT orders, missing\
                                             essential field: scaled_limit_price")
                    if self.order_info["scaled_limit_priorder_typece"] is not\
                        specific_order_field_types["scaled_limit_price"]:
                        raise TypeError(f"scaled_limit_price must be:\
                                        {specific_order_field_types['scaled_limit_price']}")
                    
                # For STP orders
                elif self.order_info['order_type'] is Ord.OrderType.ORDER_TYPE_STP: 
                    if self.order_info.get("scaled_stop_price") is None:
                        raise Exception("For LMT orders, missing\
                                        essential field: scaled_stop_price")
                    if self.order_info["scaled_limit_price"] is not\
                        specific_order_field_types["scaled_stop_price"]:
                        raise AttributeError(f"scaled_limit_price must be:\
                                             {specific_order_field_types['scaled_stop_price']}")
                # STL orders                        
                elif self.order_info['order_type'] is Ord.OrderType.ORDER_TYPE_STL:
                    for key, value in specific_order_field_types:
                        if self.order_info.get(key) is None:
                            raise AttributeError(f"Essential parameter(s):\
                                            {key} is missing.")
                        if self.order_info[key] is not specific_order_field_types[key]:
                            raise TypeError(f"{key} must be: {value}.")
                            
                ### Duration GTD case check
                duration_GTD_field_types = {
                    "good_thru_date": int,
                    }
                if self.order_info['duration'] is Ord.Duration.GTD:
                    for key, value in duration_GTD_field_types:
                        if self.order_info.get(key) is None:
                            raise AttributeError(f"Essential parameter(s):\
                                                 {key} is missing.")
                        if self.order_info[key] is not duration_GTD_field_types[key]:
                            raise TypeError(f"{key} must be: {value}.")
                            
                ### Execution instruction case Check
                execution_Trail_field_types = {
                    "scaled_trail_offset": int
                    }
                if self.order_info['exec_instructions'] is\
                    Ord.ExecInstruction.EXEC_INSTRUCTION_TRAIL:
                    for key, value in execution_Trail_field_types:
                        if self.order_info.get(key) is None:
                            raise AttributeError(f"Essential parameter(s):\
                                                 {key} is missing.")
                        if self.order_info[key] is not execution_Trail_field_types[key]:
                            raise TypeError(f"{key} must be: {value}.")   
                            
                            
            case RequestType.MODIFY_ORDER:
                pass
            case RequestType.CANCEL_ORDER:
                pass
            case RequestType.ACRIVATE_ORDER:
                pass
            case RequestType.CANCELALL_ORDER:
                pass
            case RequestType.LIQUIDATEALL_ORDER:
                pass
            case RequestType.GOFLAT_ORDER:
                pass

@dataclass
class Payload(object):
    # An object ready to send out to the trade engine
    # Only the Trade Engine can read the Payload object
    # The Payload Object should contains all the necessary information for 
    # Sending the order.
    # Payload only concern itself with whether the order is sent or not, 
    # it does not tell you the order status (filled or not)
    # Payload check the format coming from Signals
    # One Payload is suppose to be one order request (New, modify, cancel, goflat)
    request_id: int = 0
    account_id: int = 0
    cl_order_id: str = ""
    status: PayloadStatus = PayloadStatus.PENDING
    order_request_type: RequestType = RequestType.NEW_ORDER
    start_time: str = 0 # In long text format
    end_time: str = 0 # In long text format
    order_info: dict = field(default_factory=dict)
    check_method: PayloadFormatCheck = PayloadFormatCheck
    
    def __post_id__(self) -> None:
        # Check the order instructions based on the order type
        # import checking classes and func specific for CQG type orders
        check_obj = self.check_method(self.order_request_type, 
                                      self.order_info)
        check_obj.check()
        

class ExecutePayload_CQG(object):
    # Execution object for CQG trade rounting connection
    def __init__(self, 
                 connect: ConnectCQG, 
                 payload: Payload,
                 request_id: int,
                 account_id: int):
        self._connect = connect 
        self._payload = payload
        self.request_id = request_id
        self.account_id = account_id
    
    def unload(self) -> None:
        """
        Sending order request base on the payload type

        """
        CLOrder = CQGLiveOrder(self._connect, 
                               symbol_name = self._payload.order_info['symbol_name'], 
                               request_id = self.request_id, 
                               account_id = self.account_id)
        CLOrder.send(request_type = self._payload.order_request_type, 
                     request_details = self._payload.order_info)

