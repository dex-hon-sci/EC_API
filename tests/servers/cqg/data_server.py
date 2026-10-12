import asyncio
from asyncio import AsyncIterator
from typing import Optional, Literal
import websockets
from websockets.asyncio.server import serve, ServerConnection
from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg, ClientMsg
from tests.servers.tape import SourceTape, GBMTape
from tests.servers.ws_server_base import WSserver
from tests.servers.brains import ServerBrain
from tests.servers.cqg.data_server_brain import FakeDataServerBrainCQG

class MsgFormatterCQG:
    def __init__(self):...
RpcAction = tuple[Literal["rpc"], ServerMsg]
StreamAction = tuple[Literal["stream"], AsyncIterator[ServerMsg]]
BrainAction = RpcAction | StreamAction

class FakeExchangeDataServerCQG:
    def __init__(
            self, 
            host: int, port: int,
            #ws_server: WSserver,
            tape: SourceTape,
            brain: ServerBrain
        ):
        self.tape: Optional[SourceTape] = tape
        self.brain: Optional[ServerBrain] = brain
        
        self.ws_server: WSserver = WSserver(host, port, self.handler)
        self.stop_evt: asyncio.Event = asyncio.Event()
    
    async def response_logic(self, msg: ClientMsg, **kwargs):
        return await self.brain.response_logic(msg, **kwargs)
    
    async def handler(self, conn: ServerConnection):
        while not self.stop_evt.is_set():
            try:
               msg = await conn.recv()
               server_msg = await self.response_logic(msg)
               await conn.send(server_msg.SerializeToString())
               
            except websockets.exceptions.ConnectionClosed:
                break
    # --- Streaming
    async def spawn_stream(self): ...
    async def stream_task(self, tape):...
        
    # --- Lifecycle
    async def start(self):
        # initialise WS server layer
        await self.ws_server.start()
        
        # inintialise Server Brain
        
    async def stop(self):
        await self.ws_server.stop()