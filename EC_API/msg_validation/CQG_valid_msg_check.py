#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  1 09:28:22 2025

@author: dexter
"""
from EC_API.ext.WebAPI.webapi_2_pb2 import ClientMsg, ServerMsg
from EC_API.msg_validation.base import ValidMsgCheck, MsgCheckPara
from EC_API.msg_validation.mapping import MAP_STATUS_ENUMS
from google.protobuf.descriptor import FieldDescriptor


def get_CQG_servermsg_type(server_msg: ServerMsg) -> tuple[list[str]|list[ServerMsg]]:
    found_message_types = []
    found_message_values = []

    for field_descriptor, value in server_msg.ListFields():
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
        
        self.client_msg = client_msg
        # Get CQG servermsg type serves as an existence test
        self.msg_types, self.msg_values = get_CQG_servermsg_type(server_msg)
        
        
    def accept_status_check(self):
        # To check for accepted server_msg
        for msg_type, msg_value in zip(self.msg_types, self.msg_values):
        # Find out the msg_type
            if msg_value.result_code in MAP_STATUS_ENUMS[msg_type]["Accept"]:
                self.recv_success_status = True
                return self.server_msg
            
    def reject_status_check(self):
        # To check for recognised rejected server_msg
        for msg_type, msg_value in zip(self.msg_types, self.msg_values):
        # Find out the msg_type
            if msg_value.result_code in MAP_STATUS_ENUMS[msg_type]["Reject"]:
                self.recv_reject_status = True
                return self.server_msg
            
    def match_result_type_check(self):
        if self.server_msg.result_code == 1:
            self.recv_success_status = True
            return self.server_msg

    def match_result_IDs_check(self):
        # Match request_id account_id contract_id cl_order_id
        pass

    def special_requirement_check():
        pass


    def check_all(self):
        self.accept_status_check()
        self.reject_status_check()
        self.special_requirement_check()
        self.match_result_check()
        
        



#from google.protobuf import json_format
#json_string = json_format.MessageToJson(server_msg, indent=2)
#print(json_string)
