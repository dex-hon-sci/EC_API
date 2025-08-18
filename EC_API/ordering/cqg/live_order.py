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
from EC_API.connect.cqg.connect import ConnectCQG
from EC_API.connect.hearback import hearback, get_contract_metadata
from EC_API.ordering.enums import (
    SubScope,
    OrderType,
    Duration,
    RequestType
    )
from EC_API.ordering.base import LiveOrder
from EC_API.utility.base import random_string

class CQGLiveOrder(LiveOrder):
    # a class that control the ordering action to the exchange
    # This object is specific for CQG type request
    def __init__(self, 
                 connect: ConnectCQG, 
                 symbol_name: str, 
                 request_id: int, 
                 account_id: int,
                 sub_scope: int = SubScope.SUBSCRIPTION_SCOPE_ORDERS,
                 msg_id: int = int(random_string(length=10)), # For symbol resolutions
                 trade_subscription_id: int = int(random_string(length=10)) # For trade_sub
                 ):
        
        self._connect = connect
        self._symbol_name = symbol_name
        self.request_id = request_id
        self.account_id = account_id
        self.sub_scope = sub_scope
        self.msg_id = msg_id # for information report
        self.trade_subscription_id = trade_subscription_id # for trade subscription
        self.auto_unsub = True

    @get_contract_metadata
    def _resolve_symbols(self, 
                         subscribe=None, 
                         **kwargs):
        client_msg = ClientMsg()
        information_request = client_msg.information_requests.add()
        information_request.id = self.msg_id
        if subscribe is not None:
            information_request.subscribe = subscribe
            
        information_request.symbol_resolution_request.symbol = self._symbol_name
        
        if 'instrument_group_request' in kwargs:
            information_request.instrument_group_request = kwargs['instrument_group_request']
        
        self._connect.client.client.send_client_message(client_msg)
        return 
    
    @hearback
    def _request_trade_subscription(self,
                                    subscribe: bool = True,
                                    skip_orders_snapshot: bool = False):
        
        client_msg = ClientMsg()
        trade_sub_request = client_msg.trade_subscriptions.add()
        trade_sub_request.id = self.trade_subscription_id
        trade_sub_request.subscribe = subscribe
        trade_sub_request.subscription_scopes.append(self.sub_scope)
        trade_sub_request.skip_orders_snapshot = skip_orders_snapshot
        #trade_sub_request.last_order_update_utc_timestamp = last_order_update_utc_timestamp
        
        if self.sub_scope == SubScope.SUBSCRIPTION_SCOPE_ACCOUNT_SUMMARY:
            account_summary_parameters = trade_sub_request.account_summary_parameters
            # 8 means purchasing_power, 15 means current_balance, 16 means profit_loss
            account_summary_parameters.requested_fields.extend([8,15,16])
            
        self._connect.client.send_client_message(client_msg)

        return 

    @hearback
    def new_order_request(self, 
                          contract_id: int = 0, # Get this from contractmetadata
                          cl_order_id: str = "", 
                          order_type: OrderType = OrderType.ORDER_TYPE_MKT, 
                          duration: Duration = Duration.DURATION_DAY, 
                          side: Ord.Side = None, # Delibrate choice here to return error msg if no side is provided
                          qty_significant: int = 0, # make sure qty are in Decimal (int) not float
                          qty_exponent: int = 0, 
                          is_manual: bool = False,
                          **kwargs) -> ServerMsg:
        
        
        default_kwargs = {
                 'when_utc_time': datetime.datetime.now(timezone.utc),
                 'exec_instructions': None,
                 'good_thru_date': None,
                 'scaled_limit_price': None,
                 'scaled_stop_price': None,
                 'extra_attributes': None,
                 'scaled_trail_offset': None,
                 'good_thru_utc_timestamp': None,
                 'suspend': None,
                 'algo_strategy': "CQG ARRIVALPRICE"
                 }
        merged_kwargs = {**default_kwargs, **kwargs}

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
        
        optional_kwargs_keys = [
            'good_thru_date',
            'scaled_limit_price',
            'scaled_stop_price',
            'when_utc_timestamp',
            'scaled_trail_offset',
            'good_thru_utc_timestamp',
            'suspend']
        
        for proto_field_name in optional_kwargs_keys:
            value = merged_kwargs.get(proto_field_name)
            if value is not None:
                setattr(order_request.new_order.order, proto_field_name, value)
                
        exec_instructions = merged_kwargs.get('exec_instructions')
        if exec_instructions:
            for instruction in exec_instructions:
                order_request.new_order.order.exec_instructions.append(instruction)
                
        order_request.new_order.order.algo_strategy = merged_kwargs['algo_strategy']
        
        extra_attributes_data = merged_kwargs.get('extra_attributes')
        if extra_attributes_data:
          for name, value in extra_attributes_data.items():
            extra_attribute = order_request.new_order.order.extra_attributes.add()
            extra_attribute.name = name
            extra_attribute.value = value    
        
        self._connect.client.send_client_message(client_msg)
        return self._connect.client, client_msg
        
    @hearback
    def modify_order_request(self,  
                             order_id: int = 0, # Get this from the previous Order 
                             orig_cl_order_id: str = "", 
                             cl_order_id: str = "", 
                             **kwargs) -> ServerMsg: # WIP
        default_kwargs = {
            'when_utc_timestamp': datetime.datetime.now(timezone.utc),
            'qty': None, 
            'scaled_limit_price': None,
            'scaled_stop_price': None,
            'remove_activation_time': None,
            'remove_suspension_utc_time': None,
            'duration': None, 
            'good_thru_date': None,
            'good_thru_utc_timestamp': None, 
            'activation_utc_timestamp': None,
            'extra_attributes': None,
            }
        
        kwargs = dict(default_kwargs, **kwargs)

        client_msg = ClientMsg()
        order_request = client_msg.order_requests.add()
        order_request.request_id = self.request_id
        order_request.modify_order.order_id = order_id
        order_request.modify_order.account_id = self.account_id
        order_request.modify_order.orig_cl_order_id = orig_cl_order_id
        order_request.modify_order.cl_order_id = cl_order_id
        order_request.modify_order.when_utc_timestamp = kwargs['when_utc_timestamp']
        
        optional_kwargs_keys = [
            'qty', 
            'scaled_limit_price', 
            'scaled_limit_price',
            'remove_activation_time', 
            'remove_suspension_utc_time', 
            'activation_utc_timestamp',
            'duration', 
            'good_thru_date', 
            'good_thru_utc_timestamp',
            'activation_utc_timestamp',
            'extra_attributes'
            ]
        
        for key in optional_kwargs_keys:
            if kwargs[key] is not None:
                setattr(order_request.modify_order, key, kwargs[key])
                
        extra_attributes_data = kwargs.get('extra_attributes')
        if extra_attributes_data:
          for name, value in extra_attributes_data.items():
            extra_attribute = order_request.new_order.order.extra_attributes.add()
            extra_attribute.name = name
            extra_attribute.value = value
        
        self._connect.client.send_client_message(client_msg)

        return self._connect.client, client_msg

    @hearback
    def cancel_order_request(self, 
                             order_id: int = 0, 
                             orig_cl_order_id: str = "", 
                             cl_order_id: str = "",  
                             **kwargs) -> ServerMsg:
        default_kwargs = {
            'when_utc_timestamp': datetime.datetime.now(timezone.utc).timestamp()
            }
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
        return
            
    @hearback
    def activate_order_request(self, 
                               order_id: int = 0, 
                               orig_cl_order_id: str = "", 
                               cl_order_id: str = "", 
                               **kwargs) -> ServerMsg:
        default_kwargs = {
            'when_utc_timestamp': datetime.datetime.now(timezone.utc),
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

    @hearback
    def cancelall_order_request(self,
                                cl_order_id: str = "",
                                **kwargs)-> ServerMsg:
        default_kwargs = {
            'when_utc_timestamp': datetime.datetime.now(timezone.utc),
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
    def suspend_order_request(self, **kwargs) -> ServerMsg: # SuspendOrder

        return 
    
    @hearback 
    def liquidateall_order_request(self, 
                                   contract_id: int = 0,
                                   cl_order_id: str = "",
                                   **kwargs) -> ServerMsg:
        default_kwargs = {
            'when_utc_timestamp': datetime.datetime.now(timezone.utc),
            'is_short': None,
            'current_day_only': None
            }
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
        default_kwargs = {
            'when_utc_timestamp': datetime.datetime.now(timezone.utc),
            'execution_source_code': None, 
            'speculation_type': None
            }
        kwargs = dict(default_kwargs, **kwargs)
    
        client_msg = ClientMsg()
        order_request = client_msg.order_requests.add()
        order_request.request_id = self.request_id
        order_request.go_flat.account_ids.append(self.account_id)
        order_request.go_flat.when_utc_timestamp = kwargs['when_utc_timestamp']
        #order_request.go_flat.execution_source_code = kwargs['execution_source_code']
        #order_request.go_flat.speculation_type = kwargs['speculation_type']
        self._connect.client.send_client_message(client_msg)
        
    
    def send(self, 
             request_type: RequestType,
             request_details: dict,
             **kwargs) -> None:
        
        # resolve symbol -> get CONTRACT_ID from Contractmetadata
        CONTRACT_METADATA = self._resolve_symbols(msg_id = self.msg_id, subscribe=None)
        CONTRACT_ID = CONTRACT_METADATA.contract_id

        # Trade Subscription 
        CONTRACT_ID = self._request_trade_subscription(self.trade_subscription_id,
                                                       subscribe = True,
                                                       sub_scope = self.sub_scope
                                                       )

        match request_type:
            case RequestType.NEW_ORDER:
                # For new_order_request -> return OrderID
                server_msg = self.new_order_request(CONTRACT_ID, 
                                                    **request_details)
            case RequestType.MODIFY_ORDER:
                # For other oder_requests, use the OrderID from new_order_request
                server_msg = self.modify_order_request(**request_details)
            
            case RequestType.CANCEL_ORDER:
                server_msg = self.cancel_order_request(**request_details)
            
            case RequestType.ACRIVATE_ORDER:
                server_msg = self.activate_order_request(**request_details)
            
            case RequestType.CANCELALL_ORDER:
                server_msg = self.cancelall_order_request(**request_details)
                
            case RequestType.LIQUIDATEALL_ORDER:
                server_msg = self.liquidateall_order_request(CONTRACT_ID, 
                                                             **request_details)
            case RequestType.GOFLAT_ORDER:
                server_msg = self.goflat_order_request(**request_details)
                
        if self.auto_unsub:
            # Unsubscribe from trade subscription
            unsub_trade_msg = self._request_trade_subscription(
                self.trade_subscription_id,
                subscribe = False,
                sub_scope =self.sub_scope
                )

        return server_msg
