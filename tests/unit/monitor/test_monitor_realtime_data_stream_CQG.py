import pytest
import asyncio
import random
from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg
from EC_API.connect.enums import ConnectionState
from EC_API.connect.cqg.base import ConnectCQG
from EC_API.connect.enums import ConnectionState
from EC_API.monitor.enums import MktDataSubLevel
from EC_API.monitor.cqg.realtime_data import MonitorDataCQG
from EC_API._typing import ParsedRTMDCQG
from tests.unit.fixtures.proxy_clients import FakeTransport
from tests.unit.fixtures.server_msg_builders_CQG import (
    build_symbol_resolution_report_server_msg,
    build_market_data_subscription_statuses_server_msg,
    build_real_time_market_data_server_msg
    )

# =============================================================================
# 
# async def _inject_after_send(
#         loop,
#         fake_transport: FakeTransport,
#         response: ServerMsg
#     ) -> None:
#     """Wait for an outbound message then inject a server response."""
#     await loop.run_in_executor(None, fake_transport.out_q.get)
#     await fake_transport.in_q.put(response)
#     
# =============================================================================
async def fake_consumer(
        MD: MonitorDataCQG,
        level: MktDataSubLevel,
        symbol_name: str
    ) -> list[ParsedRTMDCQG]:
    res: list[ParsedRTMDCQG] = []
    count = 0
    async for tick in MD.stream(symbol_name, level=level):
        res.append(tick)
        count+=1
        if count == 100:
            break
        
    return res
    
    
async def fake_producer( 
        #loop: asyncio.BaseEventLoop,       
        fake_transport: FakeTransport, 
        sym_count = 4,
        nums = 100, 
        seed = 10,
    ) -> None:
    rng = random.Random(seed)
    
    k = 0
    # symbol res report
    for i in range(sym_count):
        sym_rp = build_symbol_resolution_report_server_msg(
            ServerMsg(), 
            report_id = k,
            cotract_id = i,
            contract_symbol = f"FakeSymbol_{i}",
            )
        k+=1
        await fake_transport.in_q.put(sym_rp)
        
    # market subscription status
    for i in range(sym_count):
        mkt_status = build_market_data_subscription_statuses_server_msg(
            ServerMsg()
            )
        k+=1
        await fake_transport.in_q.put(mkt_status)
        
    # real-time data 
    for _ in range(nums):
        msg = build_real_time_market_data_server_msg(
            ServerMsg(),contract_id = rng.randrange(0, sym_count)
            )
        await fake_transport.in_q.put(msg)
        


@pytest.mark.asyncio
async def test_monitor_data_CQG_yield_one_item_valid() -> None:
    async with ConnectCQG(
        "host_name", "user_name", "password", 
        immediate_connect= False, client=object()
        ) as conn:
        fake_transport = FakeTransport()

        conn.transport = fake_transport
        MD = MonitorDataCQG(conn)
        #loop = asyncio.get_running_loop()

        # Setup Logon state
        conn._state_mgr.transition_to(ConnectionState.CONNECTING)
        conn._state_mgr.transition_to(ConnectionState.CONNECTED_DEFAULT)
        conn._state_mgr.transition_to(ConnectionState.CONNECTED_LOGON)
        
        # load and consume data
        result, _ = await asyncio.gather(
            fake_consumer(MD, MktDataSubLevel.LEVEL_TRADES_BBA, 'FakeSymbol_1'),
            fake_producer(fake_transport, sym_count = 4, nums=100)
            )  
        
        # tests
        assert result
            
@pytest.mark.asyncio
async def test_stops_on_event() -> None:...

@pytest.mark.asyncio
async def test_monitor_data_CQG_stream_valid():
    async with ConnectCQG(
        "host_name", "user_name", "password", 
        immediate_connect= False, client=object()
        ) as conn:
        MD = MonitorDataCQG(conn)
        
        conn._state_mgr.transition_to(ConnectionState.CONNECTED_LOGON)
    
# test for no logon
# test for error in realtime_requests..
# test for error in unsubscribe requests...