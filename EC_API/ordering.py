#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 19 16:06:10 2025

@author: dexter
"""
from .WebAPI.webapi_2_pb2 import ClientMsg

from .WebAPI.trade_routing_2_pb2.TradeSubscription import SubscriptionScope
from .WebAPI.order_2_pb2.Order import Side, OrderType, Duration

from .WebAPI.trade_routing_2_pb2.TradeSubscription.SubscriptionScope\
                                         import SUBSCRIPTION_SCOPE_ORDERS,\
                                                SUBSCRIPTION_SCOPE_POSITIONS,\
                                                SUBSCRIPTION_SCOPE_COLLATERAL,\
                                                SUBSCRIPTION_SCOPE_ACCOUNT_SUMMARY,\
                                                SUBSCRIPTION_SCOPE_EXCHANGE_POSITIONS,\
                                                SUBSCRIPTION_SCOPE_EXCHANGE_BALANCES 


from .WebAPI.order_2_pb2.Order.Side import SIDE_BUY, SIDE_SELL
from .WebAPI.order_2_pb2.Order.OrderType import ORDER_TYPE_MKT, ORDER_TYPE_LMT,\
                                                ORDER_TYPE_STP, ORDER_TYPE_STL,\
                                                ORDER_TYPE_CROSS
from .WebAPI.order_2_pb2.Order.Duration import DURATION_DAY, DURATION_GTC,\
                                               DURATION_GTD, DURATION_GTT,\
                                               DURATION_FOK, DURATION_FAK,\
                                               DURATION_FOK,DURATION_ATO,\
                                               DURATION_ATC,DURATION_GFA


from EC_API.connect import ConnectCQG
import datetime


class TradeSubscription(object):
    
    def __init__(self, connect: ConnectCQG):
        self._connect = connect
        self.status_check = False
        self.trade_snapshot_check = False
        self.checkcheck = False
        
    def valid_msg_check(self):
        # Check for status_code
        # check for trade_snapshot
        # Check for message type
        return

    def request_trade_subscription(self, 
                                   msg_id: int, 
                                   sub_scope: SubscriptionScope = \
                                              SUBSCRIPTION_SCOPE_ORDERS):
        client_msg = ClientMsg()
        trade_sub_request = client_msg.trade_subscriptions.add()
        # user-defined ID of a request that should be unique to match with possible OrderRequestReject.
        trade_sub_request.id = msg_id
        trade_sub_request.subscribe = True
        # the client can specify the accounts in the request:
        #trade_sub_request.publication_type=1
        #trade_sub_request.account_ids.append(16883045)
        # subscription_scope is an array, we use "extend" to add subscription_scope
        # 1 means order_status, 2 means positions_status, 3 means colleteral_status, deprecated, use 4 instead
        # 4 means account_summary_status, 5 means exchange_positions, 6 means exchange_balances
        trade_sub_request.subscription_scopes.extend([sub_scope])#,2,4,5,6]) 
        
        ## user needs account_summary_parameters when scopes contain 4
        ##account_summary_parameters = trade_sub_request.account_summary_parameters
        # 8 means purchasing_power, 15 means urrent_balance, 16 means profit_loss
        ##account_summary_parameters.requested_fields.extend([8,15,16])
        if sub_scope == SUBSCRIPTION_SCOPE_ACCOUNT_SUMMARY: # SUBSCRIPTION_SCOPE_ACCOUNT_SUMMARY
            account_summary_parameters = trade_sub_request.account_summary_parameters
            # 8 means purchasing_power, 15 means current_balance, 16 means profit_loss
            account_summary_parameters.requested_fields.extend([8,15,16])

        self._connect.client.send_client_message(client_msg)
        print('==============request trade sub complete==============')
    
        while True: 
            server_msg = self._connect.client.receive_server_message()
            if server_msg.trade_snapshot_completions is not None:
                server_msg = self._connect.client.receive_server_message()
                break
            
        return server_msg
    
    
class LiveOrder(object):
    # a class that control the ordering action to the exchange

    def __init__(self, 
                 connect: ConnectCQG, 
                 symbol: str, 
                 request_id: int, 
                 account_id: int):
        self._connect = connect
        self._symbol = symbol
        self.request_id = request_id
        self.account_id = account_id
        
    


    def new_order_request(self, 
                          contract_id: int, # Get this from trade_sub
                          cl_order_id: str, 
                          order_type: OrderType, 
                          duration: Duration, 
                          side: Side,
                          qty_significant:int, # make sure qty are in Decimal not float
                          qty_exponent: int, 
                          is_manual: bool = False,
                          **kwargs):
        
        default_kwargs = {'exec_instructions':None,
                          'good_thru_date': None,
                          'scaled_limit_price': None, 
                          'scaled_stop_price': None}
        
        kwargs = dict(default_kwargs, **kwargs)
        
        client_msg = ClientMsg()
        order_request = client_msg.order_requests.add()
        order_request.request_id = self.request_id
        order_request.new_order.order.account_id = self.account_id
        order_request.new_order.order.when_utc_time = 0
        order_request.new_order.order.contract_id = contract_id
        order_request.new_order.order.cl_order_id = cl_order_id
        order_request.new_order.order.order_type = order_type
        order_request.new_order.order.duration = duration
        order_request.new_order.order.side = side
        order_request.new_order.order.qty.significand = qty_significant
        order_request.new_order.order.qty.exponent = qty_exponent
        order_request.new_order.order.is_manual = is_manual
        
        # add the limit_price when order_type is LIMIT
        if kwargs['exec_instructions'] is not None:
            order_request.new_order.order.exec_instructions.append(kwargs['exec_instructions'])
            
        if kwargs['good_thru_date'] is not None:
            order_request.new_order.order.good_thru_date = kwargs['good_thru_date']
            
        if kwargs['scaled_limit_price'] is not None:
            order_request.new_order.order.scaled_limit_price = kwargs['scaled_limit_price']
            
        if kwargs['scaled_stop_price'] is not None:
            order_request.new_order.order.scaled_stop_price = kwargs['scaled_stop_price']
            
            
        order_request.new_order.order.algo_strategy = "CQG ARRIVALPRICE"
        extra_attributes = order_request.new_order.order.extra_attributes.add()
        extra_attributes.name = "ALGO_CQG_cost_model"
        extra_attributes.value = "1"
    
    
        self._connect.client.send_client_message(client_msg)
        
        # Listen for order confirmation
        
    def modify_order_request(self,  
                             order_id: int, # Get this from the previous Order 
                             orig_cl_order_id: str, 
                             cl_order_id: str, 
                             **kwargs): # WIP
        default_kwargs = {'when_utc_timestamp': datetime.datetime.now(),
                          'qty': 0, 
                          'scaled_limit_price': None,
                          'scaled_stop_price': None,
                          'remove_activation_time': None,
                          'remove_suspension_utc_time': None,
                          'duration': None, 'good_thru_date': None,
                          'good_thru_utc_timestamp': None, 
                          'extra_attributes': None}
        kwargs = dict(default_kwargs, **kwargs)

        client_msg = ClientMsg()
        order_request = client_msg.order_requests.add()
        order_request.request_id = self.request_id
        order_request.modify_order.order_id = order_id
        order_request.modify_order.account_id = self.account_id
        order_request.modify_order.orig_cl_order_id = orig_cl_order_id
        order_request.modify_order.cl_order_id = cl_order_id
        
        if kwargs['qty'] != None:
            order_request.modify_order.qty = kwargs['qty']
        if kwargs['scaled_limit_price'] != None:
            order_request.modify_order.scaled_limit_price = kwargs['scaled_limit_price']
        if kwargs['scaled_stop_price'] != None:
            order_request.modify_order.scaled_stop_price = kwargs['scaled_stop_price']
        if kwargs['remove_activation_time'] != None:
            order_request.modify_order.remove_activation_time = kwargs['remove_activation_time']
        if kwargs['remove_suspension_utc_time'] !=None:
            order_request.modify_order.remove_suspension_utc_time = kwargs['remove_suspension_utc_time']
        if kwargs['duration'] != None:
            order_request.modify_order.duration = kwargs['duration']
        if kwargs['good_thru_date'] != None:
            order_request.modify_order.good_thru_date = kwargs['good_thru_date']
        if kwargs['good_thru_utc_timestamp'] != None:
            order_request.modify_order.good_thru_utc_timestamp = kwargs['good_thru_utc_timestamp']
        if kwargs['extra_attributes'] != None:
            order_request.modify_order.extra_attributes.append(kwargs['extra_attributes'])
        
        self._connect.client.send_client_message(client_msg)
        print('===============order complete=======================')

        while True:
            server_msg = self._connect.client.receive_server_message()
            if server_msg.trade_snapshot_completions is not None:
                server_msg = self._connect.client.receive_server_message()
                
        return server_msg

    def cancel_order_request(self, client, request_id, account_id, order_id, 
                            orig_cl_order_id, cl_order_id,  **kwargs):
        default_kwargs = {'when_utc_timestamp': datetime.datetime.now()}
        kwargs = dict(default_kwargs, **kwargs)

        client_msg = ClientMsg()
        order_request = client_msg.order_requests.add()
        order_request.request_id = request_id
        order_request.cancel_order.order_id = order_id
        order_request.cancel_order.account_id = account_id
        order_request.cancel_order.orig_cl_order_id = orig_cl_order_id
        order_request.cancel_order.cl_order_id = cl_order_id
        order_request.cancel_order.when_utc_timestamp = kwargs['when_utc_timestamp']

        client.send_client_message(client_msg)
        print('===============order complete=======================')

        while True:
            server_msg = client.receive_server_message()
            if server_msg.trade_snapshot_completions is not None:
                server_msg = client.receive_server_message()
                
        return server_msg
    


class AutoOder(Order):
    
    def __init__():
        pass
    
    def send_new_order():
        
# =============================================================================
#         new_order_request(client, 
#                           request_id: int, account_id, order_id, 
#                                 orig_cl_order_id, cl_order_id)
# =============================================================================
        return
    
class OrderPayload():
    # Input Stragtegy Info dict.
    # Output 
    def __init__():
        pass 
    

    
# Strategy calculation and produce order payload
# Order payload table (id, types, time, etc.) for logging and query (DB connections)
# Order function takes in the payload, fire up a thread and send out orders.
# Dynamic intake, read real-life data to make adjustment to to the orders


if __name__ == "__main__":
    # logon
    # Resolve symbol
    # Trade Subscrition
    pass