import asyncio
from EC_API.channel.redis import RedisChannel
from EC_API.connect.cqg.base import ConnectCQG
from EC_API.ordering.cqg.trade_session import TradeSessionCQG
from EC_API.ordering.cqg.live_order import LiveOrderCQG
from EC_API.ordering.enums import RequestType, SubScope
from EC_API.payload.base import Payload, ExecutePayload
from EC_API.payload.safety import PreTradeRiskCheck


HOST_NAME, USR_NAME, PASSWORD, ACCOUNT_ID = 0, 0, 0

class TradeEngineCQG:
    def __init__(self, channel_cfg_addr: str, pretraderisk_cfg_addr:str):
        # ---- IPC Channel setting ----
        self.channel = RedisChannel(channel_cfg_addr)
        
        # ---- Sessions setting ----
        self.conn = ConnectCQG(HOST_NAME, USR_NAME, PASSWORD, ACCOUNT_ID)
        self.trade_session = TradeSessionCQG(self.conn)
        
        # ---- Risk checks ----
        self.PREC = PreTradeRiskCheck('cqg')
        self.PREC.load(pretraderisk_cfg_addr)
        
        # ---- Engine property ----
        self.order_info_in_streams = list()
        self._stop_evt = asyncio.Event()
     
    # -------
    def add_in_stream(self):...
    def remove_in_stream(self):...
    # ------- Engine functions
    async def _package_and_send(self, order_type: RequestType, order_info: dict):
        async with self.trade_session as TS:
            PL = Payload(
              order_request_type = order_type,
              order_info = order_info,
              check_method = self.PREC # Static risk check done upon creation
              )
            await TS.trade_subscription_request(sub_id=1, sub_scope = SubScope.ORDERS)
            await TS.resolve_symbol(order_info['symbol_name']) 
            await ExecutePayload(live_order=LiveOrderCQG(TS)).unload(PL)

    async def _send_order_loop(self):
        while not self._stop_evt:
            # Continuous listening to the latest order instruction from redis stream
            msg = await self.channel.listen('order_info:WTI') 
            
            # If there is something, an event is triggered
            if msg is None:
                continue
            # package and send (fire and forget)
            order_type, order_info = msg
            await self._package_and_send(order_type, order_info)
      
    # -------- Engine LifeCycle
    async def _setup(self):...
    async def start(self):...
    async def stop(self):...
                
    async def run(self):
        self.conn.start()
        self._engine_task = asyncio.create_task(self._send_order_loop())

        await self._engine_task