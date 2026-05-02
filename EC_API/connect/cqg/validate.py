#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 22:55:03 2026

@author: dexter
"""
from typing import Any

def validate_required_fields(
        params: dict[str, Any], 
        required_fields: dict[str, Any]
    ) -> None:
    # to check if the input in params has all the entries in the required_fields
    for field in required_fields:
        if field not in list(params.keys()):
            raise KeyError(f"{field} is required and not found in input.")
        
        
def valudate_logon_input_para(msg_info: dict[str, Any]) -> None:...
    
def validate_sym_res_input_para(msg_info: dict[str, Any]) -> None:
    if msg_info.get('preferred_types') is not None:
        ml: list[str] = msg_info['preferred_types'].replace(" ","").split(",")
        for ele in ml:
            if ele not in ("F","C","P","S","T","U","X"):
                raise ValueError(
                    'Field: preferred_types must be one of the\
                    following: ("F","C","P","S","T","U","X").')
                    
    if msg_info.get("preferred_countries") is not None:
        mll: list[str] = msg_info['preferred_countries'].replace(" ","").split(",")
        ...
