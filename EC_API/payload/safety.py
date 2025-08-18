#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 11 20:40:59 2025

@author: dexter
"""
from typing import Protocol, Any
from ..ordering.enums import RequestType

def isnot_null(reference_dict: dict[str, Any], 
               target_dict: dict[str, Any]) -> None:
    # Return nothing if value exist in target_dict, else raise key error
    for key in list(reference_dict.keys()):
        if target_dict.get(key) is None:
            raise KeyError(f"Essential parameter(s): {key} is missing.")
            
def is_correct_type(reference_dict: dict[str, Any], 
                    target_dict: dict[str, Any]) -> None:
    # Return nothing if type exist in target_dict, else raise key error
    for key in reference_dict:
        #print(type(target_dict[key]), reference_dict[key])
        if type(target_dict[key]) != reference_dict[key]:
            raise TypeError(f"Type Error, {key} must be: {reference_dict[key].__name__}.")
            
class PayloadFormatCheck(Protocol):
    """
    Protocol class for checking Payload formats.
    """
    def __init__(self,                  
                 order_request_type: RequestType, 
                 order_info: dict):

        self.order_request_type = order_request_type
        self.order_info = order_info
        
    def check_crendential(self):
        """
        Run null and type check on the global fields.
        """
        pass
    
    def check_request_specific_fields(self):
        """
        Run null, type, attr checks on request specific fields.
        """
        pass
    
    def check_order_specific_essential_fields(self):
        """
        Run null and type checks on order specific fields.
        """
        pass
    
    def check_valid_value(self):
        """
        Run checks to see if the input values are within the safety range.
        """
        pass
        
    def run(self):
        """
        Run all checks.
        """
        pass
