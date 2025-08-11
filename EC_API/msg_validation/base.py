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
     
    def expected_response_check(self)->None:
        """
        Check if server msg types matches the expected response of the sent 
        client msg type. 
        """
        pass
    
    def match_result_IDs_check(self) -> None:
        """
        Check if the server msg contains a (set of) matching IDs to the client
        msg.

        """
        pass
    
    def accept_status_check(self) -> None:
        """
        Check if the server msg contains a result_code/status_code that 
        suggest the request is accepted by the server.

        """
        pass
    
    def reject_status_check(self) -> None:
        """
        Check if the server msg contains a result_code/status_code that 
        suggest the request is rejected by the server.

        """
        pass
    
    def special_requirement_check(self) -> None:
        """
        Check if the server msg contains a special attribute that indicates
        the request was fully being responded to, e.g. is_report_complete = true.

        """
        pass
    
    def check_all(self) -> None:
        """
        Run all checks in this class sequentially.
        """
        pass
    
    def return_msg(self):
        """
        Return server msg based on some policy.
        
        Return
        ------
        Some server msg and/or websocket client object

        """
        pass
    
