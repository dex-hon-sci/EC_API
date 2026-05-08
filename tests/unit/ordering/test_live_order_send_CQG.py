import asyncio
import pytest
from EC_API.ext.WebAPI.trade_routing_2_pb2 import TradeSubscription as CQG_TS
from EC_API.connect.cqg.base import ConnectCQG
from EC_API.ordering.enums import RequestType, SubScope
from EC_API.ordering.cqg.live_order import LiveOrderCQG
from EC_API.ordering.cqg.trade_session import TradeSessionCQG
from EC_API.exceptions import (
    LiveOrderTimeOutError,
    LiveOrderRequestError,
    MissingSymbolResolutionError,
    TradeSubscriptionMissingError,
    MissingOrderIDError
    )
from tests.unit.fixtures.proxy_clients import FakeCQGClient, FakeTransport

# ------ Happy Path ------
@pytest.mark.asyncio
async def test_new_order_request_send_valid() -> None: ...

@pytest.mark.asyncio
async def test_modify_order_request_send_valid() -> None: ...

@pytest.mark.asyncio
async def test_cancel_order_request_send_valid() -> None: ...

@pytest.mark.asyncio
async def test_activate_order_request_send_valid() -> None: ...

@pytest.mark.asyncio
async def test_cancelall_order_request_send_valid() -> None: ...

@pytest.mark.asyncio
async def test_liquidateall_order_request_send_valid() -> None: ...

@pytest.mark.asyncio
async def test_goflat_order_request_send_valid() -> None: ...


# ------ Sad Path
@pytest.mark.asyncio
async def test_order_request_failed_missing_symbol_name() -> None:
    fake_transport = FakeTransport()
    conn = ConnectCQG(
        "host_name",
        "user_name",
        "password",
        account_id=10000,
        immediate_connect=False,
        client=FakeCQGClient(),
        transport=fake_transport
        )
    conn._timeout = 0.0001
    
    request_details = {'A':'a'} # <---no 'symbol_name' field

    async with TradeSessionCQG(conn) as TS:
        with pytest.raises(KeyError):
            await LiveOrderCQG(TS).send(
                RequestType.NEW_ORDER, 
                request_details=request_details
                )
            
@pytest.mark.asyncio
async def test_order_request_failed_no_symbol_resolution() -> None:
    fake_transport = FakeTransport()
    conn = ConnectCQG(
        "host_name",
        "user_name",
        "password",
        account_id=10000,
        immediate_connect=False,
        client=FakeCQGClient(),
        transport=fake_transport
        )
    conn._timeout = 0.0001
    
    request_details = {'symbol_name':'CLE'} 

    async with TradeSessionCQG(conn) as TS: # <---no symbol resolution
        with pytest.raises(MissingSymbolResolutionError):
            await LiveOrderCQG(TS).send(
                RequestType.NEW_ORDER, 
                request_details=request_details
                )
            
@pytest.mark.asyncio
async def test_order_request_failed_trade_subscription_order_scope() -> None:
    fake_transport = FakeTransport()
    conn = ConnectCQG(
        "host_name",
        "user_name",
        "password",
        account_id=10000,
        immediate_connect=False,
        client=FakeCQGClient(),
        transport=fake_transport
        )
    conn._timeout = 0.0001
    
    request_details = {
        'symbol_name':'CLE', 
        'chain_order_id': 'chain_order_id_0' #<== wrong chain_order_id
        } 
    metadata = {'CLE': "something", "contract_id": 0}
    
    async with TradeSessionCQG(conn) as TS: # <---no Trade Subscription
        TS._symbol_registry.register('CLE', metadata)        
        TS._active_trade_subs[1] = [
            SubScope.ORDERS
            ]
        TS._active_order_q['chain_order_id_1']  = asyncio.Queue()
        
        with pytest.raises(MissingOrderIDError):
            await LiveOrderCQG(TS).send(
                RequestType.MODIFY_ORDER, 
                request_details=request_details
                )

