import pytest
import asyncio
import random
from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg, ClientMsg
from EC_API.ext.WebAPI.market_data_2_pb2 import MarketDataSubscription as MktDSub
from EC_API.connect.enums import ConnectionState
from EC_API.connect.cqg.base import ConnectCQG
from EC_API.monitor.enums import MktDataSubLevel
from EC_API.monitor.cqg.realtime_data import MonitorDataCQG
from EC_API._typing import ParsedRTMDCQG
from tests.unit.fixtures.proxy_clients import (
    FakeTransport, 
    FakeCQGClient
    )
from tests.unit.fixtures.server_msg_builders_CQG import (
    build_symbol_resolution_report_server_msg,
    build_market_data_subscription_statuses_server_msg,
    build_real_time_market_data_server_msg
    )

def client_msg_type(client_msg: ClientMsg) -> list[str]:
    return [fd.name for fd, val in client_msg.ListFields()]

class FakeDataServer:
    def __init__(self, conn: ConnectCQG, loop):
        self.conn = conn
        self.transport = self.conn._transport
        self.loop = loop
        
        self._server_stop_evt = asyncio.Event()
        
    async def response_logic(self, msg: ClientMsg):
        msg_name = client_msg_type(msg)[0] 
        # we assume client dispatch message one at a time
        match msg_name:
            case "information_requests": # In this context
                await self._sym_res_response(msg)
                 
            case "market_data_subscriptions":
                await self._mkt_data_status_response(msg)
                count = 0
                #while not self.conn._stop_evt():
                while count < 100:
                    await self._mkt_data_stream_responses(msg)
                    count+=1
            case _:
                pass
        
    async def _sym_res_response(self, msg: ClientMsg) -> None:
        sym = msg.information_requests[0].symbol_resolution_request.symbol
        
        sym_rp = build_symbol_resolution_report_server_msg(
            ServerMsg(), 
            report_id = msg.information_requests[0].id,
            cotract_id = int(sym.split("_")[-1]),
            contract_symbol = sym,
            )
        #outq = await self.loop.run_in_executor(None, self.transport.out_q.get)
        await self.transport.in_q.put(sym_rp)
        #print('outq', outq)
        
    async def _mkt_data_status_response(self, client_msg: ClientMsg):
        for mkt_sub in client_msg.market_data_subscriptions:
            mkt_status = build_market_data_subscription_statuses_server_msg(
                ServerMsg(),
                contract_id= mkt_sub.contract_id,
                level = mkt_sub.level
                )
            print("[producer] mkt_status", mkt_status)
            from EC_API.protocol.cqg.router_util import extract_router_keys
            print("[producer] key extraction", extract_router_keys(mkt_status))
            
            #outq = await self.loop.run_in_executor(None, self.transport.out_q.get)
            #print('[producer] outq', outq)
    
            await self.transport.in_q.put(mkt_status)
        
    async def _mkt_data_stream_responses(self, client_msg: ClientMsg):
        
        for mkt_sub in client_msg.market_data_subscriptions:
            server_msg = build_real_time_market_data_server_msg(
                ServerMsg(),
                contract_id = mkt_sub.contract_id
                )
            await self.transport.in_q.put(server_msg)

        
    async def run(self):
        # while loop, scan the transport
        while not self._server_stop_evt.is_set():
            client_msg = await self.loop.run_in_executor(None, self.transport.out_q.get)
            #client_msg = self.transport.out_q.get()
            await self.response_logic(client_msg)
            
            if client_msg.market_data_subscriptions:
                if client_msg.market_data_subscriptions[0].level == MktDSub.Level.LEVEL_NONE:
                    break
            
        

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
@pytest.mark.asyncio
async def test_monitor_data_CQG_yield_one_item_valid() -> None:
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
        result = await asyncio.gather(
            fake_consumer(MD, MktDataSubLevel.LEVEL_TRADES_BBA, 'FakeSymbol_0'),
            FakeDataServer(conn, loop).run()
            )  
        print(result)
        #assert 1 ==0 
        conn._state_mgr.transition_to(ConnectionState.CONNECTED_LOGOFF)

        
@pytest.mark.asyncio
async def test_stops_on_event() -> None:...

@pytest.mark.asyncio
async def test_monitor_data_CQG_stream_valid():
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
    
# test for no logon
# test for error in realtime_requests..
# test for error in unsubscribe requests...