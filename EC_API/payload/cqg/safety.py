#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 11 16:32:09 2025

@author: dexter
"""
import datetime
from EC_API.ordering.enums import RequestType
from EC_API.payload.safety import (
    PayloadFormatCheck, 
    isnot_null, 
    is_correct_type
    )
from EC_API.ordering.enums import (
    Side, 
    Duration, 
    OrderType,
    ExecInstruction
    )

ASSETS_SAFETY_RANGE = {
    "CLE": {'scaled_limit_price': {'upper_limit': 10000, 
                                   'lower_limit': 100},
            'scaled_stop_price': {'upper_limit': 15000,
                                  'lower_limit': 100},
            'qty': {'upper_limit': 10,
                    'lower_limit': 1},
            'qty_significant': {'upper_limit': 9,
                                'lower_limit': 1},
            'qty_exponent': {'upper_limit': 1,
                             'lower_limit': 0},
            },
    "HOE": {}
    } # example dict # Need to make a control function for this

class CQGFormatCheck(PayloadFormatCheck):
    """
    A class that checks if the Parameters in the Payload object conform to 
    the CQG standatrd.
    """
    def __init__(self, 
                 order_request_type: RequestType, 
                 order_info: dict):
        self.order_request_type = order_request_type
        self.order_info = order_info
        self.asset_safty_range: dict = ASSETS_SAFETY_RANGE
        
    def check_crendential(self) -> None:
        credential_essentials_field_types = {
            "symbol_name": str,
            }
        isnot_null(credential_essentials_field_types, self.order_info)
        is_correct_type(credential_essentials_field_types, self.order_info)
        
    def check_request_specific_fields(self) -> None:
        # Check if the fields are valid for a specific request type 
        match self.order_request_type:
            case RequestType.NEW_ORDER:
                acceptable_request_specific_fields = {
                    "symbol_name": str,
                    'cl_order_id': str, 
                    "order_type": OrderType,
                    "duration": Duration,
                    "side": Side,
                    "qty_significant": int,
                    "qty_exponent": int,
                    "is_manual": bool,
                    "exec_instructions": ExecInstruction, 
                    "good_thru_date": datetime.datetime,
                    "scaled_limit_price": int,
                    "scaled_stop_price": int,
                    'extra_attributes': dict,
                    'scaled_trail_offset': int,
                    'suspend': bool,
                    'algo_strategy': str,
                    }
                
                essentials_request_specific_field_types = {
                    'cl_order_id': str, 
                    'order_type': OrderType, 
                    'duration': Duration,
                    'side': Side, 
                    'qty_significant': int,
                    }
                
                isnot_null(essentials_request_specific_field_types, 
                           self.order_info) # Null checks
                is_correct_type(essentials_request_specific_field_types, 
                                self.order_info) # Type checks
                
            case RequestType.MODIFY_ORDER:
                # ORDER_ID, status is not filled
                acceptable_request_specific_fields = {
                    "symbol_name": str,
                    'orig_cl_order_id': str,
                    "cl_order_id": str, 
                    'when_utc_timestamp': datetime.datetime,
                    'qty': int, 
                    'scaled_limit_price': int,
                    'scaled_stop_price': int,
                    'remove_activation_time': bool,
                    'remove_suspension_utc_time': bool,
                    'duration': Duration, 
                    'good_thru_date': None,
                    'good_thru_utc_timestamp': datetime.datetime, 
                    'activation_utc_timestamp': datetime.datetime,
                    'extra_attributes': dict,
                    }
                
                essentials_request_specific_field_types = {
                    'orig_cl_order_id': str,
                    "cl_order_id": str, 
                    }
                
                isnot_null(essentials_request_specific_field_types, 
                           self.order_info) # Null checks
                is_correct_type(essentials_request_specific_field_types, 
                                self.order_info) # Type checks

            case RequestType.CANCEL_ORDER:
                # ORDER_ID, status is not filled
                acceptable_request_specific_fields = {
                    "symbol_name": str,
                    'orig_cl_order_id': str,
                    "cl_order_id": str, 
                    'when_utc_timestamp': int
                    }
                
                essentials_request_specific_field_types = {
                    'orig_cl_order_id': str,
                    "cl_order_id": str, 
                    }
                
                isnot_null(essentials_request_specific_field_types, 
                           self.order_info) # Null checks
                is_correct_type(essentials_request_specific_field_types, 
                                self.order_info) # Type checks

            case RequestType.ACTIVATE_ORDER:
                # ORDER_ID, status is suspend
                acceptable_request_specific_fields = {
                    "symbol_name": str,
                    'orig_cl_order_id': str,
                    "cl_order_id": str, 
                    'when_utc_timestamp': int
                    }
                
                essentials_request_specific_field_types = {
                    'orig_cl_order_id': str,
                    "cl_order_id": str, 
                    }
                
                isnot_null(essentials_request_specific_field_types, 
                           self.order_info) # Null checks
                is_correct_type(essentials_request_specific_field_types, 
                                self.order_info) # Type checks

            case RequestType.CANCELALL_ORDER:
                acceptable_request_specific_fields = {
                    "symbol_name": str,
                    'cl_order_id': str,
                    'when_utc_timestamp': int
                    }
                
                essentials_request_specific_field_types = {
                    "symbol_name": str,
                    "cl_order_id": str, 
                    }
                
                isnot_null(essentials_request_specific_field_types, 
                           self.order_info) # Null checks
                is_correct_type(essentials_request_specific_field_types, 
                                self.order_info) # Type checks

            case RequestType.LIQUIDATEALL_ORDER:
                acceptable_request_specific_fields = {
                    "symbol_name": str,
                    'when_utc_timestamp': datetime.datetime,
                    'is_short': bool,
                    'current_day_only': bool
                    }

            case RequestType.GOFLAT_ORDER:
                acceptable_request_specific_fields = {
                    "symbol_name": str,
                    'when_utc_timestamp': datetime.datetime,
                    'execution_source_code': bool, 
                    'speculation_type': bool
                    }

        for key in self.order_info:
            if key not in list(acceptable_request_specific_fields.keys()):
                raise AttributeError(f"{key} is not an acceptable field for {self.order_request_type} request.")
            elif key in list(acceptable_request_specific_fields.keys()):
                if type(self.order_info[key]) != acceptable_request_specific_fields[key]:
                    raise TypeError(f"Type Error, {key} must be: {acceptable_request_specific_fields[key].__name__}.")

                                     
    def check_order_specific_essential_fields(self) -> None:
        # This function check the essential fields for particular order options
        # Such as LMT order needs to have the field scaled_limit_price
        
        if self.order_info.get('order_type') is not None:
            # Specific requirements check
            LMT_order_field_types = {"scaled_limit_price": int}
            STP_order_field_types = {"scaled_stop_price": int}
            STL_order_field_types = {"scaled_limit_price": int,
                                     "scaled_stop_price": int}
    
            ## Order types check
            # For LMT orders
            if self.order_info['order_type'] is OrderType.ORDER_TYPE_LMT:
                isnot_null(LMT_order_field_types, self.order_info)
                is_correct_type(LMT_order_field_types, self.order_info)
                
            # For STP orders
            elif self.order_info['order_type'] is OrderType.ORDER_TYPE_STP: 
                isnot_null(STP_order_field_types, self.order_info)
                is_correct_type(STP_order_field_types, self.order_info)
    
            elif self.order_info['order_type'] is OrderType.ORDER_TYPE_STL:
                isnot_null(STL_order_field_types, self.order_info)
                is_correct_type(STL_order_field_types, self.order_info)
                    
        ### Duration GTD case check
        if self.order_info.get('duration') is not None:
            duration_GTD_field_types = {"good_thru_date": int}
    
            if self.order_info['duration'] is Duration.DURATION_GTD:
                isnot_null(duration_GTD_field_types, self.order_info)
                is_correct_type(duration_GTD_field_types, self.order_info)

                    
        ### Execution instruction case Check
        if self.order_info.get('exec_instructions') is not None:
            execution_Trail_field_types = {"scaled_trail_offset": int}
            if self.order_info['exec_instructions'] is\
                ExecInstruction.EXEC_INSTRUCTION_TRAIL:
                isnot_null(execution_Trail_field_types, self.order_info)
                is_correct_type(execution_Trail_field_types, self.order_info)

    def check_valid_value(self) -> None:
        # Check if the value entered is allowed by our safety parameters.  
        # Call the relevant dictionary that store all the safety prarmeters
        range_mapping = self.asset_safty_range[self.order_info['symbol_name'][:3]]
        
        for key in range_mapping:
            if self.order_info.get(key) is not None:
                up_bound = range_mapping[key]['upper_limit']
                low_bound = range_mapping[key]['lower_limit']
                if (self.order_info[key] > up_bound) or (self.order_info[key] < low_bound):
                        raise ValueError(f'{key} is outside of the allowed range: [{low_bound}, {up_bound}].')
    
    def run(self) -> None:
        self.check_crendential()
        self.check_request_specific_fields()
        self.check_order_specific_essential_fields()
        self.check_valid_value()
        

