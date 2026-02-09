#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 28 21:14:37 2025

@author: dexter
"""
from datetime import datetime, timezone
# EC_API imports
from EC_API.ext.WebAPI.webapi_2_pb2 import ClientMsg
from EC_API.ext.common.shared_1_pb2 import NamedValue # Throw this away later
from EC_API.utility.base import to_significand_sint64_exponent_sint32
from EC_API.ordering.cqg.validate import (
    validate_input_para, 
    validate_required_fields
    )
from EC_API.protocol.cqg.builder_util import (
    apply_optional_fields, 
    assert_input_types
    )
from EC_API.ordering.enums import (
    Side, SubScope,
    OrderType, Duration,
    ExecInstruction
    )
from EC_API.ordering.cqg.enums import (
    SubScopeCQG, OrderTypeCQG,
    DurationCQG,
    ExecInstructionCQG
    )
from EC_API.ordering.cqg.enum_mapping import (
    _SubScope_MAP_INT2CQG, _Side_MAP_INT2CQG, 
    _OrderType_MAP_INT2CQG, _Duration_MAP_INT2CQG, 
    _ExecInstruction_MAP_INT2CQG
    )
from EC_API.ordering.cqg.fields import (
    TRADE_SUBSCRIPTION_REQUIRED_FIELD,
    NEW_ORDER_REQUIRED_FIELDS,
    NEW_ORDER_OPTIONAL_FIELDS,
    MODIFY_ORDER_REQUIRED_FIELDS,
    MODIFY_ORDER_OPTIONAL_FIELDS,
    CANCEL_ORDER_REQUIRED_FIELDS,
    ACTIVATE_ORDER_REQUIRED_FIELDS,
    CANCELALL_ORDER_REQUIRED_FIELDS,
    CANCELALL_ORDER_OPTIONAL_FIELDS,
    LIQIDATEALL_ORDER_REQUIRED_FIELDS,
    LIQIDATEALL_ORDER_OPTIONL_FIELDS,
    GOFLAT_ORDER_REQUIRED_FIELDS,
    GOFLAT_ORDER_OPTIONAL_FIELDS
    )

# Make CANCELALL, LIQUIDATEALL, SUSPEND
def build_trade_subscription_msg(
    trade_subscription_id: int, 
    subscribe: bool,
    sub_scope: SubScope | SubScopeCQG,
    skip_orders_snapshot: bool    
    ) -> ClientMsg:
    
    params = locals().copy()
    assert_input_types(params, TRADE_SUBSCRIPTION_REQUIRED_FIELD)

    client_msg = ClientMsg()
    trade_sub_request = client_msg.trade_subscriptions.add()
    trade_sub_request.id = trade_subscription_id
    trade_sub_request.subscribe = subscribe
    trade_sub_request.subscription_scopes.append(_SubScope_MAP_INT2CQG[sub_scope])
    trade_sub_request.skip_orders_snapshot = skip_orders_snapshot
    #trade_sub_request.last_order_update_utc_timestamp = last_order_update_utc_timestamp
    
    if sub_scope == _SubScope_MAP_INT2CQG.get(sub_scope): # SUBSCRIPTION_SCOPE_ACCOUNT_SUMMARY
        account_summary_parameters = trade_sub_request.account_summary_parameters
        # 8 means purchasing_power, 15 means current_balance, 16 means profit_loss
        account_summary_parameters.requested_fields.extend([
            8, 15, 16])

    return client_msg

def build_new_order_request_msg(
    account_id: int,
    request_id: int,
    contract_id: int,
    cl_order_id: str, 
    side: Side, # Delibrate choice here to return error msg if no side is provided
    qty_significant: int, # make sure qty are in Decimal (int) not float
    qty_exponent: int, 
    order_type: OrderType | OrderTypeCQG = OrderType.MKT, 
    duration: Duration | DurationCQG = Duration.DAY, 
    is_manual: bool = False,
    **kwargs
    ) -> ClientMsg:
    
    defaults = {
    'exec_instructions': None,
    'good_thru_date': None,
    'scaled_limit_price': None, 
    'scaled_stop_price': None,
    'when_utc_timestamp': None,
    'suspend': None,
    'scaled_trail_offset' : None,
    'good_thru_utc_timestamp': None,
    'suspend': None,
    'algo_strategy': None
    }
    kwargs = dict(defaults, **kwargs)    
    params = locals().copy()
    params.pop('kwargs')
    params.pop('defaults')
    full = {**params, **kwargs}
    
    validate_required_fields(params, NEW_ORDER_REQUIRED_FIELDS)
    
    assert_input_types(params, NEW_ORDER_REQUIRED_FIELDS, strict = True)
    assert_input_types(kwargs, NEW_ORDER_OPTIONAL_FIELDS, strict = False)

    validate_input_para(full)
    
    client_msg = ClientMsg()
    order_requests = client_msg.order_requests.add()
    order_requests.request_id = request_id
    order_requests.new_order.order.account_id = account_id
    order_requests.new_order.order.contract_id = contract_id
    order_requests.new_order.order.cl_order_id = cl_order_id
    order_requests.new_order.order.order_type = _OrderType_MAP_INT2CQG[order_type]
    order_requests.new_order.order.duration = _Duration_MAP_INT2CQG[duration]
    order_requests.new_order.order.side = _Side_MAP_INT2CQG[side]
    order_requests.new_order.order.is_manual = is_manual
    
    order_requests.new_order.order.qty.significand = qty_significant
    order_requests.new_order.order.qty.exponent = qty_exponent

    if kwargs['exec_instructions'] is not None:
        order_requests.new_order.order.exec_instructions.append(
            _ExecInstruction_MAP_INT2CQG[kwargs['exec_instructions']]
            )
        kwargs.pop('exec_instructions')
    if kwargs['suspend'] is not None:
        order_requests.new_order.suspend = kwargs['suspend']
        kwargs.pop('suspend')
        
    apply_optional_fields(order_requests.new_order.order,
                          values=kwargs, 
                          spec=NEW_ORDER_OPTIONAL_FIELDS)
    return client_msg

def build_modify_order_request_msg(
    account_id: int, 
    request_id: int,
    order_id: str, # Get this from the previous Order 
    orig_cl_order_id: str, 
    cl_order_id: str, 
    when_utc_timestamp: datetime = datetime.now(timezone.utc),
    **kwargs
    ) -> ClientMsg:

    defaults = {
    'scaled_limit_price': None,
    'scaled_stop_price': None,
    'qty': None,
    'remove_activation_time': None,
    'remove_suspension_utc_time': None,
    'duration': None, 
    'good_thru_date': None,
    'good_thru_utc_timestamp': None, 
    'activation_utc_timestamp': None,
    'extra_attributes': None,
    }
    kwargs = dict(defaults, **kwargs)
    params = locals().copy()
    params.pop('kwargs')
    params.pop('defaults')
    full = {**params, **kwargs}

    validate_required_fields(params, MODIFY_ORDER_REQUIRED_FIELDS)

    assert_input_types(params, MODIFY_ORDER_REQUIRED_FIELDS, strict = True)
    assert_input_types(kwargs, MODIFY_ORDER_OPTIONAL_FIELDS, strict = False)

    validate_input_para(full)
    
    client_msg = ClientMsg()
    order_requests = client_msg.order_requests.add()
    order_requests.request_id = request_id
    order_requests.modify_order.order_id = order_id
    order_requests.modify_order.account_id = account_id
    order_requests.modify_order.orig_cl_order_id = orig_cl_order_id
    order_requests.modify_order.cl_order_id = cl_order_id
    order_requests.modify_order.when_utc_timestamp = when_utc_timestamp
    
    if kwargs['qty'] is not None:
        if kwargs['qty'] == 0:
            return 0.0, 0
        
        significand, exponent = to_significand_sint64_exponent_sint32(kwargs['qty'])
        order_requests.modify_order.qty.significand = int(significand)
        order_requests.modify_order.qty.exponent = int(exponent)
        kwargs.pop('qty')

    apply_optional_fields(order_requests.modify_order,
                          values=kwargs, 
                          spec=MODIFY_ORDER_OPTIONAL_FIELDS)
    
    if kwargs['extra_attributes'] is not None:
        order_requests.modify_order.extra_attributes.append(
            kwargs['extra_attributes'])

    return client_msg

def build_cancel_order_request_msg(
    account_id: int, 
    request_id: int,
    order_id: int, 
    orig_cl_order_id: str, 
    cl_order_id: str,
    when_utc_timestamp: datetime = datetime.now(timezone.utc)
    ) -> ClientMsg:
    
    params = locals().copy()
    
    validate_required_fields(params, CANCEL_ORDER_REQUIRED_FIELDS)
    assert_input_types(params, CANCEL_ORDER_REQUIRED_FIELDS, strict = True)

    client_msg = ClientMsg()
    order_requests = client_msg.order_requests.add()
    order_requests.request_id = request_id
    order_requests.cancel_order.order_id = order_id
    order_requests.cancel_order.account_id = account_id
    order_requests.cancel_order.orig_cl_order_id = orig_cl_order_id
    order_requests.cancel_order.cl_order_id = cl_order_id
    order_requests.cancel_order.when_utc_timestamp = when_utc_timestamp
    
    return  client_msg

def build_cancelall_order_request_msg(
    account_id: int,
    request_id: int,
    cl_order_id: str,
    **kwargs
    )-> ClientMsg:
    default_kwargs = {
        'when_utc_timestamp': datetime.now(timezone.utc),
        }
    kwargs = dict(default_kwargs, **kwargs)
    params = locals().copy()
    params.pop('kwargs')
    params.pop('defaults')
    
    validate_required_fields(params, CANCELALL_ORDER_REQUIRED_FIELDS)
    
    # ... to be worked on
    
    client_msg = ClientMsg()
    order_request = client_msg.order_requests.add()
    order_request.request_id = request_id
    order_request.cancel_all_orders.cl_order_id = cl_order_id
    order_request.cancel_all_orders.when_utc_timestamp = kwargs['when_utc_timestamp']
    return client_msg
 
def build_suspend_order_request_msg() -> ClientMsg:
    return 

def build_activate_order_request_msg(
    account_id: int,
    request_id: int, 
    order_id: str, 
    orig_cl_order_id: str, 
    cl_order_id: str,
    when_utc_timestamp: datetime,
    ) -> ClientMsg:

    params = locals().copy()
    
    validate_required_fields(params, ACTIVATE_ORDER_REQUIRED_FIELDS)
    assert_input_types(params, ACTIVATE_ORDER_REQUIRED_FIELDS, strict = True)

    client_msg = ClientMsg()
    order_request = client_msg.order_requests.add()
    order_request.request_id = request_id
    order_request.activate_order.order_id = order_id
    order_request.activate_order.account_id = account_id
    order_request.activate_order.orig_cl_order_id = orig_cl_order_id
    order_request.activate_order.cl_order_id = cl_order_id
    order_request.activate_order.when_utc_timestamp = when_utc_timestamp

    return client_msg

def build_goflat_order_request_msg(    
    account_id: int,
    request_id: int,
    when_utc_timestamp: datetime,
    **kwargs
    ) -> ClientMsg:    
    
    defaults = {
    #'when_utc_timestamp': None,
    'execution_source_code': None, 
    'speculation_type': None
    }
    kwargs = dict(defaults, **kwargs)
    params = locals().copy()
    params.pop('kwargs')
    params.pop('defaults')
    full = {**params, **kwargs}

    validate_required_fields(params, GOFLAT_ORDER_REQUIRED_FIELDS)

    assert_input_types(params, GOFLAT_ORDER_REQUIRED_FIELDS, strict = True)
    assert_input_types(kwargs, GOFLAT_ORDER_OPTIONAL_FIELDS, strict = False)

    validate_input_para(full)

    client_msg = ClientMsg()
    order_requests = client_msg.order_requests.add()
    order_requests.request_id = request_id
    order_requests.go_flat.account_ids.append(account_id)
    order_requests.go_flat.when_utc_timestamp = when_utc_timestamp
    
    apply_optional_fields(order_requests.go_flat,
                          values=kwargs, 
                          spec=GOFLAT_ORDER_OPTIONAL_FIELDS)

    #order_request.go_flat.when_utc_timestamp = kwargs['when_utc_timestamp']
    return client_msg

##############         
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
