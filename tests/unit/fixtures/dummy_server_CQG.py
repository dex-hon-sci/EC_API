#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 06:34:47 2026

@author: dexter
"""
import asyncio
from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg, ClientMsg
from EC_API.ext.WebAPI.market_data_2_pb2 import MarketDataSubscription as MktDSub
from EC_API.ext.WebAPI.user_session_2_pb2 import LoggedOff as LOff
from EC_API.ext.WebAPI.webapi_2_pb2 import InformationReport as InfoRp

from EC_API.connect.cqg.base import ConnectCQG

from tests.unit.fixtures.server_msg_builders_CQG import (
    build_logged_off_server_msg,
    build_symbol_resolution_report_server_msg,
    build_market_data_subscription_statuses_server_msg,
    build_real_time_market_data_server_msg
    )

def client_msg_type(client_msg: ClientMsg) -> list[str]:
    return [fd.name for fd, val in client_msg.ListFields()]

class FakeDataServerCQG:
    def __init__(
            self, 
            conn: ConnectCQG, 
            loop: asyncio.BaseEventLoop, 
            success_decisions: dict = dict(),
            extra_instructions: dict = dict()
            ):
        self.conn = conn
        self.transport = self.conn._transport
        self.loop = loop
        # --- Settings
        self.success_decisions = success_decisions # Determine if a response return success or not
        self.extra_instructions = extra_instructions
        #
        self._server_stop_evt = asyncio.Event()
        
    async def response_logic(self, msg: ClientMsg):
        msg_name = client_msg_type(msg)[0] 
        # we assume client dispatch message one at a time
        match msg_name:
            # ---- Session ----
            case "logon":
                ...
            case "logoff":
                await self._logoff_response(msg)
            # ---- Metadata ----
            case "information_requests": # In this context
                await self._sym_res_response(msg)
                 
            # ---- Realtime Data ----
            case "market_data_subscriptions":
                await self._mkt_data_status_response(msg)
                count = 0
                #while not self.conn._stop_evt():
                if self.success_decisions["market_data_subscriptions"]:
                    while count < 100:
                        await self._mkt_data_stream_responses(msg)
                        count+=1
            case _:
                pass
            
    # ---- Sessions ----
    async def _logon_response(self, client_msg: ClientMsg) -> None:
        if self.success_decisions.get("logon") is not None:
            if self.success_decisions['logon']:
                ...
            elif not self.success_decisions['logon']:
                ...
        
    async def _restore_response(self, client_msg: ClientMsg) -> None:
        ...

    async def _logoff_response(self, client_msg: ClientMsg) -> None:
        if self.success_decisions.get("logoff") is not None:
            if self.success_decisions['logoff']:
                server_msg = build_logged_off_server_msg(
                    ServerMsg(),
                    res = LOff.LogoffReason.LOGOFF_REASON_BY_REQUEST
                    )
            else:
                server_msg = build_logged_off_server_msg(
                    ServerMsg(),
                    res = LOff.LogoffReason.LOGOFF_REASON_BY_REQUEST
                    )
        
            await self.transport.in_q.put(server_msg)
        
    # ---- Metadata ----
    async def _sym_res_response(self, client_msg: ClientMsg) -> None:
        if self.success_decisions.get("information_requests") is not None:
            sym = client_msg.information_requests[0].symbol_resolution_request.symbol

            if self.success_decisions["information_requests"]:
                
                if client_msg.information_requests[0].subscribe is None:
                    success_code = InfoRp.StatusCode.STATUS_CODE_SUCCESS
                else:
                    if client_msg.information_requests[0].subscribe:
                        success_code = InfoRp.StatusCode.STATUS_CODE_SUBSCRIBED
                    elif not client_msg.information_requests[0].subscribe:
                        success_code = InfoRp.StatusCode.STATUS_CODE_DROPPED
                    
                sym_rp = build_symbol_resolution_report_server_msg(
                    ServerMsg(), 
                    report_id = client_msg.information_requests[0].id,
                    cotract_id = int(sym.split("_")[-1]),
                    contract_symbol = sym,
                    res = success_code
                    )
                
            elif not self.success_decisions["information_requests"]:
                sym_rp = build_symbol_resolution_report_server_msg(
                    ServerMsg(), 
                    report_id = client_msg.information_requests[0].id,
                    cotract_id = int(sym.split("_")[-1]),
                    contract_symbol = sym,
                    res = InfoRp.StatusCode.STATUS_CODE_FAILURE
                    )
        await self.transport.in_q.put(sym_rp)
        
    # ---- Realtime Market ----
    async def _mkt_data_status_response(self, client_msg: ClientMsg):
        if self.success_decisions.get("market_data_subscriptions") is not None:
            if self.success_decisions["market_data_subscriptions"]:
                for mkt_sub in client_msg.market_data_subscriptions:
                    mkt_status = build_market_data_subscription_statuses_server_msg(
                        ServerMsg(),
                        contract_id= mkt_sub.contract_id,
                        level = mkt_sub.level
                        )
            elif not self.success_decisions["market_data_subscriptions"]:
                for mkt_sub in client_msg.market_data_subscriptions:

                    mkt_status = build_market_data_subscription_statuses_server_msg(
                        ServerMsg(),
                        contract_id= mkt_sub.contract_id,
                        level = mkt_sub.level
                        )
                
            #print("[producer] mkt_status", mkt_status)
            #from EC_API.protocol.cqg.router_util import extract_router_keys
            #print("[producer] key extraction", extract_router_keys(mkt_status))
            
            await self.transport.in_q.put(mkt_status)
        
    async def _mkt_data_stream_responses(self, client_msg: ClientMsg):
            for mkt_sub in client_msg.market_data_subscriptions:
                server_msg = build_real_time_market_data_server_msg(
                    ServerMsg(),
                    contract_id = mkt_sub.contract_id
                    )
                
            await self.transport.in_q.put(server_msg)
            
    async def _unsubscribe_mkt_data_response(self):...
    
    # ---- Trade Session ----
    # ---- run method ----
    async def run(self):
        import functools
        import queue
        # while loop, scan the transport
        while not self._server_stop_evt.is_set():
            
            try:
                client_msg = await self.loop.run_in_executor(
                    None, functools.partial(self.transport.out_q.get, timeout = 0.05)
                    )
            except queue.Empty:
                raise
                
            #client_msg = self.transport.out_q.get()
            await self.response_logic(client_msg)
            
            if client_msg.market_data_subscriptions:
                if client_msg.market_data_subscriptions[0].level == MktDSub.Level.LEVEL_NONE:
                    break
        

# =============================================================================
# class DummyWSServer:
#     
#     def __init__(
#             self,
#             host: str,
#             port: int,
#         ):
#         self._host = host
#         self._port = port
#         
#     @property
#     def host(self) -> str:
#         return self._host
#     
#     @property
#     def port(self) -> int:
#         return self._port
#     
#     @property
#     def url(self) -> str:
#         return f"https://{self.host}:{self.port}"
#     
#     async def start(self):
#         return 
#     
#     async def stop(self):
#         return 
#     # Build up message
#     # Unleash
#     
#     
# 
# class FakeDataServer:...
#     
# class FakeTradeServer:...
# 
# @pytest.fixture
# async def dummy_server():
#     server = DummyWSServer("", 0)
#     
# def decoder():...
# async def place_standard_reponses():...
# =============================================================================
    
