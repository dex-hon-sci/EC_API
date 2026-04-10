import asyncio
import pytest
from EC_API.ext.WebAPI.trade_routing_2_pb2 import TradeSubscriptionStatus as TrdSubStatus
from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg
from EC_API.connect.cqg.base import ConnectCQG
from EC_API.ordering.cqg.trade_session import TradeSessionCQG
from EC_API.ordering.enums import SubScope
from tests.unit.fixtures.proxy_clients import FakeTransport
from tests.unit.fixtures.server_msg_builders_CQG import (
    build_trade_subscription_statuses_server_msg,
    build_trade_snapshot_completetions_server_msg,
    build_real_time_market_data_server_msg
    )
from EC_API.exceptions import (
    TradeSessionRequestError, TradeSubscriptionMissingError
    )


async def _inject_after_send(
        fake_transport: FakeTransport,
        response: ServerMsg
    ) -> None:
    """Wait for an outbound message then inject a server response."""
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, fake_transport.out_q.get)
    await fake_transport.in_q.put(response)
    
def make_conn():
    conn = ConnectCQG(
        "host_name", "user_name", "password", 
        immediate_connect= False, client=object()
        )
    fake_transport = FakeTransport()
    conn._transport = fake_transport
    conn._timeout = 0.1
    return conn, fake_transport

@pytest.mark.asyncio
async def test_trade_subscription_request_valid()->None:
    conn,ft = make_conn()
    TS = TradeSessionCQG(conn)
    
    msg = ServerMsg()
    response1 = build_trade_subscription_statuses_server_msg(msg, sub_id = 2)
    response2 = build_trade_snapshot_completetions_server_msg(response1, sub_id = 2)
    
    result, _ = await asyncio.gather(
        TS.trade_subscription_request(2, SubScope.ORDERS),
        _inject_after_send(ft, response2)
        )    
    assert result is not None
    assert isinstance(result.trade_subscription_statuses, list)
    assert len(result.trade_subscription_statuses)==2
    assert result[0].trade_subscription_statuses[0].id == 2
    assert result[0].trade_subscription_statuses[0].status_code == TrdSubStatus.StatusCode.STATUS_CODE_SUCCESS

    assert result[1].trade_snapshot_completions[0].subscription_id == 2
    assert len(result[1].trade_snapshot_completions[0].subscription_scopes) == 4
    
@pytest.mark.asyncio
async def test_trade_subscription_request_invalid()->None:...

@pytest.mark.asyncio
async def test_unsubscribe_trade_request_valid()->None: ...

@pytest.mark.asyncio
async def test_unsubscribe_trade_request_invalid()-> None: ...

@pytest.mark.asyncio
async def test_request_historical_orders_valid() -> None: ...
