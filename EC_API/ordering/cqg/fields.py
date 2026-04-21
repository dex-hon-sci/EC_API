#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 22 00:33:52 2025

@author: dexter
"""
from datetime import datetime
from typing import Union
# EC_API imports
from EC_API.ext.common.shared_1_pb2 import NamedValue # Throw this away later
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
from EC_API._typing import _FieldSpec

TRADE_SUBSCRIPTION_REQUIRED_FIELD: _FieldSpec = {
    'trade_subscription_id': ('trade_subscription_id', int, int),
    'sub_scope': ('sub_scope', Union[SubScope, SubScopeCQG], None), 
    'subscribe': ('subscribe', bool, None),
    'skip_orders_snapshot': ('skip_orders_snapshot', bool, None),
    }

NEW_ORDER_REQUIRED_FIELDS: _FieldSpec = {
    'account_id': ('account_id', int, int),
    'request_id': ('request_id', int, int),
    'contract_id': ('contract_id', int, int),
    'cl_order_id': ('cl_order_id', str, str), 
    'order_type': ('order_type', Union[OrderType, OrderTypeCQG], None), 
    'duration': ('duration', Union[Duration, DurationCQG], None),
    'side': ('side', Side, None),
    'qty_significant': ('qty_significant', int, int),
    'qty_exponent': ('qty_exponent', int, int), 
    'is_manual': ('is_manual', bool, None)
    }

NEW_ORDER_OPTIONAL_FIELDS: _FieldSpec = { #(key, type, transform_func)
    'when_utc_timestamp': ('when_utc_timestamp', datetime, None),
    'good_thru_date': ('good_thru_date', int, None),
    'scaled_limit_price': ('scaled_limit_price', int, None),
    'scaled_stop_price': ('scaled_stop_price', int, None),
    'scaled_trail_offset': ('scaled_trail_offset', int, None),
    'good_thru_utc_timestamp': ('good_thru_utc_timestamp', datetime, None),
    'exec_instructions': ('exec_instructions', Union[ExecInstruction, ExecInstructionCQG], None),
    'suspend': ('suspend', bool, None),
    "algo_strategy": ("algo_strategy", str, str)
    }

MODIFY_ORDER_REQUIRED_FIELDS: _FieldSpec = {
    'account_id': ('account_id', int, int),
    'request_id': ('request_id', int, int),
    'order_id': ('order_id', str, None),
    'orig_cl_order_id': ('orig_cl_order_id', str, str), 
    'cl_order_id': ('cl_order_id', str, str), 
    'when_utc_timestamp': ('when_utc_timestamp', datetime, None),
    }
    
MODIFY_ORDER_OPTIONAL_FIELDS: _FieldSpec = {
    'scaled_limit_price': ('scaled_limit_price', int, None), 
    'scaled_stop_price': ('scaled_stop_price', int, None),
    'qty': ('qty', int, None), # Sensitive fields only take exact types and no transform func
    'remove_activation_time': ('remove_activation_time', bool, None), 
    'remove_suspension_utc_time': ('remove_suspension_utc_time', bool, None), 
    'duration': ('duration', Union[Duration, DurationCQG], None), 
    'good_thru_date': ('good_thru_date', int, None), 
    'good_thru_utc_timestamp': ('good_thru_utc_timestamp', datetime, None),
    'activation_utc_timestamp': ('activation_utc_timestamp', datetime, None),
    'extra_attributes': ('extra_attributes', NamedValue, None)
    }


CANCEL_ORDER_REQUIRED_FIELDS: _FieldSpec = {
    'account_id': ('account_id', int, int),
    'request_id': ('request_id', int, int),
    'order_id': ('order_id', str, None),
    'orig_cl_order_id': ('orig_cl_order_id', str, str), 
    'cl_order_id': ('cl_order_id', str, str), 
    'when_utc_timestamp': ('when_utc_timestamp', datetime, None)
    }

CANCEL_ORDER_OPTIONAL_FIELDS: _FieldSpec = {}

ACTIVATE_ORDER_REQUIRED_FIELDS: _FieldSpec = {
    'account_id': ('account_id', int, int),
    'request_id': ('request_id', int, int),
    'order_id': ('order_id', str, None),
    'orig_cl_order_id': ('orig_cl_order_id', str, str), 
    'cl_order_id': ('cl_order_id', str, str), 
    'when_utc_timestamp': ('when_utc_timestamp', datetime, None)
    }

ACTIVATE_ORDER_OPTIONAL_FIELDS: _FieldSpec = {}

GOFLAT_ORDER_REQUIRED_FIELDS: _FieldSpec = {
    'account_id': ('account_id', int, int),
    'request_id': ('request_id', int, int),
    'when_utc_timestamp': ('when_utc_timestamp', datetime, None),
    }

GOFLAT_ORDER_OPTIONAL_FIELDS: _FieldSpec = {
    'execution_source_code': ('execution_source_code', str, str), 
    'speculation_type': ('speculation_type', int, int)    
    }
###########

CANCELALL_ORDER_REQUIRED_FIELDS: _FieldSpec = {
    'account_id': ('account_id', int, int),
    'request_id': ('request_id', int, int),
    'cl_order_id': ('cl_order_id', str, str), 
    'when_utc_timestamp': ('when_utc_timestamp', datetime, None)
    }

CANCELALL_ORDER_OPTIONAL_FIELDS: _FieldSpec = {
    'is_short': ('is_short', bool, None),
    'current_day_only': ('current_day_only', bool, None)
    }


LIQUIDATEALL_ORDER_REQUIRED_FIELDS: _FieldSpec = {
    'account_id': ('account_id', int, int),
    'request_id': ('request_id', int, int),
    'contract_id': ('contract_id', int, int),
    }

LIQUIDATEALL_ORDER_OPTIONAL_FIELDS: _FieldSpec = {
    'when_utc_timestamp': ('when_utc_timestamp', datetime, None),
    'is_short': ('is_short', bool, None),
    'current_day_only': ('current_day_only', bool, None)
    }


