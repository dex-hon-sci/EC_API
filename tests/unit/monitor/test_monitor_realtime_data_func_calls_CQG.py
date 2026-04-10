import pytest
import asyncio

from EC_API.ext.WebAPI.market_data_2_pb2 import MarketDataSubscriptionStatus as MktDSubStatus
from EC_API.ext.WebAPI.market_data_2_pb2 import MarketDataSubscription as MktDSub
from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg
from EC_API.connect.cqg.base import ConnectCQG
from EC_API.monitor.cqg.realtime_data import MonitorDataCQG
from EC_API.monitor.enums import MktDataSubLevel

from tests.unit.fixtures.proxy_clients import FakeTransport
from tests.unit.fixtures.server_msg_builders_CQG import (
    build_market_data_subscription_statuses_server_msg,
    build_real_time_market_data_server_msg
    )
from EC_API.exceptions import (MonitorDataRequestError)

async def _inject_after_send(
        fake_transport: FakeTransport,
        response: ServerMsg
    ) -> None:
    """Wait for an outbound message then inject a server response."""
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, fake_transport.out_q.get)
    await fake_transport.in_q.put(response)

@pytest.mark.asyncio
async def test_realtime_data_request_valid() -> None:
    #fake_client = FakeCQGClient()
    conn = ConnectCQG(
        "host_name", "user_name", "password", 
        immediate_connect= False, client=object()
        )
    fake_transport = FakeTransport()
    conn._transport = fake_transport
    conn._timeout = 0.1
    
    conn.start()
    MD = MonitorDataCQG(conn)
    
    msg = build_market_data_subscription_statuses_server_msg(ServerMsg(), contract_id=19)
    msg = build_real_time_market_data_server_msg(msg, 19)

    result, _ = await asyncio.gather(
        MD._realtime_data_request(19, MktDataSubLevel.LEVEL_TRADES),
        _inject_after_send(fake_transport, msg)
        )    
    assert result is not None
    assert isinstance(result,list)
    assert len(result) == 1 
    assert result[0]['contract_id'] == 19
    assert result[0]['status_code'] == MktDSubStatus.StatusCode.STATUS_CODE_SUCCESS
    assert result[0]['level'] == MktDSub.Level.LEVEL_TRADES
    # Add assert after finishing the parser functions
    await conn.stop()

@pytest.mark.asyncio    
async def test_unsubscribe_mkt_data_valid() -> None:
    conn = ConnectCQG(
        "host_name", "user_name", "password", 
        immediate_connect= False, client=object()
        )
    fake_transport = FakeTransport()
    conn._transport = fake_transport
    conn._timeout = 0.1
    
    conn.start()
    MD = MonitorDataCQG(conn)
    
    msg = build_market_data_subscription_statuses_server_msg(
        ServerMsg(), contract_id=19, level=MktDSub.Level.LEVEL_NONE)

    result, _ = await asyncio.gather(
        MD._unsubscribe_mkt_data(19),
        _inject_after_send(fake_transport, msg)
        )    
    assert result is not None
    assert isinstance(result,list)
    assert len(result) == 1
    assert result[0]['contract_id'] == 19
    assert result[0]['status_code'] == MktDSubStatus.StatusCode.STATUS_CODE_SUCCESS
    assert result[0]['level'] == MktDSub.Level.LEVEL_NONE
 
    await conn.stop()

@pytest.mark.asyncio
async def test_realtime_data_request_invalid_wrong_level() -> None:
    conn = ConnectCQG(
        "host_name", "user_name", "password", 
        immediate_connect= False, client=object()
        )
    fake_transport = FakeTransport()
    conn._transport = fake_transport
    conn._timeout = 0.1
    
    WRONG_LEVEL = "WRONG_LEVEL"
    
    conn.start()
    MD = MonitorDataCQG(conn)
    with pytest.raises(
            MonitorDataRequestError, 
            match="Level: WRONG_LEVEL unsupported."
        ):
        await MD._realtime_data_request(19, WRONG_LEVEL)

