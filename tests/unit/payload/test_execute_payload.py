#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 03:44:56 2026

@author: dexter
"""
from pathlib import Path
import asyncio
import logging
import pytest
from EC_API.connect.cqg.base import ConnectCQG
from EC_API.ordering.enums import (
    Side, SubScope,
    Duration, RequestType,
    OrderType,
    ExecInstruction
    )
from EC_API.ordering.cqg.live_order import LiveOrderCQG
from EC_API.ordering.cqg.trade_session import TradeSessionCQG
from EC_API.payload.base import Payload, ExecutePayload
from EC_API.payload.enums import PayloadStatus
from EC_API.payload.safety import PreTradeRiskCheck

from tests.unit.fixtures.proxy_clients import FakeCQGClient, FakeTransport
from tests.unit.fixtures.dummy_server_CQG import FakeDataServerCQG

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"
TEST_RISK_CONFIG = FIXTURES_DIR / "test_payload_check.toml"

PTRC = PreTradeRiskCheck('cqg')
PTRC.load(TEST_RISK_CONFIG)


@pytest.fixture
async def conn(timeout = None):
    c = ConnectCQG(
        "host_name", "user_name", "password",
        account_id=10000,
        immediate_connect=False,
        client=FakeCQGClient(),
        transport=FakeTransport(),
    )
    c._timeout = 0.01 if timeout is None else timeout
    return c

@pytest.mark.asyncio
async def test_execute_payload_new_order_request_send_valid(conn, caplog) -> None:
    success_decisions = {
        "new_order_request": True,
        "information_requests": True
        }
    loop = asyncio.get_running_loop()
    fake_server = FakeDataServerCQG(
        conn, loop, success_decisions = success_decisions
        )
    
    request_details = {
        "symbol_name": "CLE",
        "cl_order_id": "1231314",
        "order_type": OrderType.LMT,
        "duration": Duration.GTC,
        "side": Side.BUY,
        "qty": 2,
        "is_manual": False,
        "limit_price": 150,
        "exec_instructions": ExecInstruction.NONE,
    }
    metadata = {'CLE': "something", "contract_id": 1}
    
    PL = Payload(          
            order_request_type = RequestType.NEW_ORDER,
            order_info = request_details,
            risk_check = PTRC
            )

    async def unload_order():
        async with TradeSessionCQG(conn) as TS:
            TS._symbol_registry.register('CLE', metadata)
            TS._active_trade_subs[1] = [SubScope.ORDERS]
            
            await ExecutePayload(PL, LiveOrderCQG(TS)).unload()
                        
    with caplog.at_level(logging.INFO, logger="EC_API.payload.base"):
        result, _ = await asyncio.gather(unload_order(), fake_server.run(contract_id=1))
    assert "Payload sent" in caplog.text
    assert PL.status == PayloadStatus.SENT

# --- Error
@pytest.mark.asyncio
async def test_execute_payload_fail_not_pending(conn, caplog) -> None:
    request_details = {
        "symbol_name": "CLE",
        "cl_order_id": "1231314",
        "order_type": OrderType.LMT,
        "duration": Duration.GTC,
        "side": Side.BUY,
        "qty": 2,
        "is_manual": False,
        "limit_price": 150,
        "exec_instructions": ExecInstruction.NONE,
    }
    PL = Payload(          
            order_request_type = RequestType.NEW_ORDER,
            order_info = request_details,
            risk_check = PTRC
            )
    PL.status = PayloadStatus.SENT # <-- illegal start
    async def unload_order():
        async with TradeSessionCQG(conn) as TS:            
            await ExecutePayload(PL, LiveOrderCQG(TS)).unload()

    with caplog.at_level(logging.WARNING, logger="EC_API.payload.base"):
        await unload_order()
    assert "Only pending payloads can be unloaded" in caplog.text
    
@pytest.mark.asyncio
async def test_execute_payload_fail_timeout(conn, caplog) -> None:
    request_details = {
        "symbol_name": "CLE",
        "cl_order_id": "1231314",
        "order_type": OrderType.LMT,
        "duration": Duration.GTC,
        "side": Side.BUY,
        "qty": 2,
        "is_manual": False,
        "limit_price": 150,
        "exec_instructions": ExecInstruction.NONE,
    }
    metadata = {'CLE': "something", "contract_id": 1}

    PL = Payload(          
            order_request_type = RequestType.NEW_ORDER,
            order_info = request_details,
            risk_check = PTRC
            )
    async def unload_order():
        async with TradeSessionCQG(conn) as TS:        
            TS._symbol_registry.register('CLE', metadata)
            TS._active_trade_subs[1] = [SubScope.ORDERS]

            await ExecutePayload(PL, LiveOrderCQG(TS)).unload()

    with caplog.at_level(logging.WARNING, logger="EC_API.payload.base"):
        await unload_order()
    assert "Payload timed out" in caplog.text
    assert PL.status == PayloadStatus.VOID
    
@pytest.mark.asyncio
async def test_execute_payload_fail_builder_error(conn, caplog) -> None:
    request_details = {
        "symbol_name": "CLE",
        "cl_order_id": 123131, # <--wrong type
        "order_type": OrderType.LMT,
        "duration": Duration.GTC,
        "side": Side.BUY,
        "qty": 2,
        "is_manual": False,
        "limit_price": 150,
        "exec_instructions": ExecInstruction.NONE,
    }
    metadata = {'CLE': "something", "contract_id": 1}

    PL = Payload(          
            order_request_type = RequestType.NEW_ORDER,
            order_info = request_details,
            risk_check = PTRC
            )
    async def unload_order():
        async with TradeSessionCQG(conn) as TS:        
            TS._symbol_registry.register('CLE', metadata)
            TS._active_trade_subs[1] = [SubScope.ORDERS]

            await ExecutePayload(PL, LiveOrderCQG(TS)).unload()

    with caplog.at_level(logging.WARNING, logger="EC_API.payload.base"):
        await unload_order()
    assert "Payload rejected" in caplog.text
    assert PL.status == PayloadStatus.VOID

@pytest.mark.asyncio
async def test_execute_payload_fail_missing_trade_sub_error(conn, caplog) -> None:
    request_details = {
        "symbol_name": "CLE",
        "cl_order_id": 123131, # <--wrong type
        "order_type": OrderType.LMT,
        "duration": Duration.GTC,
        "side": Side.BUY,
        "qty": 2,
        "is_manual": False,
        "limit_price": 150,
        "exec_instructions": ExecInstruction.NONE,
    }
    metadata = {'CLE': "something", "contract_id": 1}

    PL = Payload(          
            order_request_type = RequestType.NEW_ORDER,
            order_info = request_details,
            risk_check = PTRC
            )
    async def unload_order():
        async with TradeSessionCQG(conn) as TS:        
            TS._symbol_registry.register('CLE', metadata)
            #TS._active_trade_subs[1] = [SubScope.ORDERS] # <--missing trade_subs

            await ExecutePayload(PL, LiveOrderCQG(TS)).unload()

    with caplog.at_level(logging.WARNING, logger="EC_API.payload.base"):
        await unload_order()
    assert "Payload blocked — setup error" in caplog.text
    assert PL.status == PayloadStatus.VOID
    
@pytest.mark.asyncio
async def test_execute_payload_fail_missing_sym_res_error(conn, caplog) -> None:
    request_details = {
        "symbol_name": "CLE",
        "cl_order_id": 123131, # <--wrong type
        "order_type": OrderType.LMT,
        "duration": Duration.GTC,
        "side": Side.BUY,
        "qty": 2,
        "is_manual": False,
        "limit_price": 150,
        "exec_instructions": ExecInstruction.NONE,
    }
    metadata = {'CLE': "something", "contract_id": 1}

    PL = Payload(          
            order_request_type = RequestType.NEW_ORDER,
            order_info = request_details,
            risk_check = PTRC
            )
    async def unload_order():
        async with TradeSessionCQG(conn) as TS:        
            #TS._symbol_registry.register('CLE', metadata)# <--missing symbol_resolution
            TS._active_trade_subs[1] = [SubScope.ORDERS] 

            await ExecutePayload(PL, LiveOrderCQG(TS)).unload()

    with caplog.at_level(logging.WARNING, logger="EC_API.payload.base"):
        await unload_order()
    assert "Payload blocked — setup error" in caplog.text
    assert PL.status == PayloadStatus.VOID
    
@pytest.mark.asyncio
async def test_execute_payload_fail_missing_order_id_error(conn, caplog) -> None:
    request_details = {
        "symbol_name": "CLE",
        "order_id": "order_id_0", # Unknown Order ID
        "cl_order_id": "1231314",
        "orig_cl_order_id" : "1313",
        "qty": 8,
        }
    metadata = {'CLE': "something", "contract_id": 0}

    PL = Payload(          
            order_request_type = RequestType.MODIFY_ORDER,
            order_info = request_details,
            risk_check = PTRC
            )
    async def unload_order():
        async with TradeSessionCQG(conn) as TS:        
            TS._symbol_registry.register('CLE', metadata)        
            TS._active_trade_subs[1] = [SubScope.ORDERS]
            TS._active_order_q['chain_order_id_1']  = asyncio.Queue()
            
            TS.latest_order_state_by_chain['chain_order_id_1'] = {'order_id': 'order_id_1'}
            TS.active_order_ids_by_chain['chain_order_id_1'] = ('order_id_1', 10101)

            await ExecutePayload(PL, LiveOrderCQG(TS)).unload()

    with caplog.at_level(logging.WARNING, logger="EC_API.payload.base"):
        await unload_order()
    assert "Payload blocked — setup error" in caplog.text
    assert PL.status == PayloadStatus.VOID
