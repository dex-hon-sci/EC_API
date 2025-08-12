#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 11 20:40:59 2025

@author: dexter
"""
from typing import Protcol, Any
from EC_API.ordering.enums import RequestType

def isnot_null(reference_dict: dict[str, Any], 
               target_dict: dict[str, Any]) -> None:
    # Return nothing if value exist in target_dict, else raise key error
    for key in list(reference_dict.keys()):
        if target_dict.get(key) is None:
            raise KeyError(f"Essential parameter(s): {key} is missing.")
            
def is_correct_type(reference_dict: dict[str, Any], 
                    target_dict: dict[str, Any]) -> None:
    # Return nothing if type exist in target_dict, else raise key error
    for key, value in reference_dict:
        if type(target_dict[key]) is not reference_dict[key]:
            raise TypeError(f"Type Error, {key} must be: {target_dict[key]}")
            
class PayloadFormatCheck(Protcol):
    """
    Protocol class for checking Payload formats
    """
    def __init__(self,                  
                 order_request_type: RequestType, 
                 order_info: dict):

        self.order_request_type = order_request_type
        self.order_info = order_info
        
    def check_crendential(self):
        """
        """
        pass
    
    def check_universal_essential_fields(self):
        """
        """

        pass
    
    def check_order_specific_essential_fields(self):
        """
        """

        pass
    
    def check_request_specific_essential_fields(self):
        """
        """

        pass
        
    def run(self):
        """
        """

        pass

