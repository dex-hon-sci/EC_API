#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 19 13:01:54 2025

@author: dexter
"""
from WebAPI.webapi_2_pb2 import ClientMsg
from WebAPI import webapi_client
from WebAPI.user_session_2_pb2 import LogonResult, LoggedOff, Logon, \
                                      RestoreOrJoinSession, RestoreOrJoinSessionResult

# input payload (ordering)
# input logon informations

# send order function
# A function that can take in live-data in a while loop and update orders based 
# on some predetermined rules.

class ConnectCQG(object):
    # This class control all the functions related to connecting to CQG and 
    # subscriptions related functions
    
    def __init__(self, 
                 host_name: str, 
                 user_name:str, 
                 password:str):
        
        self._host_name = host_name
        self._user_name = user_name
        self._password = password
        
        # immediate connect to the server as we create the object
        self._client = webapi_client.WebApiClient()
        self._client.connect(self._host_name)
        
    def client(self):
        # return client connection object
        return self._client

    def logon(self, 
              client_app_id: str ='WebApiTest', 
              client_version: str ='python-client-test-2-230',
              protocol_version_major: int=2,
              protocol_version_minor = 230):
        
        # create a client_msg based on the protocol.
        client_msg = ClientMsg()
        # initialize the logon message, there are four required parameters.
        logon = client_msg.logon
        logon.user_name = self._user_name
        logon.password = self._password
        logon.client_app_id = client_app_id
        logon.client_version = client_version
        logon.protocol_version_major = protocol_version_major
        logon.protocol_version_minor = protocol_version_minor
    
        # see send_client_message() function in webapi_client.py in line 23.
        self._client.send_client_message(client_msg)
        # see receive_server_message() function in webapi_client.py in line 33.
        server_msg = self._client.receive_server_message()
        if server_msg.logon_result.result_code == LogonResult.ResultCode.RESULT_CODE_SUCCESS:
            # in later samples, we will need to use base_time to complete the from_utc_time.
            # in the time_and_sales_request sample and the time_bar_request sample.
            print("Logon Successful")
            return server_msg.logon_result.base_time
            #return server_msg.logon_result.result_code #, LogonResult.ResultCode.__dict__['_enum_type'].__dict__['values_by_name']['RESULT_CODE_FAILURE'].__dict__
        else:
            # the text_message contains the reason why user cannot login.
            raise Exception("Can't login: " + server_msg.logon_result.text_message)

    def logoff(self):
        # Logoff. Invoke this everytime when a connection is dropped
        client_msg = ClientMsg()
        logoff = client_msg.logoff
        logoff.text_message = "logoff test"
        
        self._client.send_client_message(client_msg)
        server_msg = self._client.receive_server_message()
        if server_msg.logged_off:
            print("Logoff :)")
        if server_msg.logged_off.text_message:
            print("Logoff reason is: " + server_msg.logged_off.logoff_reason)
            
    def resolve_symbol(self, 
                       symbol_name: str, 
                       msg_id: int, 
                       subscribe: bool=None, **kwargs):
        # after the server confirm that we login successfully, we can send information_request
        # contains the symbol_resolution_request, the real time data, historical data, 
        # tick data, and order activities are all depended on symbol_resolution_report
        client_msg = ClientMsg()
        information_request = client_msg.information_requests.add()
        
        # This example assume one symbol only.
        information_request.id = msg_id
        if subscribe is not None:
            information_request.subscribe = subscribe
            
        information_request.symbol_resolution_request.symbol = symbol_name
        
        if 'instrument_group_request' in kwargs:
            information_request.instrument_group_request = kwargs['instrument_group_request']    
        if 'preferred_types' in kwargs:
            information_request.preferred_types = kwargs['preferred_types']
        
        self._client.send_client_message(client_msg)

        server_msg = self._client.receive_server_message()
        return server_msg.information_reports[0].symbol_resolution_report.contract_metadata
    
if __name__ == "__main__":
    import load_dotenv
    import os
    load_dotenv()
    host_name = os.environ.get("CQG_API_host_name_demo")
    user_name = os.environ.get("CQG_API_trade_demo_usrname")
    password = os.environ.get("CQG_API_trade_demo_pw")

    resolveSymbolName = 'ZUC'

    C = ConnectCQG(host_name, user_name, password)
    C.logon()
    C.logoff()