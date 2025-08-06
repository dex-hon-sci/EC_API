#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 09:34:29 2025

@author: dexter
"""
from typing import Protocol

# =============================================================================
# @dataclass
# class MsgCheckPara:
#     # Separate ValidMsgCheck from MsgCheckPara in case of 
# 
#     recv_expected_response = False # Check for expected response types
#     recv_match_IDs = False
#     recv_special_clear = False
#     recv_accept_status = False # For checking succe state in status_code
#     recv_reject_status = False # For checking reject state in status_code
#     
# =============================================================================
    
class ValidMsgCheck(Protocol):
    # Interface for Valid msg checking in case we switch to a different
    # Market data service provider
    def __init__(self):
        self.recv_expected_response = False
        self.recv_match_IDs = False
        self.recv_special_clear = False
        self.recv_accept_status = False
        self.recv_reject_status = False
     
    def expected_response_check(self):
        pass
    
    def accept_status_check(self):
        pass
    
    def reject_status_check(self):
        pass
    
    def special_requirement_check(self):
        # Existence check for the correct message
        pass
    
    def check_all(self):
        pass
    
    def return_msg(self):
        pass
    
