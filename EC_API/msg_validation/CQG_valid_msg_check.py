#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  1 09:28:22 2025

@author: dexter
"""
from google.protobuf.descriptor import FieldDescriptor
from EC_API.ext.WebAPI.webapi_2_pb2 import ClientMsg, ServerMsg
from EC_API.msg_validation.base import ValidMsgCheck, MsgCheckPara
from EC_API.msg_validation.CQG_mapping import (
    MAP_STATUS_ENUMS, 
    MAP_RESPONSES_TYPES_STR,
    extract_result_code_from_server_msg,
    extract_special_clear_from_server_msg,
    extract_IDs_from_server_msg
    )


def get_CQG_msg_type(msg: ClientMsg|ServerMsg) ->\
                           tuple[list[str]|list[ClientMsg|ServerMsg]]:
    found_message_types = []
    found_message_values = []

    for field_descriptor, value in msg.ListFields():
        field_name = field_descriptor.name
    
        # For repeated fields, the value is a list. We check if the list
        # is not empty. ListFields() will only return the field if the
        # list has at least one element.
        if field_descriptor.label == FieldDescriptor.LABEL_REPEATED:
            if len(value) > 0:
                found_message_types.append(field_name)
                found_message_values.append(value)
        
        # For optional fields, ListFields() only returns the field
        # if it has been explicitly set.
        else:
            found_message_types.append(field_name)
            found_message_values.append(value)

    return (found_message_types, found_message_values)


class CQGValidMsgCheck(ValidMsgCheck, MsgCheckPara):
    # This class is in charge of validating serverresponse message 
    # AFTER sending a request is sent. 
    # It contains a set of checks that is required to resolve if 
    # we receive the correct set of responses from the server.
    
    # Check message types, map them to their corresponding set of enums
    # Check existence, 
    
    # then check msg types (existence) Tier1 (match request types)
    # match requestID first Tier2
    # Check specific markers (e.g., is_snapshot) Tier3

    def __init__(self, 
                 client_msg: ClientMsg, 
                 server_msg: ServerMsg):
        # Client/Server msg to cross match correct response types
        self.client_msg_types, self.client_msg_vals = get_CQG_msg_type(client_msg)
        self.server_msg_types, self.server_msg_vals = get_CQG_msg_type(server_msg)
    
    def expected_response_check(self):
        for client_msg_type, server_msg_type in zip(self.client_msg_types, 
                                                     self.server_msg_types):
            if server_msg_type in MAP_RESPONSES_TYPES_STR[client_msg_type]:
                self.recv_expected_msg = True
                
    def match_result_IDs_check(self):
        # Match request_id account_id contract_id cl_order_id
        pass

    def special_requirement_check(self):
        for server_msg_type, server_msg_val in zip(self.server_msg_types, 
                                                   self.server_msg_values):
            if extract_special_clear_from_server_msg(self.server_msg):
                self.recv_special_clear = True           
        
    def accept_status_check(self):
        # To check for accepted server_msg
        for server_msg_type, server_msg_val in zip(self.server_msg_types, 
                                                   self.server_msg_values):
            if extract_result_code_from_server_msg(self.server_msg) in \
               MAP_STATUS_ENUMS[server_msg_type]["Accept"]:
                self.recv_success_status = True
            
    def reject_status_check(self):
        # To check for recognised rejected server_msg
        for server_msg_type, server_msg_value in zip(self.server_msg_type, 
                                                     self.server_msg_values):
        # Find out the msg_type
            if extract_result_code_from_server_msg(self.server_msg) in \
               MAP_STATUS_ENUMS[server_msg_type]["Reject"]:
                self.recv_reject_status = True
            

    def check_all(self):
        # Check all condititions
        self.expected_response_check()
        self.match_result_IDs_chec()
        self.special_requirement_check()
        self.accept_status_check()
        self.reject_status_check()
        
    def return_msg(self):
        # Return message policy

        succes_msg_cond = (self.recv_expected_response and 
                           self.recv_match_IDs and 
                           self.recv_special_clear and 
                           self.recv_accept_status)
        fail_msg_cond = (self.recv_expected_response and 
                         self.recv_match_IDs and 
                         self.recv_special_clear and 
                         self.recv_reject_status)

        if succes_msg_cond:
            return self.server_msg
        elif fail_msg_cond:
            return self.server_msg
        else:
            pass

# Information report is_report_complete
# OrderStatus Enum, match OrderID, clorderid
