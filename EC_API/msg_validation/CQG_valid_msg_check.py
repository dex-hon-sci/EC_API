#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  1 09:28:22 2025

@author: dexter
"""
from EC_API.ext.WebAPI.webapi_2_pb2 import ClientMsg, ServerMsg
from EC_API.msg_validation.base import ValidMsgCheck, MsgCheckPara

class CQGValidMsgCheck(ValidMsgCheck):
    # This class is in charge of validating serverresponse message 
    # AFTER sending a request is sent. 
    # It contains a set of checks that is required to resolve if 
    # we receive the correct set of responses from the server.
    
    # check existence, check right types, check desired response 

    def __init__(self):
        
        # Check parameters
        super().__init__()
        #self.para = MsgCheckPara()
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
