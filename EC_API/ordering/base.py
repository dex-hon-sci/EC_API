#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 29 13:19:48 2025

@author: dexter
"""
from collections import Protocol

from EC_API.ordering.enums import *
from EC_API.connect import Connect
from EC_API.msg_validation.base import CQGValidMsgCheck

class LiveOrder(Protocol):
    def __init__(self, 
                 connect: Connect,
                 symbol_name: str,
                 request_id: int,
                 account_id:int):
        self._connect = connect
        self._symbol_name = symbol_name
        self.request_id = request_id
        self.account_id = account_id

    def new_order_request(self):
        """
        New order request. Return a tracking ID for reference and modifications.

        """
        pass
    
    def modify_order_request(self, ID):
        """
        Modify order request. Input ID and new values in allowed fields for 
        existing unresolved orders.

        """
        pass
    
    def cancel_order_request(self, ID):
        """
        Cancel order request. Input ID and cancel existing unresolved orders.
        """
        pass
    
    def activate_order_request(self, ID):
        """
        Activate order request. Input ID and activate existing suspended orders.
        """
        pass
    
    def cancelall_order_request(self):
        """
        Cancel all unresolved order requests based on the account_id.
        """
        pass
    
    def liquidateall_order_request(self):
        """
        Liquidate all open positions based on the account_id.
        """

        pass
    
    def goflat_order_request(self):
        """
        Liquidate  all positions and cancel all unresolved order requests 
        based on the account_id.
        """

        pass
    
    def send(self, 
             request_type: RequestType,
             request_details: dict):
        """
        Master function for running LiveOrder object. Send order requests to 
        the exchange provided some request details matching the request types.

        Parameters
        ----------
        request_type : str
            DESCRIPTION.
        request_details : dict
            DESCRIPTION.

        Returns
        -------
        None.

        """
        match request_type:
            case RequestType.NEW_ORDER:
                # For new_order_request -> return OrderID
                self.new_order_request(**request_details)
    
            case RequestType.MODIFY_ORDER:
                # For other oder_requests, use the OrderID from new_order_request
                self.modify_order_request(**request_details)
            
            case RequestType.CANCEL_ORDER:
                self.cancel_order_request(**request_details)
            
            case RequestType.ACRIVATE_ORDER:
                self.activate_order_request(**request_details)
            
            case RequestType.CANCELALL_ORDER:
                self.cancelall_order_request(**request_details)
                
            case RequestType.LIQUIDATEALL_ORDER:
                self.liquidateall_order_request(**request_details)
                
            case RequestType.GOFLAT_ORDER:
                self.goflat_order_request(**request_details)
