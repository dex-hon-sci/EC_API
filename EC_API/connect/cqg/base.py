#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 18 11:34:22 2025

@author: dexter
"""
import asyncio
from typing import Optional, Any, Callable
import logging
from datetime import datetime, timezone

from EC_API.ext.WebAPI import webapi_client
from EC_API.connect.base import Connect
from EC_API.connect.enums import ConnectionState
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
from EC_API.connect.cqg.parsers import (
    parse_logon_result,
    parse_restore_or_join_session_result,
    parse_logged_off,
    parse_pong,
    parse_symbol_resolution_report
    )
from EC_API.connect.enums import CONNECT_STATES_LIFECYCLE
from EC_API.connect.cqg.enum_mapping import (
    CONN_LOGON_RESCODE_CQG2INT,
    CONN_RESTORE_RESCODE_CQG2INT, 
    CONN_LOGOFF_RESCODE_CQG2INT,
    )
from EC_API.utility.state_mgr import StateMgr
from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg
from EC_API.utility.error_handlers import msg_io_error_handler
from EC_API.exceptions import (
    TransportConnectError,
    TransportDisconnectError,
    ConnectRequestError,
    ConnectCancelledError,
    ConnectTimeOutError,
    MsgBuilderError,
    MsgParserError
    )
from EC_API._typing import (
    PongType,
    ContractMetaDataType
    )

logger = logging.getLogger(__name__)

class ConnectCQG(Connect):
    """
    """
    def __init__(
            self, 
            host_name: str, 
            user_name: str, 
            password: str,
            account_id: str = "",
            immediate_connect: bool = False,
            client: Optional[webapi_client.WebApiClient] = None
        ):
        # Inputs
        self._host_name = host_name
        self._user_name = user_name
        self._password = password
        self._account_id = account_id
                
        # Sessions para
        self.session_token: Optional[str] = None
        self.client_app_id: Optional[str] = None
        self.protocol_version_major: Optional[int] = None
        self.protocol_version_minor: Optional[int] = None
        
        # Event Loop
        self._router_task: Optional[asyncio.Task] = None
        self._stop_evt = asyncio.Event()
        self._timeout = 1 # make make this a ping based decision

        # State Control
        self._state_mgr = StateMgr(
            CONNECT_STATES_LIFECYCLE, 
            start = ConnectionState.UNKNOWN, 
            cur = ConnectionState.UNKNOWN,
            allowed_starts=[ConnectionState.UNKNOWN]
            )

        # Generic Message parameter
        self._rid = 10 # initial request ID
        
        # Define client and transport layer
        self._client = webapi_client.WebApiClient() if client is None else client
        self._loop = asyncio.get_running_loop()
        self._transport = TransportCQG(
            self._host_name,
            loop = self._loop, 
            client=self._client
            )
        
        # Routers. Use queues inside for message storage
        self._msg_router = MessageRouter()
        self._mkt_data_stream_router = StreamRouter()
        self._exec_stream_router = StreamRouter()
        
        # queues for containing different server messages
        self._misc_queue: asyncio.Queue = asyncio.Queue() # For information report?
        
        if immediate_connect:
            self.start()
            
    def rid(self) -> int: # request
        self._rid += 1
        if self._rid > 2_000_000_000: # Hard limit set by CQG
            self._rid = 1
        return self._rid
            
    # ---- Internal Getter Methods ----
    @property
    def state(self) -> ConnectionState:
        return self._state_mgr.cur
    
    @property
    def client(self):
        # return client connection object
        return self._client
    
    @property
    def transport(self) -> TransportCQG:
        return self._transport
    
    # ---- Live cycle --------
    def start(self) -> bool:
        if self.state not in (
                ConnectionState.UNKNOWN, 
                ConnectionState.DISCONNECTED
                ):
            logger.warning("Invalid state: %s to run start() function call.", self.state)
            return False
        
        if self.state == ConnectionState.UNKNOWN:
            self._state_mgr.transition_to(ConnectionState.CONNECTING)
        elif self.state == ConnectionState.DISCONNECTED:
            self._state_mgr.transition_to(ConnectionState.RECONNECTING)
        
        try: 
            self._transport.connect()
        except TransportConnectError as e:
            logger.warning(str(e))
            self._state_mgr.transition_to(ConnectionState.DISCONNECTED)
            return False
        else: # Only start transport threads when connection is established.
            self._state_mgr.transition_to(ConnectionState.CONNECTED_DEFAULT)
            self._transport.start()
            self._router_task = asyncio.create_task(self._router_loop())
        return True

    async def stop(self) -> bool: 
        # Prerequisites
        if self.state in (
                ConnectionState.UNKNOWN, 
                ConnectionState.CLOSING,
                ConnectionState.CLOSED
                ):
            logger.warning(f"Current State:{self.state} cannot initiate disconnection.")
            return False
        
        # --- DISCONNECTION STATE
        # (1) ensure logoff is done before stopping
        if self.state == ConnectionState.CONNECTED_LOGON:
            # Successful Logoff automatically move state to LOGOFF
            try:
                logoff_msg = await self.logoff() 
            except TransportConnectError as e:
                logger.warning(str(e)) # proceed to ungraceful disconnection
                
            if not logoff_msg:
                return False
       
        try:  # Try Disconnect first before joining the threads
             self._transport.disconnect()
        except TransportDisconnectError as e:
            logger.warning(str(e))
            return False
        else:
            self._state_mgr.transition_to(ConnectionState.DISCONNECTED)
            
        # --- CLOSING STATE
        if self.state == ConnectionState.DISCONNECTED:
            self._state_mgr.transition_to(ConnectionState.CLOSING)
            
        # Stop the Router loop
        self._stop_evt.set()

        try: # This stops the send and recv loops and join the threads
            self._transport.stop()
        except TransportDisconnectError as e:
            logger.warning("Transport Dosconnect Failed: %s.", str(e))
        finally:
             if self._router_task:
                self._router_task.cancel()
                try:
                    await self._router_task
                except (asyncio.CancelledError, Exception) as e:
                    if not isinstance(e, asyncio.CancelledError):
                        logger.warning("Router task raised on shutdown: %s", e)
                self._state_mgr.transition_to(ConnectionState.CLOSED)
                
        return True

    # ---- Router Loop ------        
    async def _router_loop(self) -> None:

        while not self._stop_evt.is_set():
            msg: ServerMsg = await self._transport.recv()
                
            if not msg or not isinstance(msg, ServerMsg):
                logger.warning("Invalid Message Type, msg: %s", msg)
                continue
            
            # 0) check if it is a composite message
            top_unique_fields = server_msg_type(msg)
            
            if len(top_unique_fields) > 1:
                msgs = split_server_msg(msg, top_unique_fields)
            elif len(top_unique_fields) == 0:
                continue
            else:
                msgs = [msg]

            for msg, top_unique_field in zip(msgs, top_unique_fields):
                # Cheapest check first, 
                # 1) streaming dispatch
                if is_realtime_tick(top_unique_field):
                    contract_id = realtime_tick_contract_id(msg)
                    await self._mkt_data_stream_router.publish(contract_id, msg)
                    continue
    
                # 2) order update dispatch <--need to handle this better
                if is_order_update_stream(top_unique_field):
                    order_id = order_statuses_order_id(msg)
                    await self._exec_stream_router.publish(order_id, msg)
                    continue
                    
                # 3) Expensive RPC type key matching
                keys = extract_router_keys(msg)
                if len(keys) >1:
                    logger.debug("multiple keys: %s", keys)
                for key in keys:
                    if key is not None:        
                        key_type, msg_type, msg_id_type, msg_id = key
                        # 3) RPC routing (futures), 
                        if key_type in {"rpc_reqid", "session", "sub", "info"}:
                            self._msg_router.on_message(key, msg)
                            #print('router loop', key, msg)
                            #await self._misc_queue.put(msg)
    # ---- Failure Mode -------------------
    async def _on_transport_failure(self, exc: Exception) -> None:
        pass
        
    async def _reconnect_loop(self):...
    
    async def _update_timeout_loop(self):...
             
    # ---- CQG messages function calls ----
    async def logon(
        self, 
        client_app_id: str ='WebApiTest', 
        client_version: str ='python-client-test-2-240',
        protocol_version_major: int = 2,
        protocol_version_minor: int = 240, 
        drop_concurrent_session: bool = False,
        private_label: str = "WebApiTest",
        **kwargs
        ) -> dict[str, Any] | None:
        
        with msg_io_error_handler(
                ConnectRequestError, 
                timeout_error = ConnectTimeOutError
            ):
            client_msg =build_logon_msg(
                    self._user_name, self._password,
                    client_app_id=client_app_id,
                    protocol_version_major= protocol_version_major,
                    protocol_version_minor=protocol_version_minor,
                    drop_concurrent_session = drop_concurrent_session,
                    private_label = private_label,
                    **kwargs
                    )
            
            msg_key = ('session', 'logon_result', 'single', 0)
            fut = self._msg_router.register_key(msg_key)
            
            await self._transport.send(client_msg)
            server_msg = await asyncio.wait_for(fut, timeout = self._timeout)
            
            int_msg = parse_logon_result(server_msg) # internal message
                    
            if CONN_LOGON_RESCODE_CQG2INT.get(int_msg['result_code']):
                next_state = CONN_LOGON_RESCODE_CQG2INT[int_msg['result_code']]
                self._state_mgr.transition_to(next_state)
            return int_msg
    
    async def logoff(self) -> dict[str, Any] | None:
        # Logoff. Invoke this everytime when a connection is dropped
        with msg_io_error_handler(
                ConnectRequestError, 
                timeout_error = ConnectTimeOutError
            ):
            client_msg = build_logoff_msg("logoff")
        
            msg_key = ('session', 'logged_off', 'single', 0)
            fut = self._msg_router.register_key(msg_key)
        
            await self._transport.send(client_msg)
            server_msg = await asyncio.wait_for(fut, timeout = self._timeout)
        
            int_msg = parse_logged_off(server_msg)
        
            # Only accept specific path
            if CONN_LOGOFF_RESCODE_CQG2INT.get(int_msg['logoff_reason']):
                next_state = CONN_LOGOFF_RESCODE_CQG2INT[int_msg['logoff_reason']]
                self._state_mgr.transition_to(next_state)
            return int_msg

    async def restore_request(
            self, 
            session_token: str | None= None, 
            client_app_id: str | None = None,
            protocol_version_major: int | None = None,
            protocol_version_minor: int | None = None,
            **kwargs
        ) -> dict[str, Any] | None:
        # Restoring session after dropoff     
        with msg_io_error_handler(
                ConnectRequestError, 
                timeout_error = ConnectTimeOutError
            ):
            restore_msg = build_restore_msg(
                client_app_id          if client_app_id          is not None else self.client_app_id,
                protocol_version_major if protocol_version_major is not None else self.protocol_version_major,
                protocol_version_minor if protocol_version_minor is not None else self.protocol_version_minor,
                session_token          if session_token          is not None else self.session_token,
                **kwargs)

            msg_key = ('session', 'restore_or_join_session_result', 'single', 0)
            fut = self._msg_router.register_key(msg_key)
            await self._transport.send(restore_msg)
            server_msg = await asyncio.wait_for(fut, timeout = self._timeout)
            
            with msg_io_error_handler(ConnectRequestError):
                int_msg = parse_restore_or_join_session_result(server_msg)
            
            if CONN_RESTORE_RESCODE_CQG2INT.get(int_msg['result_code']):
                next_state = CONN_RESTORE_RESCODE_CQG2INT[int_msg['result_code']]
                self._state_mgr.transition_to(next_state)
            return int_msg

    async def ping(self, token: str | None = None) -> PongType | None:
        if not token:
            token = str(self.rid())
        utc_time = int(datetime.now(tz=timezone.utc).timestamp())
        
        with msg_io_error_handler(
                ConnectRequestError, 
                timeout_error = ConnectTimeOutError
            ):
            ping_msg = build_ping_msg(token, ping_utc_time=utc_time)

            msg_key =  ('session', 'pong', 'token', token)
            fut = self._msg_router.register_key(msg_key)
            await self._transport.send(ping_msg)
            server_msg = await asyncio.wait_for(fut, timeout=self._timeout)
            return parse_pong(server_msg)
        
    async def resolve_symbol(
        self, symbol: str,
        ) -> ContractMetaDataType | None:
        
        # symbol Resolution
        with msg_io_error_handler(
                ConnectRequestError, 
                timeout_error = ConnectTimeOutError
            ):
            msg = build_resolve_symbol_msg(symbol, self.rid, subscribe=True)

            msg_key = ("rpc", "information_report:symbol_resolution_report", "request_id", self.rid)
            fut = self._msg_router.register_key(msg_key)
            await self._transport.send(msg)
            server_msg = await asyncio.wait_for(fut, timeout=self._timeout)
            
            # walk through the second layer of the message, Find all info report,        
            # parse a list of info
            return parse_symbol_resolution_report(server_msg)
