#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 09:34:29 2025

@author: dexter
"""
from typing import Protocol
    
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
    
