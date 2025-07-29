#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 29 13:19:48 2025

@author: dexter
"""
from dataclasses import dataclass, field

from WebAPI.webapi_2_pb2 import ClientMsg
from WebAPI.trade_routing_2_pb2 import TradeSubscription as TS
from WebAPI.order_2_pb2 import Order as Ord #Side, OrderType, Duration

from EC_API.ordering.enums import *
from EC_API.connect import ConnectCQG
import datetime
from datetime import timezone

# message check data class

@dataclass
class MsgCheckPara:
    msg_type: str = "TradeSubscription"
    status_check = False
    trade_snapshot_check = False
    result_check = False


class ValidMsgCheck(MsgCheckPara):
    # This class is incharge of valid message check AFTER sending a request to 
    # the server. It contains a set of checks that is required to resolve if 
    # we receive the correct set of responses from the server.
    
    # check existence, check right types, check desired response 

    def __init__(self):
        # Check parameters
        self.msg_type = "TradeSubscription"
        self.status_check = False
        self.trade_snapshot_check = False
        self.result_check = False
        
        # build a list for check parameters
        # TradeSubscription
        # new_order_request
        
    def status_check(self, server_msg):
        return
    
    def result_check(self, server_msg):
        return


    def check(self, server_msg):
        return 


class TradeSubscription(object):
    
    def __init__(self, connect: ConnectCQG):
        self._connect = connect
        
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
                
    def valid_msg_check(self, server_msg):
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
                                   msg_id: int, 
                                   ):
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
                self.status_msg = server_msg
                status_check = True
                
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
        
    def _resolve_symbols():
        return
        
    def new_order_request(self, 
                          contract_id: int, # Get this from trade_sub
                          cl_order_id: str, 
                          order_type: Ord.OrderType, 
                          duration: Ord.Duration, 
                          side: Ord.Side,
                          qty_significant:int, # make sure qty are in Decimal (int) not float
                          qty_exponent: int, 
                          is_manual: bool = False,
                          **kwargs):
        
        default_kwargs = {'when_utc_timestamp': datetime.datetime.now(),
                          'exec_instructions':None,
                          'good_thru_date': None,
                          'scaled_limit_price': None, 
                          'scaled_stop_price': None,
                          'sub_scope':1}
        
        kwargs = dict(default_kwargs, **kwargs)
        
        client_msg = ClientMsg()
        order_request = client_msg.order_requests.add()
        order_request.request_id = self.request_id
        order_request.new_order.order.account_id = self.account_id
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
            
        if kwargs['when_utc_time'] is not None:
            order_request.new_order.order.when_utc_time = kwargs['when_utc_timestamp']

        order_request.new_order.order.algo_strategy = "CQG ARRIVALPRICE"
        extra_attributes = order_request.new_order.order.extra_attributes.add()
        extra_attributes.name = "ALGO_CQG_cost_model"
        extra_attributes.value = "1"
    
        sub_scope = kwargs['sub_scope']
    
# =============================================================================
#         self._connect.client.send_client_message(client_msg)
#         while True:
#             server_msg = self._connect.client.receive_server_message()
#             if server_msg.trade_snapshot_completions is not None:
#                 server_msg = self._connect.client.receive_server_message()
#         return server_msg
# =============================================================================
    
        self._connect.client.send_client_message(client_msg)
        while True:
            server_msg = self._connect.client.receive_server_message()
            print(server_msg)
                    
            result_types = {"1": server_msg.order_statuses, 
                            "2": server_msg.position_statuses, 
                            "3": server_msg.collateral_statuses, 
                            "4": server_msg.account_summary_statuses}
    
            if server_msg.trade_snapshot_completions is not None:
                trade_snapshot_check = True
                    
            if len(result_types[str(sub_scope)]) >0: 
                if sub_scope in [1]:
                    LIS_status = [result_types[str(sub_scope)][i].status 
                                       for i in range(len(result_types[str(sub_scope)]))]
                    LIS_clorderid = [result_types[str(sub_scope)][i].order.cl_order_id 
                                       for i in range(len(result_types[str(sub_scope)]))]
        
                    print("LIS_status, LIS_clorderid", LIS_status, LIS_clorderid)
                    try:
                        # If we find the index we return
                        index = LIS_clorderid.index(cl_order_id)
        
                        print('index', index)
                        print("======Result =============")
                        result_check = True
                        result_msg = server_msg
                        print("result", result_msg, result_types[str(sub_scope)])
                    except:
                        pass
                elif sub_scope in [2,3,4]:
                    result_check = True
                    result_msg = server_msg
    
                    
            if self.result_check and self.trade_snapshot_check:
                return result_msg
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
                          'extra_attributes': None,'sub_scope':1}
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
        sub_scope = kwargs['sub_scope']

        while True:
            server_msg = self._connect.client.receive_server_message()
            print("S_MSG", server_msg)
                    
            result_types = {"1": server_msg.order_statuses, 
                            "2": server_msg.position_statuses, 
                            "3": server_msg.collateral_statuses, 
                            "4": server_msg.account_summary_statuses}
    
            if server_msg.trade_snapshot_completions is not None:
                trade_snapshot_check = True
                                            
            if len(result_types[str(sub_scope)]) >0: 
                print("======Result =============",)
                result_msg = server_msg
                result_check = True
                print("result", result_msg, result_types[str(sub_scope)])
    
                    
            if result_check and trade_snapshot_check:
                #server_msg = client.receive_server_message()
    
                return result_msg


    def cancel_order_request(self, 
                             order_id: int, 
                             orig_cl_order_id: str, 
                             cl_order_id: str,  
                             **kwargs):
        default_kwargs = {'when_utc_timestamp': datetime.datetime.now(timezone.utc).timestamp()}
        #default_kwargs = {'when_utc_timestamp': datetime.datetime.now(timezone.utc)}
        kwargs = dict(default_kwargs, **kwargs)
    
# =============================================================================
#         dt = datetime.datetime.fromtimestamp(kwargs['when_utc_timestamp'])
#         T = Timestamp()
#         T.FromDatetime(dt)
#         print("Google Timestamp", T)
# =============================================================================
        
        client_msg = ClientMsg()
        order_request = client_msg.order_requests.add()
        order_request.request_id = self.request_id
        order_request.cancel_order.order_id = order_id
        order_request.cancel_order.account_id = self.account_id
        order_request.cancel_order.orig_cl_order_id = orig_cl_order_id
        order_request.cancel_order.cl_order_id = cl_order_id
        order_request.cancel_order.when_utc_timestamp = kwargs['when_utc_timestamp']
    
        self._connect.client.send_client_message(client_msg)
        print('===============order complete=======================')
        # Check bool
        status_check = False
        trade_snapshot_check = False
        result_check = False
    
        while True:
            server_msg = self._connect.client.receive_server_message()
            
            result_types = {"1": server_msg.order_statuses, 
                            "2": server_msg.position_statuses, 
                            "3": server_msg.collateral_statuses, 
                            "4": server_msg.account_summary_statuses}
    
            if server_msg.order_request_rejects is not None: # For catching error message
                trade_snapshot_check = True 
            
            if server_msg.order_statuses is not None:
                if len(server_msg.order_statuses)>0:
                    print("recieved order_statues", len(server_msg.order_statuses))
                    LIS = [server_msg.order_statuses[i].status 
                           for i in range(len(server_msg.order_statuses))]
                    print("LIS", LIS)
                    LIS2 = [server_msg.order_statuses[i].order_id 
                           for i in range(len(server_msg.order_statuses))]
                    print("LIS2", LIS2)
                    #print("TransactionStatus.Status.IN_CANCEL", TransactionStatus.Status.IN_CANCEL)
                    match LIS[-1]:
                        case Ord.OrderStatus.Status.IN_CANCEL:
                            print("IN_CANCEL")
                        case Ord.OrderStatus.Status.CANCELLED:
                            print("CANCELLED")
                            self.result_check = True
                        case Ord.OrderStatus.Status.REJECTED:
                            self.result_check = True
                            print("REJECTED")
                        
    
            if self.trade_snapshot_check and self.result_check:
                return order_request, server_msg
    
    def activate_order_request(self, 
                               order_id: int, 
                               orig_cl_order_id: str, 
                               cl_order_id: str, 
                               **kwargs):
        default_kwargs = {'when_utc_timestamp': datetime.datetime.now(timezone.utc),
                          }
        kwargs = dict(default_kwargs, **kwargs)
        client_msg = ClientMsg()
        order_request = client_msg.order_requests.add()
        order_request.request_id = self.request_id
        order_request.activate_order.order_id = order_id
        order_request.activate_order.account_id = self.account_id
        order_request.activate_order.orig_cl_order_id = orig_cl_order_id
        order_request.activate_order.cl_order_id = cl_order_id
        order_request.activate_order.when_utc_timestamp = kwargs['when_utc_timestamp']
        
        print('===============order complete=======================')
    
        self._connect.client.send_client_message(client_msg)
        while True:
            server_msg = self._connect.client.receive_server_message()
                    
            if server_msg.order_request_rejects is not None: # For catching error message
                self.trade_snapshot_check = True 
    
            if server_msg.order_statuses is not None:
                if len(server_msg.order_statuses)>0:
                    print("recieved order_statues", len(server_msg.order_statuses))
                    LIS = [server_msg.order_statuses[i].status 
                           for i in range(len(server_msg.order_statuses))]
                    print("LIS", LIS)
                    LIS2 = [server_msg.order_statuses[i].order_id 
                           for i in range(len(server_msg.order_statuses))]
                    print("LIS2", LIS2)
                    #print("TransactionStatus.Status.IN_CANCEL", TransactionStatus.Status.IN_CANCEL)
                    match LIS[-1]:
                        case OrderStatus.Status.SUSPENDED:
                            print("SUSPENDED")
                        case OrderStatus.Status.ACTIVEAT:
                            print("ACTIVEAT")
                            self.result_check = True
                        case OrderStatus.Status.FILLED:
                            self.result_check = True
                            print("FILLED")
                        
    
            if self.trade_snapshot_check and self.result_check:
                return order_request, server_msg
    
    def cancelall_order_request(self,**kwargs):
        # TBD
        return 
    
    def suspend_order_request(self,**kwargs): # SuspendOrder

        return 
    
    def Liquidateall_order_request(self,**kwargs): # LiquidateAll

        return 

    
    def goflat_order_request(self, **kwargs):
        default_kwargs = {'when_utc_timestamp': datetime.datetime.now(),
                          'execution_source_code': None, 
                          'speculation_type': None}
        kwargs = dict(default_kwargs, **kwargs)
    
        client_msg = ClientMsg()
        order_request = client_msg.order_requests.add()
        order_request.request_id = self.request_id
        order_request.go_flat.account_ids.append(self.account_id)
        order_request.go_flat.when_utc_timestamp = kwargs['when_utc_timestamp']
        #order_request.go_flat.execution_source_code = kwargs['execution_source_code']
        #order_request.go_flat.speculation_type = kwargs['speculation_type']
        self._connect.client.send_client_message(client_msg)
        
        print('===============Go Flat on all orders=======================')
    
        while True:
            server_msg = self._connect.client.receive_server_message()
            if server_msg.trade_snapshot_completions is not None:
                server_msg = self._connect.client.receive_server_message()
                break
                
        return server_msg


if __name__ == "__main__":
    ## Usage example
    # logon
    # Resolve symbol
    # Trade Subscrition
    pass