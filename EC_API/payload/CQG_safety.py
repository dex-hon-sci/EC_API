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
from EC_API.ext.WebAPI.order_2_pb2 import Order as Ord 
from EC_API.WebAPI.trade_routing_2_pb2 import TradeSubscription as TS

ASSETS_SAFETY_RANGE = {
    "CLE": {'scaled_limit_price': {'upper_limit': 0, 
                                       'lower_limit': 0},
            'scaled_stop_price': {'upper_limit': 0,
                                  'lower_limit': 0},
            'qty': {'upper_limit': 10,
                    'lower_limit': 1},
            'qty_significant': {'upper_limit': 0,
                                'lower_limit': 0},
            '': {'upper_limit': 0,
                                'lower_limit': 0},
            }
    
    } # example dict

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
        # Check account_id
        #self._symbol_name = symbol_name
        #self.sub_scope = sub_scope
        credential_essentials_field_types = {
            "symbol_name": str,
            "sub_scope": TS.SubscriptionScope
            }
        isnot_null(credential_essentials_field_types, self.order_info)
        is_correct_type(credential_essentials_field_types, self.order_info)
        
    def check_global_essential_fields(self) -> None:
        # Check order request input formats for essential fields
        # Fields type, value check                
        global_essentials_field_types = {
            'contract_id': int, 
            'cl_order_id': str, 
            'duration': Ord.Duration,
            'order_type': Ord.OrderType, 
            'side': Ord.Side, 
            'qty_significant': int,
            }
        isnot_null(global_essentials_field_types, self.order_info) # Null checks
        is_correct_type(global_essentials_field_types, self.order_info) # Type checks

                                
    def check_order_specific_essential_fields(self) -> None:
        # This function check the essential fields for particular order options
        # Such as LMT order needs to have the field scaled_limit_price
        
        # Specific requirements check
        LMT_order_field_types = {"scaled_limit_price": int}
        STP_order_field_types = {"scaled_stop_price": int}
        STL_order_field_types = {"scaled_limit_price": int,
                                 "scaled_stop_price": int}

        ## Order types check
        # For LMT orders
        if self.order_info['order_type'] is Ord.OrderType.ORDER_TYPE_LMT:
            isnot_null(LMT_order_field_types, self.order_info)
            is_correct_type(LMT_order_field_types, self.order_info)
            
        # For STP orders
        elif self.order_info['order_type'] is Ord.OrderType.ORDER_TYPE_STP: 
            isnot_null(STP_order_field_types, self.order_info)
            is_correct_type(STP_order_field_types, self.order_info)

        elif self.order_info['order_type'] is Ord.OrderType.ORDER_TYPE_STL:
            isnot_null(STL_order_field_types, self.order_info)
            is_correct_type(STL_order_field_types, self.order_info)
                    
        ### Duration GTD case check
        duration_GTD_field_types = {"good_thru_date": int}

        if self.order_info['duration'] is Ord.Duration.GTD:
            isnot_null(duration_GTD_field_types, self.order_info)
            is_correct_type(duration_GTD_field_types, self.order_info)

                    
        ### Execution instruction case Check
        execution_Trail_field_types = {"scaled_trail_offset": int}
        if self.order_info['exec_instructions'] is\
            Ord.ExecInstruction.EXEC_INSTRUCTION_TRAIL:
            isnot_null(execution_Trail_field_types, self.order_info)
            is_correct_type(execution_Trail_field_types, self.order_info)
            
    
        
    def check_request_specific_fields(self) -> None:
        # Check if the fields are valid for a specific request type 
        match self.order_request_type:
            case RequestType.NEW_ORDER:
                
                pass
            
            case RequestType.MODIFY_ORDER:
                # ORDER_ID, status is not filled
                
                pass
            
            case RequestType.CANCEL_ORDER:
                # ORDER_ID, status is not filled

                pass
            
            case RequestType.ACRIVATE_ORDER:
                
                # ORDER_ID, status is suspend
                pass
            
            case RequestType.CANCELALL_ORDER:
                pass
            
            case RequestType.LIQUIDATEALL_ORDER:
                pass
            
            case RequestType.GOFLAT_ORDER:
                pass
            
    def check_valid_value(self) -> None:
        # Check if the value entered is allowed by our safety parameters.  
        
        # Call the relevant dictionary that store all the safety prarmeters
        range_mapping = self.asset_safty_range[self.order_info['symbol_name']]
        
        for key, value in range_mapping:
            if self.order_info.get(key) is not None:
                up_bound = range_mapping[key]['upper_limit']
                low_bound = range_mapping[key]['lower_limit']
                if (self.order_info[key] >= up_bound) or\
                   (self.order_info[key] <= low_bound):
                        raise ValueError(f'{key} is outside of the allowed range:\
                                         [{low_bound}, {up_bound}]')
    
    def run(self):
        self.check_crendential()
        self.check_global_essential_fields()
        self.check_order_specific_essential_fields()
        self.check_request_specific_fields()
        self.check_valid_value()
        
        optional_field_types = {  
            'when_utc_time': datetime.datetime,
            'exec_instructions': Ord.ExecInstruction,
            'good_thru_date': int,
            'scaled_limit_price': int,
            'scaled_stop_price': int,
            'extra_attributes': dict,
            'scaled_trail_offset': int,
            'suspend': bool,
            'algo_strategy': str,
            'remove_activation_time': bool,
            'remove_suspension_utc_time': bool,
            }
        

