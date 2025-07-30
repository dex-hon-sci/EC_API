#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 09:56:19 2025

@author: dexter
"""
from WebAPI.webapi_2_pb2 import ClientMsg, ServerMsg

from EC_API.ordering.enums import *
from EC_API.connect import ConnectCQG
from EC_APU.msg_validation.base import MsgCheckPara

class TradeSubscription(object):
    
    def __init__(self, connect: ConnectCQG):
        self._connect = connect
        self.msg_type = "TradeSubscription"

        # Initial Parameters
        self.subscribe = True
        self.sub_scope = SUBSCRIPTION_SCOPE_ORDERS
        self.skip_orders_snapshot = False
        
        # Defacto messages
        self.status_msg = None
        self.result_msg = None
        
        # Check parameters
        self.msg_check_para = MsgCheckPara()
        self.status_check = False
        self.trade_snapshot_check = False
        self.result_check = False
                
    def valid_msg_check(self, server_msg: ServerMsg):
        # Check for status_code
        # check for trade_snapshot
        # Check for message type
        
        result_types = {"1": server_msg.order_statuses, 
                        "2": server_msg.position_statuses, 
                        "3": server_msg.collateral_statuses, 
                        "4": server_msg.account_summary_statuses}
        
        print("ts_msg:", server_msg)

        if len(server_msg.trade_subscription_statuses)>0:
            print("If trade_subscription_statuses>0")
            print(len(server_msg.trade_subscription_statuses))
            print(server_msg.trade_subscription_statuses)
            self.status_msg = server_msg
            self.status_check = True
            
            if self.subscribe == False: # break if this is a unsubscribe msg
                print("Break for unsub")
                return self.status_msg, server_msg

        if server_msg.trade_snapshot_completions is not None:
            print("IF snapshot is not None")
            print("snap", server_msg.trade_snapshot_completions,)
            self.trade_snapshot_check = True

            #server_msg = client.receive_server_message()
            
        if result_types[str(self.sub_scope)] is not None:
            result_msg = server_msg
            self.result_check = True
            print("result", result_msg, server_msg.account_summary_statuses)
        return

    def request_trade_subscription(self, 
                                   msg_id: int)->ServerMsg:
                                   #subscribe = True,
                                   #skip_orders_snapshot = False,
                                   #sub_scope: TS.SubscriptionScope = \
                                   #          SUBSCRIPTION_SCOPE_ORDERS):
        client_msg = ClientMsg()
        trade_sub_request = client_msg.trade_subscriptions.add()
        # user-defined ID of a request that should be unique to match with possible OrderRequestReject.
        trade_sub_request.id = msg_id
        trade_sub_request.subscribe = self.subscribe
        trade_sub_request.skip_orders_snapshot = self.skip_orders_snapshot

        # the client can specify the accounts in the request:
        #trade_sub_request.publication_type=1
        #trade_sub_request.account_ids.append(16883045)
        # subscription_scope is an array, we use "extend" to add subscription_scope
        # 1 means order_status, 2 means positions_status, 3 means colleteral_status, deprecated, use 4 instead
        # 4 means account_summary_status, 5 means exchange_positions, 6 means exchange_balances
        trade_sub_request.subscription_scopes.extend([self.sub_scope])#,2,4,5,6]) 
        
        ## user needs account_summary_parameters when scopes contain 4
        ##account_summary_parameters = trade_sub_request.account_summary_parameters
        # 8 means purchasing_power, 15 means urrent_balance, 16 means profit_loss
        ##account_summary_parameters.requested_fields.extend([8,15,16])
        if self.sub_scope == SUBSCRIPTION_SCOPE_ACCOUNT_SUMMARY: # SUBSCRIPTION_SCOPE_ACCOUNT_SUMMARY
            account_summary_parameters = trade_sub_request.account_summary_parameters
            # 8 means purchasing_power, 15 means current_balance, 16 means profit_loss
            account_summary_parameters.requested_fields.extend([8,15,16])

        self._connect.client.send_client_message(client_msg)
        print('==============request trade sub complete==============')
    
        while True: 
            server_msg = self._connect.client.receive_server_message()
            
            result_types = {"1": server_msg.order_statuses, 
                            "2": server_msg.position_statuses, 
                            "3": server_msg.collateral_statuses, 
                            "4": server_msg.account_summary_statuses}
            print("ts_msg:", server_msg)

            if len(server_msg.trade_subscription_statuses)>0:
                print("If trade_subscription_statuses>0")
                print(len(server_msg.trade_subscription_statuses))
                print(server_msg.trade_subscription_statuses)
                self.status_check = True
                self.status_msg = server_msg

                
                if self.subscribe == False: # break if this is a unsubscribe msg
                    print("Break for unsub")
                    return trade_sub_request, self.status_msg, self.result_msg

            if server_msg.trade_snapshot_completions is not None:
                print("IF snapshot is not None")
                print("snap", server_msg.trade_snapshot_completions,)
                trade_snapshot_check = True

                #server_msg = client.receive_server_message()
                
            if result_types[str(self.sub_scope)] is not None:
                self.result_msg = server_msg
                result_check = True
                print("result", self.result_msg, server_msg.account_summary_statuses)

                
            if status_check and trade_snapshot_check and result_check:
                return trade_sub_request, self.status_msg, self.result_msg
            
            
                
            # Order type requirement checks (LMT, scaled_price) (STP, scaled_stop_price)
            # Order duration reauirement checks () ()