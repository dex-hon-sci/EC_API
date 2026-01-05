#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 21 23:58:45 2025

@author: dexter
"""
from typing import Any
from EC_API.ordering.enums import OrderType, Duration, ExecInstruction

def validate_required_fields(
        params: dict[str, Any], 
        required_fields: dict[str, Any]
    ) -> None:
    # to check if the input in params has all the entries in the required_fields
    for field in required_fields:
     if field not in list(params.keys()):
         raise KeyError(f"{field} is required and not found in input.")
        
def validate_input_para(order_info: dict[str, Any]) -> None:
    if order_info.get('order_type') is not None:
        # Specific requirements check
        match order_info['order_type']:
            # For LMT orders
            case OrderType.LMT:
                if order_info.get("scaled_limit_price") is None:
                    raise TypeError("LMT order requires scaled_limit_price (int).")
                if not isinstance(order_info["scaled_limit_price"], int):
                    raise TypeError("scaled_limit_price must be int.")
                
            # For STP orders
            case OrderType.STP:  
            #self.order_info['order_type'] is OrderType.ORDER_TYPE_STP: 
                if order_info.get("scaled_stop_price") is None:
                    raise TypeError("STP order requires scaled_stop_price (int).")
                if not isinstance(order_info["scaled_stop_price"], int):
                    raise TypeError("scaled_stop_price must be int.")
    
            case OrderType.STL:
                for k in ("scaled_limit_price", "scaled_stop_price"):
                    if order_info.get(k) is None:
                        raise TypeError(f"STL order requires {k} (int).")
                    if not isinstance(order_info[k], int):
                        raise TypeError(f"{k} must be int.")
                    
    ### Duration GTD case check
    if order_info.get('duration') is not None:
        #duration_GTD_field_types = {"good_thru_date": int}

        if order_info['duration'] == Duration.GTD:
            if order_info.get('good_thru_date') is None:
                raise TypeError("Duration GTD requires good_thru_date (int)")
            if not isinstance(order_info['good_thru_date'], int):
                raise TypeError("good_thru_date must be int.")

                
    ### Execution instruction case Check
    if order_info.get('exec_instructions') is not None:
        #execution_Trail_field_types = {"scaled_trail_offset": int}
        if order_info['exec_instructions'] == ExecInstruction.TRAIL:
            if order_info.get("scaled_trail_offset") is None:
                raise TypeError("the field scaled_trail_offset cannot be empty.")
            if not isinstance(order_info["scaled_trail_offset"], int):
                raise TypeError("scaled_trail_offset must be int.")

