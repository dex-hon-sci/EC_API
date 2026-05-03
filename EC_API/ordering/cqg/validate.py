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
    # Specific requirement for parameters. It checks intra-dependent inputs.
    if order_info.get('order_type') is not None:
        # Specific requirements check
        match order_info['order_type']:
            case OrderType.MKT:
                if order_info.get("scaled_limit_price") is not None:
                    raise TypeError("MKT order does not require scaled_limit_price.")
                
                if order_info.get("scaled_stop_price") is not None:
                    raise TypeError("MKT order does not require scaled_stop_price.")

            # For LMT orders
            case OrderType.LMT:
                if order_info.get("scaled_limit_price") is None:
                    raise TypeError("LMT order requires scaled_limit_price (int).")
                
            # For STP orders
            case OrderType.STP:  
            #self.order_info['order_type'] is OrderType.ORDER_TYPE_STP: 
                if order_info.get("scaled_stop_price") is None:
                    raise TypeError("STP order requires scaled_stop_price (int).")
    
            case OrderType.STL:
                for k in ("scaled_limit_price", "scaled_stop_price"):
                    if order_info.get(k) is None:
                        raise TypeError(f"STL order requires {k} (int).")
                    
    ### Duration GTD case check
    if order_info.get('duration') is not None:
        #duration_GTD_field_types = {"good_thru_date": int}
        match order_info['duration']:
            case Duration.GTD:
                if order_info.get('good_thru_date') is None:
                    raise TypeError("Duration GTD requires good_thru_date (int).")
                    
            case Duration.FOK:
                if order_info.get('good_thru_date') is not None:
                    raise TypeError("Duration FOK does not requires good_thru_date.")

                
    ### Execution instruction case Check
    if order_info.get('exec_instructions') is not None:
        #execution_Trail_field_types = {"scaled_trail_offset": int}
        if order_info['exec_instructions'] == ExecInstruction.TRAIL:
            if order_info.get("scaled_trail_offset") is None:
                raise TypeError("the field scaled_trail_offset cannot be empty.")
    
    ### Value checks
    if order_info.get("qty_significant") is not None:
        if order_info["qty_significant"] <= 0:
            raise ValueError("qty_significant cannot be negative.")
            
    if order_info.get("qty_exponent") is not None:
        lower_limit, upper_limit = -5, 5
        if order_info["qty_exponent"] < lower_limit or \
           order_info["qty_exponent"] > upper_limit:
            raise ValueError(f"qty_exponent is outside of the range [{lower_limit}, {upper_limit}].")
    
    if order_info.get("scaled_stop_price") is not None:
        if order_info['scaled_stop_price'] <= 0:
            raise ValueError("scaled_stop_price cannot be negative.")

    if order_info.get("scaled_limit_price") is not None:
        if order_info["scaled_limit_price"] <= 0:
            raise ValueError("scaled_limit_price cannot be negative.")
