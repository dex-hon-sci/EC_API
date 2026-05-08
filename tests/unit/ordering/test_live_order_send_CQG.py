import asyncio
import pytest
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
from tests.unit.fixtures.dummy_server_CQG import FakeDataServerCQG

# ------ Happy Path ------
@pytest.mark.asyncio
async def test_new_order_request_send_valid() -> None:
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

@pytest.mark.asyncio
async def test_modify_order_request_send_valid() -> None:
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
    # ---
    success_decisions = {
        "modify_order_request": True,
        "information_requests": True
        }
    loop = asyncio.get_running_loop()
    fake_server = FakeDataServerCQG(
        conn, loop, success_decisions = success_decisions
        )

    # --- Send
    request_details = {
        "symbol_name": "CLE",
        "order_id": "order_id_1",
        "cl_order_id": "1231314",
        "orig_cl_order_id" : "1313",
        "qty": 12,
        #"chain_order_id": "chain_order_id_1"
        }
    metadata = {'CLE': "something", "contract_id": 0}
    
    async def send_order():
        async with TradeSessionCQG(conn) as TS:
            TS._symbol_registry.register('CLE', metadata)        
            TS._active_trade_subs[1] = [SubScope.ORDERS]
            TS._active_order_q['chain_order_id_1']  = asyncio.Queue()
            
            TS.latest_order_state_by_chain['chain_order_id_1'] = {'order_id': 'order_id_1'}
            TS.active_order_ids_by_chain['chain_order_id_1'] = ('order_id_1', 10101)

            await LiveOrderCQG(TS).send(
                RequestType.MODIFY_ORDER, 
                request_details=request_details
                )
            
    result, _ = await asyncio.gather(send_order(), fake_server.run(contract_id=0))

    print('out_q', list(fake_transport.out_q.queue))
    assert 1==0

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
        } 
    metadata = {'CLE': "something", "contract_id": 0}
    
    async with TradeSessionCQG(conn) as TS: # <---no Trade Subscription
        TS._symbol_registry.register('CLE', metadata)     
        with pytest.raises(TradeSubscriptionMissingError):
            await LiveOrderCQG(TS).send(
                RequestType.MODIFY_ORDER, 
                request_details=request_details
                )

@pytest.mark.asyncio
async def test_order_request_failed_no_order_id() -> None:
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
    
    metadata = {'CLE': "something", "contract_id": 0}
    
    async with TradeSessionCQG(conn) as TS: # <---no order ID
        TS._symbol_registry.register('CLE', metadata)        
        TS._active_trade_subs[1] = [SubScope.ORDERS]
        TS._active_order_q['chain_order_id_1']  = asyncio.Queue()
        
        for request_type in (
                RequestType.MODIFY_ORDER, 
                RequestType.ACTIVATE_ORDER, 
                RequestType.CANCEL_ORDER
                ):
            request_details = {
                'symbol_name':'CLE', 
                'order_id': 'order_id_0' #<== wrong chain_order_id
                } 
            with pytest.raises(MissingOrderIDError):
                await LiveOrderCQG(TS).send(
                    request_type, 
                    request_details = request_details
                    )

