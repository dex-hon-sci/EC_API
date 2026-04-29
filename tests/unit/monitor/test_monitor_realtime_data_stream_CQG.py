import pytest
import asyncio
from EC_API.connect.enums import ConnectionState
from EC_API.connect.cqg.base import ConnectCQG
from EC_API.monitor.enums import MktDataSubLevel
from EC_API.monitor.cqg.realtime_data import MonitorDataCQG
from EC_API._typing import (
    ParsedRTMDCQG,
    QuotesValueTypeCQG,
    MarketValueTypeCQG,
    Q_CONTRACT_ID, MV_CONTRACT_ID
    )
from tests.unit.fixtures.proxy_clients import (
    FakeTransport, 
    FakeCQGClient
    )
from tests.unit.fixtures.dummy_server_CQG import (
    FakeDataServerCQG
    )


async def fake_consumer(
        MD: MonitorDataCQG,
        level: MktDataSubLevel,
        symbol_name: str,
        stop_num_trigger: int = 10
    ) -> list[ParsedRTMDCQG]:
    res: list[ParsedRTMDCQG] = []
    count = 0
    async for tick in MD.stream(symbol_name, level=level):
        res.append(tick)
        print('tick', tick)
        count+=1
        if count == stop_num_trigger:
            MD.conn._stop_evt.set()
    return res

@pytest.mark.asyncio
async def test_monitor_data_stream_CQG_valid() -> None:
    success_decision = {
        'logoff': True,
        'information_requests': True,
        'market_data_subscriptions': True
        }
    
    conn = ConnectCQG(
        "host_name", 
        "user_name", 
        "password", 
        immediate_connect= False, 
        client = FakeCQGClient()
        )
    fake_transport = FakeTransport()
    conn._transport = fake_transport
    conn._timeout = 0.1
    async with conn:        
        MD = MonitorDataCQG(conn)
        loop = asyncio.get_running_loop()

        # Setup Logon state
        conn._state_mgr.transition_to(ConnectionState.CONNECTED_LOGON)
        result,  _ = await asyncio.gather(
            fake_consumer(MD, MktDataSubLevel.LEVEL_TRADES_BBA, 'FakeSymbol_0'),
            FakeDataServerCQG(conn, loop, success_decision).run()
            )  
        #print(result[0], len(result))

        assert isinstance(result, list)
        assert len(result) == 10
        
        assert isinstance(result[0], tuple)
        assert len(result[0]) == 4
        
        for i in range(len(result)):
            assert isinstance(result[i][0][0], QuotesValueTypeCQG)
            assert isinstance(result[i][0][1], MarketValueTypeCQG)

            assert result[i][0][0][Q_CONTRACT_ID] == 0
            assert result[i][0][1][MV_CONTRACT_ID] == 0
        conn._state_mgr.transition_to(ConnectionState.CONNECTED_LOGOFF)
        

@pytest.mark.asyncio
async def test_monitor_data_stream_no_logon_invalid() -> None:
    conn = ConnectCQG(
        "host_name", "user_name", "password", 
        immediate_connect = False, 
        client = FakeCQGClient()
        )
    fake_transport = FakeTransport()
    conn._transport = fake_transport
    conn._timeout = 0.01
        
    async with conn:
        MD = MonitorDataCQG(conn)
        # conn._state_mgr.transition_to(ConnectionState.CONNECTED_LOGON) <--no logon
        result = [tick async for tick in MD.stream(
                        "FakeSymbol_0", level=MktDataSubLevel.LEVEL_TRADES_BBA)]
        assert result == []

@pytest.mark.asyncio
async def test_monitor_data_CQG_stream_bad_res_report_invalid() -> None:
    success_decision = {
        'logoff': True,
        'information_requests': True, #<--False
        'market_data_subscriptions': True #<--False
        }
    
    conn = ConnectCQG(
        "host_name", 
        "user_name", 
        "password", 
        immediate_connect= False, 
        client = FakeCQGClient()
        )
    fake_transport = FakeTransport()
    conn._transport = fake_transport
    conn._timeout = 0.1
    async with conn:        
        MD = MonitorDataCQG(conn)
        loop = asyncio.get_running_loop()

        # Setup Logon state
        conn._state_mgr.transition_to(ConnectionState.CONNECTED_LOGON)
        result,  _ = await asyncio.gather(
            fake_consumer(MD, MktDataSubLevel.LEVEL_TRADES_BBA, 'FakeSymbol_0'),
            FakeDataServerCQG(conn, loop, success_decision).run()
            )  
        
@pytest.mark.asyncio
async def test_monitor_data_CQG_stream_res_report_no_response_invalid():...

