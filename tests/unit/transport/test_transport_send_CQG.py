#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 13 17:56:37 2025

@author: dexter
"""
import threading
import asyncio
import time
# Python Package imports
import pytest
# EC_API imports
from EC_API.ext.WebAPI.webapi_2_pb2 import ClientMsg
from EC_API.transport.cqg.base import TransportCQG
from tests.unit.fixtures.proxy_clients import FakeCQGClient

@pytest.mark.asyncio
async def test_transport_send2queue():
    def _find_threads(prefix: str):
        return [t for t in threading.enumerate() if t.name.startswith(prefix)]

    # testing send 
    loop = asyncio.get_running_loop()
    fake_client = FakeCQGClient()
    transport = TransportCQG(
        host_name="demo_host",
        loop=loop,
        client=fake_client,  
    )
    transport.connect()
    transport.start()
    
    # Build a dummy client message (no real fields needed for this test)
    msg1 = ClientMsg()
    msg1.logon.user_name = "TEST1"
    msg1.logon.private_label = "test_send_forwards_1"
    
    msg2 = ClientMsg()
    msg2.logon.user_name = "TEST2"
    msg2.logon.private_label = "test_send_forwards_2"
    
    msg3 = ClientMsg()
    msg3.logon.user_name = "TEST3"
    msg3.logon.private_label = "test_send_forwards_3"

    private_labels = [f"test_send_forwards_{i+1}" for i in range(3)]
        
    for i, msg in enumerate([msg1, msg2, msg3]):
        await transport.send(msg)
    
        duration = time.monotonic() + 1.0
        while len(fake_client.sent_messages) < i+1 and time.monotonic() < duration:
            await asyncio.sleep(0.01)
            
        label = fake_client.sent_messages[i].logon.private_label
        assert label == private_labels[i]
        
    transport.stop()
    threads = [t for t in threading.enumerate() if t.name.startswith("TransportCQG")]
    deadline = time.monotonic() + 2.0
    while _find_threads("TransportCQG") and time.monotonic() < deadline:
        await asyncio.sleep(0.01)
    assert _find_threads("TransportCQG") == []
    assert fake_client.disconnected is True