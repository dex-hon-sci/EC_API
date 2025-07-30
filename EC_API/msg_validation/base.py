#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 09:34:29 2025

@author: dexter
"""
from dataclasses import dataclass
from WebAPI.webapi_2_pb2 import ClientMsg, ServerMsg

@dataclass
class MsgCheckPara:
    status_check = False # For checking status_code existence
    succes_status_check = False # For checking succe state in status_code
    reject_status_check = False # For checking reject state in status_code
    trade_snapshot_check = False
    result_check = False # Check for result msg existence

class CQGValidMsgCheck(MsgCheckPara):
    # This class is in charge of validating serverresponse message 
    # AFTER sending a request is sent. 
    # It contains a set of checks that is required to resolve if 
    # we receive the correct set of responses from the server.
    
    # check existence, check right types, check desired response 

    def __init__(self):
        pass
        # Check parameters
        
        # build a list for check parameters
        # TradeSubscription
        # new_order_request
        
    def status_check(self, server_msg: ServerMsg):   
        if len(server_msg.trade_subscription_statuses)>0:
            self.status_check = True
            return server_msg
        
    
    def result_check(self, server_msg: ServerMsg):
        return


    def check(self, server_msg: ServerMsg):
        return 