@pytest.mark.asyncio
async def test_monitor_data_CQG_stream_failed_symbol_regsiter_invalid():
    conn = ConnectCQG(
        "host_name", "user_name", "password", 
        immediate_connect = False, 
        client = FakeCQGClient()
        )
    fake_transport = FakeTransport()
    conn._transport = fake_transport
    conn._timeout = 0.01
        
    async with conn:
        MD = MonitorDataCQG(conn)
        loop = asyncio.get_running_loop()

        # Setup Logon state
        conn._state_mgr.transition_to(ConnectionState.CONNECTED_LOGON)
        conn._state_mgr.transition_to(ConnectionState.CONNECTED_LOGOFF)

@pytest.mark.asyncio
async def test_monitor_data_CQG_stream_failed_mkt_subs_invalid() -> None:...

@pytest.mark.asyncio
async def test_monitor_data_CQG_stream_max_subscribers_exceeded_invalid() -> None:...

@pytest.mark.asyncio
async def test_monitor_data_CQG_stream_max_sym_exceeded_invalid() -> None:...

@pytest.mark.asyncio
async def test_monitor_data_CQG_stream_unsupported_level_invalid() -> None:...

@pytest.mark.asyncio
async def test_monitor_data_CQG_stream_stops_on_event() -> None:...

# =============================================================================
#   From the symbol resolution block (lines 111–119):
#   - SymbolResolutionError — server sends a bad/failed resolution report →
#   decisions={'sym_resolution': False}
#   - ConnectTimeOutError — server never responds to symbol resolution (no in_q message)
#   - FailRegisterError / SymbolNotInRegistryError — resolution succeeds but registry
#   rejects it
# 
#   From the subscription block (lines 129–139):
#   - MonitorDataRequestError — server sends a failed subscription status →
#   decisions={'mkt_status': False}
#   - MaxSymbolsExceededError / MaxSubscribersExceededError — status code indicates
#   capacity breach
#   - UnsupportedLevelError — already tested at the unit level but not through stream()
# 
#   From the streaming loop:
#   - test_stops_on_event — already stubbed out (line 184), just needs the body
# 
# =============================================================================

