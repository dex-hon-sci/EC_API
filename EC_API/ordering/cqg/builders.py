#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 28 21:14:37 2025

@author: dexter
"""
from datetime import datetime, timezone
from EC_API.ext.WebAPI.order_2_pb2 import Order as Ord 
from EC_API.ext.WebAPI.webapi_2_pb2 import ClientMsg
from EC_API.ext.common.shared_1_pb2 import NamedValue
from EC_API.ordering.enums import (
    SubScope,
    OrderType,
    Duration,
    RequestType
    )


NEW_ORDER_OPTIONAL_FIELDS = {
    'good_thru_date': ('good_thru_date', int),
    'scaled_limit_price': ('scaled_limit_price', int),
    'scaled_stop_price': ('scaled_stop_price', int),
    'when_utc_timestamp': ('when_utc_timestamp', datetime),
    'scaled_trail_offset': ('scaled_trail_offset',),
    'good_thru_utc_timestamp': ('good_thru_utc_timestamp', datetime),
    'suspend': ('suspend', bool)
    }
    
MODIFY_ORDER_OPTIONAL_FIELDS = {
    'qty': ('qty', int), 
    'scaled_limit_price': ('scaled_limit_price', int), 
    'scaled_stop_price': ('scaled_stop_price', int),
    'remove_activation_time': ('remove_activation_time', bool), 
    'remove_suspension_utc_time': ('remove_suspension_utc_time', bool), 
    'activation_utc_timestamp': ('activation_utc_timestamp', datetime),
    'duration': ('duration', int), 
    'good_thru_date': ('good_thru_date', int), 
    'good_thru_utc_timestamp': ('good_thru_utc_timestamp', datetime),
    'activation_utc_timestamp': ('activation_utc_timestamp', datetime),
    'extra_attributes': ('extra_attributes', NamedValue)
    }

GOFLAT_ORDER_OPTIONAL_FIELDS = {
    'when_utc_timestamp': ('when_utc_timestamp', datetime),
    'execution_source_code': ('execution_source_code',), 
    'speculation_type': ('execution_source_code',)    
    }

def build_trade_subscription_msg(
    trade_subscription_id: int, 
    subscribe: bool,
    sub_scope: int,
    skip_orders_snapshot: bool
    ) -> ClientMsg:
    
    client_msg = ClientMsg()
    trade_sub_request = client_msg.trade_subscriptions.add()
    trade_sub_request.id = trade_subscription_id
    trade_sub_request.subscribe = subscribe
    trade_sub_request.subscription_scopes.append(sub_scope)
    trade_sub_request.skip_orders_snapshot = skip_orders_snapshot
    #trade_sub_request.last_order_update_utc_timestamp = last_order_update_utc_timestamp
    
    if sub_scope == SubScope.SUBSCRIPTION_SCOPE_ACCOUNT_SUMMARY:
        account_summary_parameters = trade_sub_request.account_summary_parameters
        # 8 means purchasing_power, 15 means current_balance, 16 means profit_loss
        account_summary_parameters.requested_fields.extend([8,15,16])
    return client_msg

def build_new_order_request_msg(
    account_id: int,
    request_id: int,
    contract_id: int = 0, # Get this from contractmetadata
    cl_order_id: str = "", 
    order_type: OrderType = OrderType.ORDER_TYPE_MKT, 
    duration: Duration = Duration.DURATION_DAY, 
    side: Ord.Side = None, # Delibrate choice here to return error msg if no side is provided
    qty_significant: int = 0, # make sure qty are in Decimal (int) not float
    qty_exponent: int = 0, 
    is_manual: bool = False,
    **kwargs
    ) -> ClientMsg:
    
    if side is None:
        raise ValueError("side is required")
        
    default_kwargs = {
             'when_utc_time': datetime.now(timezone.utc),
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
    order_request.request_id = request_id
    order_request.new_order.order.account_id = account_id
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
    
    return client_msg

def build_modify_order_request_msg(
        account_id: int, 
        request_id: int,
        order_id: int = 0, # Get this from the previous Order 
        orig_cl_order_id: str = "", 
        cl_order_id: str = "", 
        **kwargs
    ) -> ClientMsg:
    
    default_kwargs = {
        'when_utc_timestamp': datetime.now(timezone.utc),
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
    order_request.request_id = request_id
    order_request.modify_order.order_id = order_id
    order_request.modify_order.account_id = account_id
    order_request.modify_order.orig_cl_order_id = orig_cl_order_id
    order_request.modify_order.cl_order_id = cl_order_id
    order_request.modify_order.when_utc_timestamp = kwargs['when_utc_timestamp']
    
    optional_kwargs_keys = [
        'qty', 
        'scaled_limit_price', 
        'scaled_stop_price',
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
        extra_attribute = order_request.modify_order.extra_attributes.add()
        extra_attribute.name = name
        extra_attribute.value = value
        
    return client_msg
         

def build_cancel_order_request_msg(
    account_id: int, 
    request_id: int,
    order_id: int = 0, 
    orig_cl_order_id: str = "", 
    cl_order_id: str = "",  
    **kwargs
    ) -> ClientMsg:
    
    default_kwargs = {
        'when_utc_timestamp': datetime.now(timezone.utc).timestamp()
        }
    kwargs = dict(default_kwargs, **kwargs)
    
    client_msg = ClientMsg()
    order_request = client_msg.order_requests.add()
    order_request.request_id = request_id
    order_request.cancel_order.order_id = order_id
    order_request.cancel_order.account_id = account_id
    order_request.cancel_order.orig_cl_order_id = orig_cl_order_id
    order_request.cancel_order.cl_order_id = cl_order_id
    order_request.cancel_order.when_utc_timestamp = kwargs['when_utc_timestamp']
    return  client_msg
 

def build_cancelall_order_request_msg(
    account_id: int,
    request_id: int,
    cl_order_id: str = "",
    **kwargs
    )-> ClientMsg:
    default_kwargs = {
        'when_utc_timestamp': datetime.now(timezone.utc),
        }
    kwargs = dict(default_kwargs, **kwargs)
    
    client_msg = ClientMsg()
    order_request = client_msg.order_requests.add()
    order_request.request_id = request_id
    order_request.cancel_all_orders.cl_order_id = cl_order_id
    order_request.cancel_all_orders.when_utc_timestamp = kwargs['when_utc_timestamp']
    return client_msg
 
def build_suspend_order_request_msg() -> ClientMsg:
    return 

def build_activate_order_request_msg() -> ClientMsg:
    return 


def build_liquidateall_order_request_msg(
    account_id: int,
    request_id: int,
    contract_id: int = 0,
    cl_order_id: str = "",
    **kwargs
    ) -> ClientMsg:
    default_kwargs = {
        'when_utc_timestamp': datetime.now(timezone.utc),
        'is_short': None,
        'current_day_only': None
        }
    kwargs = dict(default_kwargs, **kwargs)
    
    client_msg = ClientMsg()
    order_request = client_msg.order_requests.add()
    order_request.request_id = request_id
    
    account_position_filters = order_request.liquidate_all.account_position_filters.add()
    account_position_filters.account_id = account_id
    account_position_filters.contract_id = contract_id
    
    if kwargs['account_position_filters'] is not None:
        account_position_filters.is_short = kwargs['is_short']
    if kwargs['current_day_only'] is not None:
        account_position_filters.current_day_only = kwargs['current_day_only']
    
    order_request.liquidate_all.cl_order_id = cl_order_id
    order_request.liquidate_all.when_utc_timestamp = kwargs['when_utc_timestamp']
    
    return client_msg
 

def build_goflat_order_request_msg(
    account_id: int,
    request_id: int,
    **kwargs
    ) -> ClientMsg:
    default_kwargs = {
        'when_utc_timestamp': datetime.now(timezone.utc),
        'execution_source_code': None, 
        'speculation_type': None
        }
    kwargs = dict(default_kwargs, **kwargs)

    client_msg = ClientMsg()
    order_request = client_msg.order_requests.add()
    order_request.request_id = request_id
    order_request.go_flat.account_ids.append(account_id)
    order_request.go_flat.when_utc_timestamp = kwargs['when_utc_timestamp']
 