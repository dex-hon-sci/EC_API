#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 18 11:34:22 2025

@author: dexter
"""
import asyncio
from typing import Optional
import logging

from EC_API.ext.WebAPI import webapi_client
from EC_API.connect.base import Connect
from EC_API.connect.enums import ConnectionState
from EC_API.transport.base import Transport
from EC_API.transport.cqg.base import TransportCQG
from EC_API.transport.routers import MessageRouter, StreamRouter
from EC_API.protocol.cqg.router_util import (
        extract_router_keys, 
        server_msg_type,
        is_realtime_tick, 
        is_order_update_stream, 
        is_trade_history,
        realtime_tick_contract_id, 
        order_statuses_order_id,
        split_server_msg
    )
from EC_API.connect.cqg.builders import (
    build_logon_msg, build_logoff_msg,
    build_ping_msg, build_resolve_symbol_msg,
    build_restore_msg
    )
from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg # remove this once parser functions are done

logger = logging.getLogger(__name__)

def dispatcher(msg_types: list[str]):...

class ConnectCQG(Connect):
    # This class control all the functions related to connecting to CQG and 
    # subscriptions related functions
    def __init__(
            self, 
            host_name: str, 
            user_name: str, 
            password: str,
            immediate_connect: bool = True,
            client: None = None
        ):
        # Inputs
        self._host_name = host_name
        self._user_name = user_name
        self._password = password
        
        self._client = client
        
        self.session_token: str = None
        self.client_app_id: str = None
        self.protocol_version_major: int = None
        self.protocol_version_minor: int = None

        # State Control
        self.state: ConnectionState = ConnectionState.UNKNOWN
        self._task: Optional[asyncio.Task] = None
        
        # Generic Message parameter
        self._rid = 10 # starting request ID
        
        # Define client
        self._client = webapi_client.WebApiClient() if client is None else client
        self._loop = asyncio.get_running_loop()
        self._transport = TransportCQG(self._host_name,
                                       loop = self._loop, 
                                       client=self._client
                                       )
        
        # Routers. Use queues inside for message storage
        self._msg_router = MessageRouter()
        self._mkt_data_stream_router = StreamRouter()
        self._exec_stream_router = StreamRouter()
        
        # queues for containing different server messages
        self._misc_queue: asyncio.Queue = asyncio.Queue() # For information report?
        self._stop_evt = asyncio.Event()
        self._timeout = 1
        
        if immediate_connect:
            self._transport.connect()
            self._transport.start()
            self._router_task = asyncio.create_task(self._router_loop())
            
    def rid(self) -> int: # request
        self._rid += 1
        if self._rid > 2_000_000_000: # Hard limit set by CQG
            self._rid = 1
        return self._rid
            
    # ---- Internal Getter Methods ----
    @property
    def client(self):
        # return client connection object
        return self._client
    
    @property
    def transport(self) -> Transport:
        return self._transport
    # ------------------------
    
    async def connect(self) -> None:
       self._transport.connect()
    
    def disconnect(self)->None:
       self._client.disconnect()
    # -----------------------
    
    # ---- Live cycle --------
    def start(self) -> None:
        self._transport.connect()
        self._transport.start()
        self._router_task = asyncio.create_task(self._router_loop())
        print("stopevt is set", self._stop_evt.is_set())

    async def stop(self) -> None:
        self._stop_evt.set()
        try:
            self._transport.stop()
        finally:
            if self._task: # <---- Need to clarify this part
                self._task.cancel()

    # ---- Router Loop ------        
    async def _router_loop(self) -> None:

        while not self._stop_evt.is_set():
            msg: ServerMsg = await self._transport.recv()
            
            # 0) check if it is a composite message then SLIT!!
            top_unique_fields = server_msg_type(msg)
            if len(top_unique_fields)>1:
                msgs = split_server_msg(msg, top_unique_fields)
            else:
                msgs = [msg]

            for msg in msgs:
                # Cheapest check first, 
                # 1) streaming dispatch
                if is_realtime_tick(msg):
                    contract_id = realtime_tick_contract_id(msg)
                    await self._mkt_data_stream_router.publish(contract_id, msg)
                    continue
    
                # 2) order update dispatch <--need to handle this better
                if is_order_update_stream(msg):
                    order_id = order_statuses_order_id(msg)
                    await self._exec_stream_router.publish(order_id, msg)
                    continue
    
                keys = extract_router_keys(msg)
                if len(keys) >1:
                    print("multiple keys:", keys)
                for key in keys:
                    if key is not None:        
                        key_type, msg_type, msg_id_type, msg_id = key
                        # 3) RPC routing (futures), 
                        if key_type in {"rpc_reqid", "session", "sub", "info"}:
                            self._msg_router.on_message(key, msg)
                            #await self._misc_queue.put(msg)
             
    # ---- CQG messages methods ----
    async def logon(
        self, 
        client_app_id: str ='WebApiTest', 
        client_version: str ='python-client-test-2-240',
        protocol_version_major: int = 2,
        protocol_version_minor: int = 240, 
        drop_concurrent_session: bool = False,
        private_label: str = "WebApiTest",
        **kwargs
        ) -> ServerMsg | None:
        
        
        client_msg = build_logon_msg(
            self._user_name, self._password,
            client_app_id=client_app_id,
            protocol_version_major= protocol_version_major,
            protocol_version_minor=protocol_version_minor,
            drop_concurrent_session = drop_concurrent_session,
            private_label = private_label,
            **kwargs
            )
        if not client_msg:
            return
        
        msg_key = ('session', 'logon_result', 'single', 0)
        fut = self._msg_router.register_key(msg_key)
        await self._transport.send(client_msg)
        return await asyncio.wait_for(fut, timeout = self._timeout)
        #status = cqg_session.parse_logon_status(reply)
        
    async def logoff(self) -> ServerMsg | None:
        # Logoff. Invoke this everytime when a connection is dropped
        client_msg = build_logoff_msg("logoff")
        if not client_msg:
            return

        msg_key = ('session', 'logged_off', 'single', 0)
        fut = self._msg_router.register_key(msg_key)
        await self._transport.send(client_msg)
        return await asyncio.wait_for(fut, timeout = self._timeout)
            
    async def restore_request(
            self, 
            session_token: str = None, 
            **kwargs
        ) -> ServerMsg | None:
        # Restoring session after dropoff
        if session_token is None:
            session_token = self.session_token

        restore_msg = build_restore_msg(
            self.client_app_id, 
            self.protocol_version_major, 
            self.protocol_version_minor, 
            session_token,
            **kwargs)
        if not restore_msg:
            return

        msg_key = ('session', 'restore_or_join_session_result', 'single', 0)
        fut = self._msg_router.register_key(msg_key)
        await self._transport.send(restore_msg)
        return await asyncio.wait_for(fut, timeout=5.0)

    async def ping(self) -> ServerMsg | None:
        ping_msg = build_ping_msg(self.msg_id)
        if not ping_msg:
            return

        msg_key =  ('session', 'pong', 'single', 0)

        fut = self._msg_router.register_key(msg_key)
        return ping_msg
    
    async def resolve_symbol( # decrapated
        self, 
        symbol_name: str, 
        msg_id: int, 
        subscribe: bool = None, 
        **kwargs
        )-> ServerMsg: #decrepated/unused
        # after the server confirm that we login successfully, we can send information_request
        # contains the symbol_resolution_request, the real time data, historical data, 
        # tick data, and order activities are all depended on symbol_resolution_report
        client_msg = build_resolve_symbol_msg(
            symbol_name, 
                                              self.msg_id, 
                                              subscribe=subscribe, 
                                              **kwargs)
        if not client_msg:
            return 
        

        self._client.send_client_message(client_msg)
        while True:
            server_msg = self._client.receive_server_message()
            print("server_msg", server_msg)
            if len(server_msg.information_reports)>0:
                return server_msg.information_reports[0].symbol_resolution_report.contract_metadata
            asyncio.sleep(0.1)
            
