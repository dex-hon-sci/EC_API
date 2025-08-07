#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 10:23:04 2025

@author: dexter
"""
from collections import Protocol

from EC_API.ext.WebAPI.webapi_2_pb2 import ClientMsg, ServerMsg
from EC_API.ext.WebAPI import webapi_client
from EC_API.ext.WebAPI.user_session_2_pb2 import LogonResult, LoggedOff, Logon, \
                                       RestoreOrJoinSession, \
                                       RestoreOrJoinSessionResult

class Connect(Protocol):
    # Base class for websocket-like connection
    def __init__(self, 
                 host_name: str, 
                 user_name: str, 
                 password: str):
        self._host_name = host_name
        self._user_name = user_name
        self._password = password
        
        # Immediate connection
    
    @property
    def client(self):
        # return client connection object
        return self._client

    def logon():
        pass
    
    def logoff():
        pass
    
    def disconnect():
        pass
        
class ConnectCQG(object):
    # This class control all the functions related to connecting to CQG and 
    # subscriptions related functions
    
    def __init__(self, 
                 host_name: str, 
                 user_name: str, 
                 password: str):
        
        self._host_name = host_name
        self._user_name = user_name
        self._password = password
        
        # immediate connect to the server as we create the object
        self._client = webapi_client.WebApiClient()
        self._client.connect(self._host_name)
        
        self.session_token = None
        self.client_app_id = None
        self.protocol_version_major = None
        self.protocol_version_minor = None
        
    def client(self):
        # return client connection object
        return self._client

    def logon(self, 
              client_app_id: str ='WebApiTest', 
              client_version: str ='python-client-test-2-240',
              protocol_version_major: int = 2,
              protocol_version_minor: int = 240, 
              **kwargs) -> ServerMsg:
        
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
        
        if 'session_settings' in kwargs:
            logon.session_settings.append(kwargs['session_settings'])

        self._client.send_client_message(client_msg)
        
        server_msg = self._client.receive_server_message()
        if server_msg.logon_result.result_code == LogonResult.ResultCode.RESULT_CODE_SUCCESS:
            
            self.session_token = server_msg.logon_result.session_token
            self.client_app_id = client_app_id
            self.client_version = client_version
            self.protocol_version_major = protocol_version_major
            self.protocol_version_minor = protocol_version_minor
            
            print("Logon Successful")
            return server_msg.logon_result.base_time
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
        return server_msg
            
    def restore_request(self, session_token: str = None) -> ServerMsg:
        # Restore request taken from class attributes
        restore_msg = ClientMsg()
        restore_request = restore_msg.restore_or_join_session 
        restore_request.client_app_id = self.client_app_id
        restore_request.protocol_version_minor = self.protocol_version_major
        restore_request.protocol_version_major = self.protocol_version_minor
        
        if session_token is None:
            restore_request.session_token = self.session_token
        else:
            restore_request.session_token = session_token

        self._client.send_client_message(restore_msg)
        
        while True:
            server_msg_restore = self._client.receive_server_message()
            if len(server_msg_restore.restore_or_join_session_result)>0:
                return server_msg_restore
            
    def pong():
        return 
    
    def resolve_symbol(self, 
                       symbol_name: str, 
                       msg_id: int, 
                       subscribe: bool=None, **kwargs): #decrepated/unused
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
        
        self._client.send_client_message(client_msg)

        server_msg = self._client.receive_server_message()
        return server_msg.information_reports[0].symbol_resolution_report.contract_metadata
    
    def disconnect(self)->None:
        self._client.disconnect()
