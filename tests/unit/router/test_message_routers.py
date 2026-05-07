#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 17:56:37 2026

@author: dexter
"""
import asyncio
import pytest
from EC_API.transport.routers import MessageRouter
from EC_API.exceptions import DuplicateRouterKeyError

@pytest.mark.asyncio
async def test_key_register_valid() -> None:
    key1 = ("msg_family_1", "msg_type_A", "request_id", 12)
    key2 = ("msg_family_2", "msg_type_B", "id", "id_1")
    
    MR = MessageRouter()
    fut1 = MR.register_key(key1)
    fut2 = MR.register_key(key2)
    
    assert MR.pending_count == 2
    assert list(MR.pending.keys())[0] == key1
    assert list(MR.pending.keys())[1] == key2
    assert isinstance(fut1, asyncio.Future)
    assert isinstance(fut2, asyncio.Future)    
    assert MR.pending[key1].done() == False
    assert MR.pending[key2].done() == False
    
@pytest.mark.asyncio
async def test_register_key_duplicate_router_key_invalid() -> None:
    key1 = ("msg_family_1", "msg_type_A", "request_id", 12)

    MR = MessageRouter()
    MR.register_key(key1)
    with pytest.raises(DuplicateRouterKeyError):
        MR.register_key(key1)

@pytest.mark.asyncio
async def test_on_message_valid() -> None:
    key1 = ("msg_family_1", "msg_type_A", "request_id", 12)
    key2 = ("msg_family_2", "msg_type_B", "id", "id_1")
    
    MR = MessageRouter()
    fut1 = MR.register_key(key1)
    fut2 = MR.register_key(key2)

    MR.on_message(key1, {"Message_1": "Content_1"})
    assert MR.pending_count == 1
    assert fut1.done() is True
    res1 = await asyncio.wait_for(fut1, timeout=1.0)
    assert res1 ==  {"Message_1": "Content_1"}
    
    MR.on_message(key2, {"Message_2": "Content_2"})
    assert MR.pending_count == 0
    assert fut2.done() is True
    res2 = await asyncio.wait_for(fut2, timeout=1.0)
    assert res2 ==  {"Message_2": "Content_2"}       
  
@pytest.mark.asyncio 
async def test_fail_all_valid() -> None:
    key1 = ("msg_family_1", "msg_type_A", "request_id", 12)
    key2 = ("msg_family_2", "msg_type_B", "id", "id_1")
    
    MR = MessageRouter()
    fut1 = MR.register_key(key1)
    fut2 = MR.register_key(key2)
    
    exc = RuntimeError("connection lost")
    MR.fail_all(exc)
    
    assert fut1.done()
    assert fut2.done()
    
    with pytest.raises(RuntimeError, match="connection lost"):
        await fut1

    with pytest.raises(RuntimeError, match="connection lost"):
        await fut2

    assert MR.pending_count == 0

@pytest.mark.asyncio
async def test_fail_all_does_not_override_completed_futures() -> None:
    mr = MessageRouter()

    key = ("family", "typeA", "request_id", 1)
    fut = mr.register_key(key)

    # Complete it normally
    mr.on_message(key, "OK")

    assert fut.done()
    assert fut.result() == "OK"

    # Now call fail_all
    mr.fail_all(RuntimeError("should not affect"))

    # Should still have original result
    assert fut.result() == "OK"
    
@pytest.mark.asyncio
async def test_fail_all_ignores_cancelled_futures() -> None:
    mr = MessageRouter()

    key = ("family", "typeA", "request_id", 1)
    fut = mr.register_key(key)

    fut.cancel()

    # Should not crash
    mr.fail_all(RuntimeError("connection lost"))

    # Cancelled future should stay cancelled
    assert fut.cancelled()
    
# --- Register racing keys tests
@pytest.mark.asyncio
async def test_register_racing_keys_returns_future() -> None:
    keys = [("fam", "type", "rid", 1), ("fam", "type", "rid", 2)]

    mr = MessageRouter()
    final_fut = mr.register_racing_keys(keys)

    assert isinstance(final_fut, asyncio.Future)
    assert not final_fut.done()

@pytest.mark.asyncio
async def test_register_racing_keys_all_sub_keys_in_pending() -> None:
    key1 = ("fam", "type", "rid", 1)
    key2 = ("fam", "type", "rid", 2)
    key3 = ("fam", "type", "rid", 3)

    mr = MessageRouter()
    mr.register_racing_keys([key1, key2, key3])

    assert mr.pending_count == 3
    assert key1 in mr.pending
    assert key2 in mr.pending
    assert key3 in mr.pending

@pytest.mark.asyncio
async def test_register_racing_keys_winner_sets_final_result() -> None:
    key1 = ("fam", "type", "rid", 1)
    key2 = ("fam", "type", "rid", 2)
    key3 = ("fam", "type", "rid", 3)

    mr = MessageRouter()
    final_fut = mr.register_racing_keys([key1, key2, key3])

    mr.on_message(key2, {"winner": "key2"})

    result = await asyncio.wait_for(final_fut, timeout=1.0)
    assert result == {"winner": "key2"}

@pytest.mark.asyncio
async def test_register_racing_keys_only_first_winner_counts() -> None:
    key1 = ("fam", "type", "rid", 1)
    key2 = ("fam", "type", "rid", 2)

    mr = MessageRouter()
    final_fut = mr.register_racing_keys([key1, key2])

    mr.on_message(key1, "first")
    mr.on_message(key2, "second")  # should be a no-op; key2 was cancelled

    result = await asyncio.wait_for(final_fut, timeout=1.0)
    assert result == "first"

@pytest.mark.asyncio
async def test_register_racing_keys_losers_cancelled_after_win() -> None:
    key1 = ("fam", "type", "rid", 1)
    key2 = ("fam", "type", "rid", 2)
    key3 = ("fam", "type", "rid", 3)

    mr = MessageRouter()
    sub_futs = {k: mr.pending.get(k) for k in []}  # capture after registration
    mr.register_racing_keys([key1, key2, key3])
    loser_fut2 = mr.pending[key2]
    loser_fut3 = mr.pending[key3]

    mr.on_message(key1, "winner")

    # give the event loop a tick to process callbacks
    await asyncio.sleep(0)

    assert loser_fut2.cancelled()
    assert loser_fut3.cancelled()

@pytest.mark.asyncio
async def test_register_racing_keys_losers_cancelled_and_pending_cleared() -> None:
    key1 = ("fam", "type", "rid", 1)
    key2 = ("fam", "type", "rid", 2)

    mr = MessageRouter()
    mr.register_racing_keys([key1, key2])
    loser = mr.pending[key2]

    mr.on_message(key1, "winner")
    await asyncio.sleep(0)  # runs _on_sub_fut_done → cancels key2
    await asyncio.sleep(0)  # runs key2's _cleanup → pops from pending

    assert loser.cancelled()
    assert mr.pending_count == 0

@pytest.mark.asyncio
async def test_register_racing_keys_single_key() -> None:
    key1 = ("fam", "type", "rid", 1)

    mr = MessageRouter()
    final_fut = mr.register_racing_keys([key1])

    mr.on_message(key1, "only")

    result = await asyncio.wait_for(final_fut, timeout=1.0)
    assert result == "only"

@pytest.mark.asyncio
async def test_register_racing_keys_empty_list() -> None:
    mr = MessageRouter()
    final_fut = mr.register_racing_keys([])

    assert isinstance(final_fut, asyncio.Future)
    assert not final_fut.done()
    assert mr.pending_count == 0

@pytest.mark.asyncio
async def test_register_racing_keys_duplicate_pre_existing_key_raises() -> None:
    key1 = ("fam", "type", "rid", 1)

    mr = MessageRouter()
    mr.register_key(key1)  # pre-register key1

    with pytest.raises(DuplicateRouterKeyError):
        mr.register_racing_keys([key1, ("fam", "type", "rid", 2)])

@pytest.mark.asyncio
async def test_register_racing_keys_duplicate_within_list_raises() -> None:
    key1 = ("fam", "type", "rid", 1)

    mr = MessageRouter()
    with pytest.raises(DuplicateRouterKeyError):
        mr.register_racing_keys([key1, key1])

@pytest.mark.asyncio
async def test_register_racing_keys_external_cancel_of_sub_does_not_set_final() -> None:
    key1 = ("fam", "type", "rid", 1)
    key2 = ("fam", "type", "rid", 2)

    mr = MessageRouter()
    final_fut = mr.register_racing_keys([key1, key2])
    sub_fut1 = mr.pending[key1]

    sub_fut1.cancel()  # cancel sub externally, not via on_message
    await asyncio.sleep(0)

    assert not final_fut.done()  # external cancel should not propagate to final_fut
