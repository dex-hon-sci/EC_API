#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 18 11:34:22 2025

@author: dexter
"""
import asyncio
from typing import Optional
from EC_API.ext.WebAPI.user_session_2_pb2 import LogonResult
from EC_API.ext.WebAPI.webapi_2_pb2 import ClientMsg, ServerMsg
from EC_API.ext.WebAPI import webapi_client
from EC_API.connect.base import Connect
from EC_API.connect.enums import ConnectionState
from EC_API.transport.base import Transport
from EC_API.transport.cqg.base import TransportCQG
from EC_API.transport.router import MessageRouter
from EC_API.protocol.cqg.mapping import cqg_mapping

from EC_API.connect.cqg.builders import (
    build_logon_msg, build_logoff_msg,
    build_ping_msg, build_resolve_symbol_msg,
    build_restore_msg
    )

Key = tuple[str, int]

def server_msg_type(msg: ServerMsg) -> str:
    return msg.WhichOneof("message")  # CQG oneof "message"

# Table-driven request_id extraction for RPC replies
def extract_router_key(msg: ServerMsg) -> Optional[Key]:
    mt = server_msg_type(msg)
    ...
# Streaming classifiers (examples)
def is_realtime_tick(msg: ServerMsg) -> bool:
    return server_msg_type(msg) == "real_time_market_data"

def is_order_update_stream(msg: ServerMsg) -> bool:
    # depending on CQG config you might get updates in trade_snapshot etc.
    return server_msg_type(msg) in {"order_statuses", "trade_snapshot"}

class ConnectCQG(Connect):
    # This class control all the functions related to connecting to CQG and 
    # subscriptions related functions
    def __init__(self, 
                 host_name: str, 
                 user_name: str, 
                 password: str,
                 immediate_connect: bool = True):
        # Inputs
        self._host_name = host_name
        self._user_name = user_name
        self._password = password
        
        self.session_token: str = None
        self.client_app_id: str = None
        self.protocol_version_major: int = None
        self.protocol_version_minor: int = None

        self._state: ConnectionState = ConnectionState.UNKNOWN
        self._task: Optional[asyncio.Task] = None

        self._msg_id = 10 # starting ID
        
        # Define client
        self._client = webapi_client.WebApiClient()
        self._loop = asyncio.get_running_loop()
        self._transport = TransportCQG()
        self._router = MessageRouter()
        
        # queues for 
        self._marketdata_queue = asyncio.Queue()
        self._exec_queue = asyncio.Queue()
        
        if immediate_connect:
            self._transport.connect()
            self._transport.start()
            self._router_task = asyncio.create_task(self._router_loop())
            #self._client.connect(self._host_name)
            
    # --- Internal -----------
    @property
    def client(self):
        # return client connection object
        return self._client
    
    @property
    def market_data_queue(self) -> asyncio.Queue: #[Tick]
        """Expose raw tick queue if some component wants direct consumption."""
        return self._market_data_q

    @property
    def exec_queue(self) -> asyncio.Queue: #[OrderUpdate]
        """Expose raw execution update queue."""
        return self._exec_q

    @property
    def transport(self) -> Transport:
        """Expose transport for advanced uses (e.g., custom messages)."""
        return self._transport
    
    def msg_id(self) -> int:
        self._msg_id += 1
        if self._msg_id > 2_000_000_000:
            self._msg_id = 1
        return self._msg_id
    # ------------------------
    
    # ---- Live cycle --------
    def start(self) -> None:
        self._transport.connect()
        self._transport.start()
        self._router_task = asyncio.create_task(self._router_loop())
        
    async def stop(self) -> None:
        self._stop_evt.set()
        try:
            self._transport.stop()
        finally:
            if self._task:
                self._task.cancel()
    # -----------------------
    async def connect(self) -> None:
        self._transport.connect()
    
    def disconnect(self)->None:
        self._client.disconnect()
        
    # -----------------------
    # ---- Router Loop ------
    async def _router_loop(self) -> None:
        while not self._stop_evt.is_set():
            pass
        
    async def _router_loop(self) -> None:
        while not self._stop_evt.is_set():
            msg: ServerMsg = await self._transport.recv()

            # 1) RPC routing (futures)
            key = extract_router_key(msg)
            if key is not None and self._router.on_message(key, msg):
                continue

            # 2) streaming dispatch
            if is_realtime_tick(msg):
                await self.tick_q.put(msg)
                continue

            if is_order_update_stream(msg):
                await self.exec_q.put(msg)
                continue

            await self.misc_q.put(msg)
    # -----------------------

    # RPC methods
    async def logon(self, 
        client_app_id: str ='WebApiTest', 
        client_version: str ='python-client-test-2-240',
        protocol_version_major: int = 2,
        protocol_version_minor: int = 240, 
        drop_concurrent_session: bool = False,
        private_label: str = "WebApiTest",
        **kwargs
        ) -> ServerMsg:
        
        
        client_msg = build_logon_msg(
            self._user_name, self._password,
            client_app_id=client_app_id,
            protocol_version_major= protocol_version_major,
            protocol_version_minor=protocol_version_minor,
            drop_concurrent_session = drop_concurrent_session,
            private_label = private_label,
            **kwargs
            )
        
        msg_key = ("logon_result", self.msg_id)
        #msg_key = ("user_session_statuses", self.msg_id)
        fut = self._router.register(msg_key)
        await self._transport.send(client_msg)
        return await asyncio.wait_for(fut, timeout=5.0)
        #status = cqg_session.parse_logon_status(reply)
        
    async def logoff(self) -> ServerMsg:
        # Logoff. Invoke this everytime when a connection is dropped
        client_msg = build_logoff_msg("logoff")
        
        msg_key = ("logoff_result", self.msg_id)
        fut = self._router.register(msg_key)
        await self._transport.send(client_msg)
        return await asyncio.wait_for(fut, timeout=5.0)
            
    async def restore_request(self, 
                              session_token: str = None, 
                              **kwargs) -> ServerMsg:
        # Restoring session after dropoff
        if session_token is None:
            session_token = self.session_token

        restore_msg = build_restore_msg(
            self.client_app_id, 
            self.protocol_version_major, 
            self.protocol_version_minor, 
            session_token,
            **kwargs)

        self._client.send_client_message(restore_msg)
        
        while True:
            server_msg_restore = self._client.receive_server_message()
            if len(server_msg_restore.restore_or_join_session_result)>0:
                return server_msg_restore
            
    async def ping(self):
        ping_msg = build_ping_msg(self.msg_id)
        ## Routing and transport
        return ping_msg

    # ------------------------
    
    # --- transport ----------       
# =============================================================================
#     async def _router_loop(self):
#         while True:
#             msg = await self._transport.recv()
#             msg_type = msg.WhichOneof("message")
#             
#             if cqg_mapping.is_symbol_resolution(msg):
#                 key = cqg_mapping.extract_router_key(msg)
#                 if key is not None:
#                     self._router.on_message(key, msg)
#             else:
#                 pass
#                 ### cases sit here or make an custom function
# =============================================================================

    # --- Symbol resolution ----------       
    async def resolve_symbol(self):
        pass
    
    async def resolve_symbol_async(self, 
                                   symbol_name: str, 
                                   msg_id: int, 
                                   subscribe: bool = None, 
                                   **kwargs)-> ServerMsg: #decrepated/unused
        # after the server confirm that we login successfully, we can send information_request
        # contains the symbol_resolution_request, the real time data, historical data, 
        # tick data, and order activities are all depended on symbol_resolution_report
        client_msg = build_resolve_symbol_msg(symbol_name, 
                                              self.msg_id, 
                                              subscribe=subscribe, 
                                              **kwargs)
        

        self._client.send_client_message(client_msg)
        while True:
            server_msg = self._client.receive_server_message()
            print("server_msg", server_msg)
            if len(server_msg.information_reports)>0:
                return server_msg.information_reports[0].symbol_resolution_report.contract_metadata
            asyncio.sleep(0.1)
            
# =============================================================================
#         # create a client_msg based on the protocol.
#         client_msg = ClientMsg()
#         
#         # initialize the logon message, there are four required parameters.
#         logon = client_msg.logon
#         logon.user_name = self._user_name
#         logon.password = self._password
#         logon.client_app_id = client_app_id
#         logon.client_version = client_version
#         logon.protocol_version_major = protocol_version_major
#         logon.protocol_version_minor = protocol_version_minor
#         logon.drop_concurrent_session = drop_concurrent_session
#         logon.private_label = private_label
# 
#         if 'session_settings' in kwargs:
#             logon.session_settings.append(kwargs['session_settings'])
# =============================================================================
# =============================================================================
# 
#         self._client.send_client_message(client_msg)
#         
#         server_msg = self._client.receive_server_message()
#         if server_msg.logon_result.result_code == LogonResult.ResultCode.RESULT_CODE_SUCCESS:
#             
#             # Save successful Logon information
#             self.session_token = server_msg.logon_result.session_token
#             self.client_app_id = client_app_id
#             self.client_version = client_version
#             self.protocol_version_major = protocol_version_major
#             self.protocol_version_minor = protocol_version_minor
#             
#             print("Logon Successful")
#             return server_msg
#         
#         else:
#             # the text_message contains the reason why user cannot login.
#             raise Exception("Can't login: " + server_msg.logon_result.text_message)
# 
# =============================================================================
# =============================================================================
#         client_msg = ClientMsg()
#         logoff = client_msg.logoff
#         logoff.text_message = "logoff test"
# =============================================================================
# =============================================================================
#         # Restore request taken from class attributes
#         restore_msg = ClientMsg()
#         restore_request = restore_msg.restore_or_join_session 
#         restore_request.client_app_id = self.client_app_id
#         restore_request.protocol_version_minor = self.protocol_version_major
#         restore_request.protocol_version_major = self.protocol_version_minor
#         
# =============================================================================

# =============================================================================
#         client_msg = ClientMsg()
#         information_request = client_msg.information_requests.add()
#         
#         # This example assume one symbol only.
#         information_request.id = msg_id
#         if subscribe is not None:
#             information_request.subscribe = subscribe
#             
#         information_request.symbol_resolution_request.symbol = symbol_name
#         
#         if 'instrument_group_request' in kwargs:
#             information_request.instrument_group_request = kwargs['instrument_group_request']    
#         print("resolve_sym_client_msg", client_msg)
# =============================================================================
