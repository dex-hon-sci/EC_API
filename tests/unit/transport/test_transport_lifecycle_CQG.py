#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 13 18:02:43 2025

@author: dexter
"""

import threading
import asyncio
import time
# Python Package imports
import pytest
# EC_API imports
from EC_API.transport.cqg.base import TransportCQG
from tests.unit.transport.proxy import FakeCQGClient

@pytest.mark.asyncio
async def test_transport_lifecycle() -> None:
    # Lifecycle - After connect() and start(), is one IO thread running?
    # Lifecycle - After stop(), does that IO thread exit?
    # Lifecycle - Is the CQG client disconnected cleanly?
    def _find_threads(prefix: str):
        return [t for t in threading.enumerate() if t.name.startswith(prefix)]
    
    # test if Transport can start and stop
    loop = asyncio.get_running_loop()
    fake_client = FakeCQGClient()
    transport = TransportCQG(
        host_name="demo_host",
        loop=loop,
        client=fake_client
    )
    transport.connect()
    transport.start()
    
    threads = _find_threads("TransportCQG")
    assert any("send_loop" in t.name for t in threads)
    assert any("recv_loop" in t.name for t in threads)
    transport.stop()

    deadline = time.monotonic() + 2.0
    while _find_threads("TransportCQG") and time.monotonic() < deadline:
        await asyncio.sleep(0.01)
    assert _find_threads("TransportCQG") == []
    assert fake_client.disconnected is True