#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 13 18:02:35 2025

@author: dexter
"""

import threading
import asyncio
import time
# Python Package imports
import pytest
# EC_API imports
from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg
from EC_API.transport.cqg.base import TransportCQG
from tests.unit.transport.proxy import FakeCQGClient

@pytest.mark.asyncio
async def test_transport_recv2async_queue() -> None:
    def _find_threads(prefix: str):
        return [t for t in threading.enumerate() if t.name.startswith(prefix)]

    # testing recieve 
    loop = asyncio.get_running_loop()
    fake_client = FakeCQGClient()
    transport = TransportCQG(
        host_name="demo_host",
        loop=loop,
        client=fake_client,  
    )
    transport.connect()
    transport.start()
    
    # Dummy results for testing receive functions in the transport layer
    msg1 = ServerMsg()
    msg1.logon_result.result_code = 0
    
    msg2 = ServerMsg()
    msg2.logon_result.result_code = 101
    
    msg3 = ServerMsg()
    msg3.logon_result.result_code = 102
    
    fake_client.push_incoming(msg1)
    fake_client.push_incoming(msg2)
    fake_client.push_incoming(msg3)
    
    for i, ele in enumerate([0, 101, 102]):
        recv_msg = await asyncio.wait_for(transport.recv(), timeout=1.0)
        assert recv_msg.logon_result.result_code == ele      
            
        res_code = recv_msg.logon_result.result_code        
        assert res_code == ele

    transport.stop()
    
    
    threads = [t for t in threading.enumerate() if t.name.startswith("TransportCQG")]
    deadline = time.monotonic() + 2.0
    while _find_threads("TransportCQG") and time.monotonic() < deadline:
        await asyncio.sleep(0.01)
    assert _find_threads("TransportCQG") == []
    assert fake_client.disconnected is True