# =============================================================================
# async def fake_producer_symres(        
#         loop: asyncio.BaseEventLoop,       
#         fake_transport: FakeTransport, 
#         start_id = 10,
#         sym_count = 1,
#     ) -> None:
#     # symbol res report
#     k = start_id 
# 
#     for i in range(sym_count):
#         sym_rp = build_symbol_resolution_report_server_msg(
#             ServerMsg(), 
#             report_id = k,
#             cotract_id = i,
#             contract_symbol = f"FakeSymbol_{i}",
#             )
#         k+=1
#         outq = await loop.run_in_executor(None, fake_transport.out_q.get)
#         await fake_transport.in_q.put(sym_rp)
#         print('outq', outq)
#         
# async def fake_producer_mkt_status(
#         loop: asyncio.BaseEventLoop,       
#         fake_transport: FakeTransport, 
#         sym_count = 1,
#     ):
#     # market subscription status
#     for i in range(sym_count):
#         mkt_status = build_market_data_subscription_statuses_server_msg(
#             ServerMsg(),
#             contract_id= 0,
#             )
#         print("[producer] mkt_status", mkt_status)
#         from EC_API.protocol.cqg.router_util import extract_router_keys
#         print("[producer] key extraction", extract_router_keys(mkt_status))
#         return
#         outq = await loop.run_in_executor(None, fake_transport.out_q.get)
#         print('[producer] outq', outq)
# 
#         await fake_transport.in_q.put(mkt_status)
#         
# async def fake_producer_data( 
#         loop: asyncio.BaseEventLoop,       
#         fake_transport: FakeTransport, 
#         sym_count = 4,
#         nums = 500, 
#         seed = 10,
#         start_id = 10
#     ) -> None:
#     rng = random.Random(seed)
# # =============================================================================
# #     
# #     k = start_id 
# #     # symbol res report
# #     for i in range(sym_count):
# #         sym_rp = build_symbol_resolution_report_server_msg(
# #             ServerMsg(), 
# #             report_id = k,
# #             cotract_id = i,
# #             contract_symbol = f"FakeSymbol_{i}",
# #             )
# #         k+=1
# #         outq = await loop.run_in_executor(None, fake_transport.out_q.get)
# #         await fake_transport.in_q.put(sym_rp)
# #         print('outq', outq)
# #          
# #     mkt_status = build_market_data_subscription_statuses_server_msg(
# #         ServerMsg(),
# #         contract_id= 0,
# #         )
# #     print("[producer] mkt_status", mkt_status)
# # 
# #     # market subscription status
# #     for i in range(sym_count):
# #         mkt_status = build_market_data_subscription_statuses_server_msg(
# #             ServerMsg(),
# #             contract_id= 0,
# #             )
# #         print("[producer] mkt_status", mkt_status)
# #         from EC_API.protocol.cqg.router_util import extract_router_keys
# #         print("[producer] key extraction", extract_router_keys(mkt_status))
# #         return
# #         outq = await loop.run_in_executor(None, fake_transport.out_q.get)
# #         print('[producer] outq', outq)
# # 
# #         await fake_transport.in_q.put(mkt_status)
# # 
# #     return  
# #         
# # =============================================================================
#     # real-time data 
#     for _ in range(nums):
#         msg = build_real_time_market_data_server_msg(
#             ServerMsg(),
#             contract_id = 0 #rng.randrange(0, sym_count)
#             )
#         await fake_transport.in_q.put(msg)
#     
#         
#     # unsubscription
#     for i in range(sym_count):
#         unsub_msg = build_market_data_subscription_statuses_server_msg(
#             ServerMsg(),
#             contract_id = 0,
#             level = MktDSub.Level.LEVEL_NONE
#             )
#         await loop.run_in_executor(None, fake_transport.out_q.get)
#         await fake_transport.in_q.put(unsub_msg)
# 
# =============================================================================
# =============================================================================
# @pytest.mark.asyncio
# async def test_monitor_data_CQG_yield_one_item_valid() -> None:
#     conn = ConnectCQG(
#         "host_name", 
#         "user_name", 
#         "password", 
#         immediate_connect= False, 
#         client = FakeCQGClient()
#         )
#     fake_transport = FakeTransport()
#     conn._transport = fake_transport
#     conn._timeout = 0.1
#     async with conn:        
#         MD = MonitorDataCQG(conn)
#         loop = asyncio.get_running_loop()
# 
#         # Setup Logon state
#         conn._state_mgr.transition_to(ConnectionState.CONNECTED_LOGON)
#         result = await asyncio.gather(
#             fake_consumer(MD, MktDataSubLevel.LEVEL_TRADES_BBA, 'FakeSymbol_0'),
#             FakeDataServer(conn, loop).run()
#             )  
#         print(result)
#         #assert 1 ==0 
#         conn._state_mgr.transition_to(ConnectionState.CONNECTED_LOGOFF)
# 
#         
# @pytest.mark.asyncio
# async def test_stops_on_event() -> None:...
# 
# @pytest.mark.asyncio
# async def test_monitor_data_CQG_stream_valid():
#     conn = ConnectCQG(
#         "host_name", "user_name", "password", 
#         immediate_connect = False, 
#         client = FakeCQGClient()
#         )
#     fake_transport = FakeTransport()
#     conn._transport = fake_transport
#     conn._timeout = 0.01
#         
#     async with conn:
#         MD = MonitorDataCQG(conn)
#         loop = asyncio.get_running_loop()
# 
#         # Setup Logon state
#         conn._state_mgr.transition_to(ConnectionState.CONNECTED_LOGON)
#         conn._state_mgr.transition_to(ConnectionState.CONNECTED_LOGOFF)
# =============================================================================

# =============================================================================
# @pytest.mark.asyncio
# async def test_monitor_data_CQG_yield_one_item_valid() -> None:
#     async with ConnectCQG(
#         "host_name", 
#         "user_name", 
#         "password", 
#         immediate_connect= False, 
#         client = FakeCQGClient()
#         ) as conn:
#         fake_transport = FakeTransport()
#         conn._transport = fake_transport
#         conn._timeout = 0.1
#         
#         MD = MonitorDataCQG(conn)
#         loop = asyncio.get_running_loop()
# 
#         # Setup Logon state
#         conn._state_mgr.transition_to(ConnectionState.CONNECTED_LOGON)
#         
#         # Preload. Otherwise the consumer outrun the producer
#         await fake_producer_symres(loop, fake_transport)
#         
#         await fake_producer_mkt_status(loop, fake_transport)
#         return
#         # load and consume data
#         result = await asyncio.gather(
#             fake_consumer(MD, MktDataSubLevel.LEVEL_TRADES_BBA, 'FakeSymbol_0'),
#             fake_producer_data(loop, fake_transport, sym_count = 1, 
#                           nums=100, start_id = conn._rid+1)
#             )  
#         
#         # tests
#         print("consumer", result)
#         assert len(result) == 10
#         assert 1 == 0
#             
# =============================================================================
    
