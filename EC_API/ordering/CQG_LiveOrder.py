#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 10:01:16 2025

@author: dexter
"""
import datetime
from datetime import timezone

from EC_API.ext.WebAPI.order_2_pb2 import Order as Ord 
from EC_API.ext.WebAPI.webapi_2_pb2 import ClientMsg, ServerMsg

from EC_API.connect import ConnectCQG
from EC_API.connect.hearback import hearback, get_contract_metadata
from EC_API.ordering.enums import *
from EC_API.ordering.base import LiveOrder

class CQGLiveOrder(LiveOrder):
    # a class that control the ordering action to the exchange
    # This object is specific for CQG type request

    def __init__(self, 
                 connect: ConnectCQG, 
                 symbol_name: str, 
                 request_id: int, 
                 account_id: int):
        
        self._connect = connect
        self._symbol_name = symbol_name
        self.request_id = request_id
        self.account_id = account_id

    @get_contract_metadata
    def _resolve_symbols(self, 
                         msg_id: int, 
                         subscribe=None, 
                         **kwargs):
        client_msg = ClientMsg()
        information_request = client_msg.information_requests.add()
        information_request.id = msg_id
        if subscribe is not None:
            information_request.subscribe = subscribe
            
        information_request.symbol_resolution_request.symbol = self._symbol_name
        
        if 'instrument_group_request' in kwargs:
            information_request.instrument_group_request = kwargs['instrument_group_request']
        
        self._connect.client.client.send_client_message(client_msg)
        return 
    
    @hearback
    def _request_trade_subscription(self,
                                    trade_subscription_id: int,
                                    subscribe: bool = False,
                                    sub_scope: int = SUBSCRIPTION_SCOPE_ORDERS,
                                    skip_orders_snapshot: bool = False):
        
        client_msg = ClientMsg()
        trade_sub_request = client_msg.trade_subscriptions.add()
        trade_sub_request.id = trade_subscription_id
        trade_sub_request.subscribe = subscribe
        trade_sub_request.subscription_scopes.append(sub_scope)
        trade_sub_request.skip_orders_snapshot = skip_orders_snapshot
        #trade_sub_request.last_order_update_utc_timestamp = last_order_update_utc_timestamp
        
        if sub_scope == SUBSCRIPTION_SCOPE_ACCOUNT_SUMMARY:
            account_summary_parameters = trade_sub_request.account_summary_parameters
            # 8 means purchasing_power, 15 means current_balance, 16 means profit_loss
            account_summary_parameters.requested_fields.extend([8,15,16])
            
        self._connect.client.send_client_message(client_msg)

        return 

    @hearback
    def new_order_request(self, 
                          contract_id: int, # Get this from contractmetadata
                          cl_order_id: str, 
                          order_type: Ord.OrderType, 
                          duration: Ord.Duration, 
                          side: Ord.Side,
                          qty_significant:int, # make sure qty are in Decimal (int) not float
                          qty_exponent: int, 
                          is_manual: bool = False,
                          **kwargs) -> ServerMsg:
        
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
        
        self._connect.client.send_client_message(client_msg)
        return self._connect.client, client_msg

# =============================================================================
#         while True:
#             server_msg = self._connect.client.receive_server_message()
#             print(server_msg)
#                     
#             result_types = {"1": server_msg.order_statuses, 
#                             "2": server_msg.position_statuses, 
#                             "3": server_msg.collateral_statuses, 
#                             "4": server_msg.account_summary_statuses}
#     
#             if server_msg.trade_snapshot_completions is not None:
#                 trade_snapshot_check = True
#                     
#             if len(result_types[str(sub_scope)]) >0: 
#                 if sub_scope in [1]:
#                     LIS_status = [result_types[str(sub_scope)][i].status 
#                                        for i in range(len(result_types[str(sub_scope)]))]
#                     LIS_clorderid = [result_types[str(sub_scope)][i].order.cl_order_id 
#                                        for i in range(len(result_types[str(sub_scope)]))]
#         
#                     print("LIS_status, LIS_clorderid", LIS_status, LIS_clorderid)
#                     try:
#                         # If we find the index we return
#                         index = LIS_clorderid.index(cl_order_id)
#         
#                         print('index', index)
#                         print("======Result =============")
#                         result_check = True
#                         result_msg = server_msg
#                         print("result", result_msg, result_types[str(sub_scope)])
#                     except:
#                         pass
#                 elif sub_scope in [2,3,4]:
#                     result_check = True
#                     result_msg = server_msg
#     
#                     
#             if self.result_check and self.trade_snapshot_check:
#                 return result_msg
#         # Listen for order confirmation
# =============================================================================
        
    @hearback
    def modify_order_request(self,  
                             order_id: int, # Get this from the previous Order 
                             orig_cl_order_id: str, 
                             cl_order_id: str, 
                             **kwargs) -> ServerMsg: # WIP
        default_kwargs = {'when_utc_timestamp': datetime.datetime.now(),
                          'qty': 0, 
                          'scaled_limit_price': None,
                          'scaled_stop_price': None,
                          'remove_activation_time': None,
                          'remove_suspension_utc_time': None,
                          'duration': None, 'good_thru_date': None,
                          'good_thru_utc_timestamp': None, 
                          'extra_attributes': None,
                          'sub_scope':1}
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

        return self._connect.client, client_msg
# =============================================================================
#         while True:
#             server_msg = self._connect.client.receive_server_message()
#             print("S_MSG", server_msg)
#                     
#             result_types = {"1": server_msg.order_statuses, 
#                             "2": server_msg.position_statuses, 
#                             "3": server_msg.collateral_statuses, 
#                             "4": server_msg.account_summary_statuses}
#     
#             if server_msg.trade_snapshot_completions is not None:
#                 trade_snapshot_check = True
#                                             
#             if len(result_types[str(sub_scope)]) >0: 
#                 print("======Result =============",)
#                 result_msg = server_msg
#                 result_check = True
#                 print("result", result_msg, result_types[str(sub_scope)])
#     
#                     
#             if result_check and trade_snapshot_check:
#                 #server_msg = client.receive_server_message()
#     
#                 return result_msg
# =============================================================================

    @hearback
    def cancel_order_request(self, 
                             order_id: int, 
                             orig_cl_order_id: str, 
                             cl_order_id: str,  
                             **kwargs) -> ServerMsg:
        default_kwargs = {'when_utc_timestamp': datetime.datetime.now(timezone.utc).timestamp()}
        #default_kwargs = {'when_utc_timestamp': datetime.datetime.now(timezone.utc)}
        kwargs = dict(default_kwargs, **kwargs)
        
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
# =============================================================================
#         # Check bool
#         status_check = False
#         trade_snapshot_check = False
#         result_check = False
#     
#         while True:
#             server_msg = self._connect.client.receive_server_message()
#             
#             result_types = {"1": server_msg.order_statuses, 
#                             "2": server_msg.position_statuses, 
#                             "3": server_msg.collateral_statuses, 
#                             "4": server_msg.account_summary_statuses}
#     
#             if server_msg.order_request_rejects is not None: # For catching error message
#                 trade_snapshot_check = True 
#             
#             if server_msg.order_statuses is not None:
#                 if len(server_msg.order_statuses)>0:
#                     print("recieved order_statues", len(server_msg.order_statuses))
#                     LIS = [server_msg.order_statuses[i].status 
#                            for i in range(len(server_msg.order_statuses))]
#                     print("LIS", LIS)
#                     LIS2 = [server_msg.order_statuses[i].order_id 
#                            for i in range(len(server_msg.order_statuses))]
#                     print("LIS2", LIS2)
#                     #print("TransactionStatus.Status.IN_CANCEL", TransactionStatus.Status.IN_CANCEL)
#                     match LIS[-1]:
#                         case Ord.OrderStatus.Status.IN_CANCEL:
#                             print("IN_CANCEL")
#                         case Ord.OrderStatus.Status.CANCELLED:
#                             print("CANCELLED")
#                             self.result_check = True
#                         case Ord.OrderStatus.Status.REJECTED:
#                             self.result_check = True
#                             print("REJECTED")
#                         
#     
#             if self.trade_snapshot_check and self.result_check:
#                 return order_request, server_msg
# =============================================================================
            
    @hearback
    def activate_order_request(self, 
                               order_id: int, 
                               orig_cl_order_id: str, 
                               cl_order_id: str, 
                               **kwargs) -> ServerMsg:
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
        return 
# =============================================================================
#         while True:
#             server_msg = self._connect.client.receive_server_message()
#                     
#             if server_msg.order_request_rejects is not None: # For catching error message
#                 self.trade_snapshot_check = True 
#     
#             if server_msg.order_statuses is not None:
#                 if len(server_msg.order_statuses)>0:
#                     print("recieved order_statues", len(server_msg.order_statuses))
#                     LIS = [server_msg.order_statuses[i].status 
#                            for i in range(len(server_msg.order_statuses))]
#                     print("LIS", LIS)
#                     LIS2 = [server_msg.order_statuses[i].order_id 
#                            for i in range(len(server_msg.order_statuses))]
#                     print("LIS2", LIS2)
#                     #print("TransactionStatus.Status.IN_CANCEL", TransactionStatus.Status.IN_CANCEL)
#                     match LIS[-1]:
#                         case Ord.OrderStatus.Status.SUSPENDED:
#                             print("SUSPENDED")
#                         case Ord.OrderStatus.Status.ACTIVEAT:
#                             print("ACTIVEAT")
#                             self.result_check = True
#                         case Ord.OrderStatus.Status.FILLED:
#                             self.result_check = True
#                             print("FILLED")
#                         
#     
#             if self.trade_snapshot_check and self.result_check:
#                 return order_request, server_msg
# =============================================================================
    @hearback
    def cancelall_order_request(self,
                                cl_order_id: str,
                                **kwargs)-> ServerMsg:
        default_kwargs = {'when_utc_timestamp': datetime.datetime.now(timezone.utc),
                          }
        kwargs = dict(default_kwargs, **kwargs)
        client_msg = ClientMsg()
        order_request = client_msg.order_requests.add()
        order_request.request_id = self.request_id
        order_request.cancel_all_orders.cl_order_id = cl_order_id
        order_request.cancel_all_orders.when_utc_timestamp = kwargs['when_utc_timestamp']
        self._connect.client.send_client_message(client_msg)

        return 
    
    @hearback
    def suspend_order_request(self,**kwargs)->ServerMsg: # SuspendOrder

        return 
    
    @hearback 
    def liquidateall_order_request(self, 
                                   contract_id,
                                   **kwargs) -> ServerMsg:
        default_kwargs = {'when_utc_timestamp': datetime.datetime.now(timezone.utc),
                          'is_short': None,
                          'current_day_only': None}
        kwargs = dict(default_kwargs, **kwargs)
        client_msg = ClientMsg()
        order_request = client_msg.order_requests.add()
        order_request.request_id = self.request_id
        
        account_position_filters = order_request.liquidate_all.account_position_filters.add()
        account_position_filters.account_id = self.account_id
        account_position_filters.contract_id = contract_id
        if kwargs['account_position_filters'] is not None:
            account_position_filters.is_short = kwargs['is_short']
        if kwargs['current_day_only'] is not None:
            account_position_filters.current_day_only = kwargs['current_day_only']
        
        order_request.liquidate_all.cl_order_id = cl_order_id
        order_request.liquidate_all.when_utc_timestamp = kwargs['when_utc_timestamp']
        
        self._connect.client.send_client_message(client_msg)

        return 

    @hearback
    def goflat_order_request(self, **kwargs) -> ServerMsg:
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
    
# =============================================================================
#         while True:
#             server_msg = self._connect.client.receive_server_message()
#             if server_msg.trade_snapshot_completions is not None:
#                 server_msg = self._connect.client.receive_server_message()
#                 break
#                 
#         return server_msg
# =============================================================================
    
    def send(self, 
             msg_id:int, 
             trade_subscription_id: int,
             symbol_name: str, 
             request_type: RequestType,
             request_details: dict,
             sub_scope = SUBSCRIPTION_SCOPE_ORDERS,
             **kwargs):
        
        # resolve symbol -> get CONTRACT_ID from Contractmetadata
        CONTRACT_METADATA = self._resolve_symbols(msg_id = msg_id, subscribe=None)
        CONTRACT_ID = CONTRACT_METADATA.contract_id

        # Trade Subscription 
        CONTRACT_ID = self._request_trade_subscription(trade_subscription_id,
                                                       subscribe = True,
                                                       sub_scope = sub_scope,
                                                       )
        
        match request_type:
            case RequestType.NEW_ORDER:
                # For new_order_request -> return OrderID
                ORDER_ID = self.new_order_request(CONTRACT_ID, **request_details)
            #contract_id: int, # Get this from trade_sub
            #cl_order_id: str, 
            #order_type: Ord.OrderType, 
            #duration: Ord.Duration, 
            #side: Ord.Side,
            #qty_significant:int, # make sure qty are in Decimal (int) not float
            #qty_exponent: int, 
            #is_manual: bool = False,
            #**kwargs) -> ServerMsg:
    
            case RequestType.MODIFY_ORDER:
                # For other oder_requests, use the OrderID from new_order_request
                self.modify_order_request(ORDER_ID, **request_details)
            
            case RequestType.CANCEL_ORDER:
                self.cancel_order_request(ORDER_ID, **request_details)
            
            case RequestType.ACRIVATE_ORDER:
                self.activate_order_request(ORDER_ID, **request_details)
            
            case RequestType.CANCELALL_ORDER:
                self.cancelall_order_request(**request_details)
                
            case RequestType.LIQUIDATEALL_ORDER:
                self.liquidateall_order_request(CONTRACT_ID, **request_details)
                
            case RequestType.GOFLAT_ORDER:
                self.goflat_order_request(**request_details)
                
        # Unsubscribe from trade subscription
        trade_server_msg_unsub = self._request_trade_subscription(trade_subscription_id,
                                            sub_scope=sub_scope,
                                            subscribe= False)

        return
    
# Usage: #############################################################
# payload_details =  { 
#                 "symbol_name": "CLEV25",
#                 "cl_order_id": "1231314",
#                 "order_type": ORDER_TYPE_LMT, 
#                 "duration": DURATION_GTC, 
#                 "side": SIDE_BUY,
#                 "qty_significant": 2, # make sure qty are in Decimal (int) not float
#                 "qty_exponent": 0, 
#                 "is_manual": bool = False,
#                 "scaled_limit_price": 1000,
#                 "good_thru_date": datetime.datetime(2025,9,9),
#                 "exec_instructions": EXEC_INSTRUCTION_AON
#                  }
#                       
# try:
#   CLOrder = CQGLiveOrder(connect: ConnectCQG, 
#                          symbol_name = payload_details['symbol_name'], 
#                          request_id =100, account_id = 000)
#   CLOrder.send(request_type=RequestType.NEW_ORDER, 
#                request_details = payload_details)
#
#
# Usage: #############################################################
# payload_details2 =  { 
#                 "symbol_name": "CLEV25",
#                 "order_id": ORDER_ID, # Get this from servermsg in new_order_request or in database
#                 "ogri_cl_order_id": "1231314",
#                 "cl_order_id": "1231315", # new cl_order_id
#                 "duration": DURATION_GTD, # Change from GTC to GTD
#                 "qty": 10, # change qty to from 2 to 10
#                 "scaled_limit_price": 1100, # change LMT proce from 1000 to 1100
#                  }
#                       
# try:
#   CLOrder = CQGLiveOrder(connect: ConnectCQG, 
#                          symbol_name = payload_details2['symbol_name'], 
#                          request_id =102, account_id = 000)
#   CLOrder.send(request_type=RequestType.MODIFY.ORDER, 
#                request_details = payload_details2)

