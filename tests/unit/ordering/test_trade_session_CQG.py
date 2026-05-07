import asyncio
import pytest
import logging
from datetime import datetime, timezone
from EC_API.ext.WebAPI.trade_routing_2_pb2 import TradeSubscriptionStatus as TrdSubStatus
from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg
from EC_API.connect.cqg.base import ConnectCQG
from EC_API.connect.enums import ConnectionState
from EC_API.ordering.enums import SubScope
from EC_API.ordering.cqg.trade_session import TradeSessionCQG
from EC_API.ordering.enums import SubScope
from tests.unit.fixtures.proxy_clients import FakeTransport
from tests.unit.fixtures.server_msg_builders_CQG import (
    build_trade_subscription_statuses_server_msg,
    build_trade_snapshot_completions_server_msg,
    build_real_time_market_data_server_msg,
    build_historical_orders_report_server_msg,
    build_symbol_resolution_report_server_msg
    )
from EC_API.exceptions import (
    TradeSessionRequestError, 
    TradeSessionTimeOutError,
    TradeSubscriptionMissingError
    )


async def _inject_after_send(
        fake_transport: FakeTransport,
        response: ServerMsg
    ) -> None:
    """Wait for an outbound message then inject a server response."""
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, fake_transport.out_q.get)
    await fake_transport.in_q.put(response)
    
def make_conn():
    conn = ConnectCQG(
        "host_name", "user_name", "password", 
        immediate_connect= False, client=object()
        )
    fake_transport = FakeTransport()
    conn._transport = fake_transport
    conn._timeout = 0.1
    return conn, fake_transport

# --- utility functions
@pytest.mark.asyncio
async def test_has_orders_scope_success() -> None:
    conn, ft = make_conn()
    TS = TradeSessionCQG(conn)
    TS._active_trade_subs[1] = [SubScope.ORDERS]
    conn.start()

    assert TS.has_orders_scope()
    await conn.stop()
    
@pytest.mark.asyncio
async def test_has_positions_scope_success() -> None:
    conn, ft = make_conn()
    TS = TradeSessionCQG(conn)
    TS._active_trade_subs[1] = [SubScope.POSITIONS]
    conn.start()

    assert TS.has_positions_scope()
    await conn.stop()
    
@pytest.mark.asyncio
async def test_has_orders_scope_fail() -> None:
    conn, ft = make_conn()
    TS = TradeSessionCQG(conn)
    TS._active_trade_subs[1] = []
    conn.start()

    assert not TS.has_orders_scope()
    await conn.stop()
    
@pytest.mark.asyncio
async def test_has_positions_scope_fail() -> None:
    conn, ft = make_conn()
    TS = TradeSessionCQG(conn)
    TS._active_trade_subs[1] = []
    conn.start()

    assert not TS.has_positions_scope()
    await conn.stop()

# --- CQG resolve symbol and unsubscribe symbol function calls
@pytest.mark.asyncio
async def test_resolve_symbol_success() -> None:
    conn, ft = make_conn()
    TS = TradeSessionCQG(conn)

    conn.start()

    rid = conn._rid + 1
    response = build_symbol_resolution_report_server_msg(
        ServerMsg(), report_id=rid, contract_symbol="CLE", cotract_id=3
    )

    result, _ = await asyncio.gather(
        TS.resolve_symbol("CLE"),
        _inject_after_send(ft, response),
    )

    assert result is not None
    assert len(result) == 1
    assert result[0]["contract_metadata"]["contract_symbol"] == "CLE"
    assert result[0]["contract_metadata"]["contract_id"] == 3
    assert result[0]["id"] == rid
    await conn.stop()

@pytest.mark.asyncio
async def test_resolve_symbol_timeout() -> None:
    conn, ft = make_conn()
    TS = TradeSessionCQG(conn)

    conn.start()

    with pytest.raises(TradeSessionRequestError):
        await TS.resolve_symbol("CLE")  # no server response injected

    await conn.stop()


@pytest.mark.asyncio
async def test_resolve_symbol_sends_correct_params() -> None:
    conn, ft = make_conn()
    TS = TradeSessionCQG(conn)

    conn.start()

    async def grab_and_respond() -> None:
        loop = asyncio.get_running_loop()
        client_msg = await loop.run_in_executor(None, ft.out_q.get)
        req = client_msg.information_requests[0]
        assert req.symbol_resolution_request.symbol == "NGF"
        assert req.subscribe == True
        response = build_symbol_resolution_report_server_msg(
            ServerMsg(), report_id=req.id, contract_symbol="NGF"
        )
        await ft.in_q.put(response)

    await asyncio.gather(TS.resolve_symbol("NGF"), grab_and_respond())
    await conn.stop()


# =============================================================================
# --- unsub_symbol tests
# =============================================================================

@pytest.mark.asyncio
async def test_unsub_symbol_success() -> None:
    conn, ft = make_conn()
    TS = TradeSessionCQG(conn)
    TS._symbol_registry.register("CLE", {'contract_id': 3})

    conn.start()

    rid = conn._rid + 1
    response = build_symbol_resolution_report_server_msg(
        ServerMsg(), report_id=rid, contract_symbol="CLE", cotract_id=3
    )

    result, _ = await asyncio.gather(
        TS.unsubscribe_symbol("CLE"),
        _inject_after_send(ft, response),
    )

    assert result is not None
    assert len(result) == 1
    assert result[0]["contract_metadata"]["contract_symbol"] == "CLE"
    await conn.stop()


@pytest.mark.asyncio
async def test_unsub_symbol_timeout() -> None:
    conn, ft = make_conn()
    TS = TradeSessionCQG(conn)
    TS._symbol_registry.register("CLE", {'contract_id': 3})

    conn.start()

    with pytest.raises(TradeSessionRequestError):
        await TS.unsubscribe_symbol("CLE")  # no server response injected
    await conn.stop()


@pytest.mark.asyncio
async def test_unsub_symbol_sends_subscribe_false() -> None:
    conn, ft = make_conn()
    TS = TradeSessionCQG(conn)
    TS._symbol_registry.register("CLE", {'contract_id': 3})

    conn.start()

    async def grab_and_respond() -> None:
        loop = asyncio.get_running_loop()
        client_msg = await loop.run_in_executor(None, ft.out_q.get)
        req = client_msg.information_requests[0]
        assert req.symbol_resolution_request.symbol == "CLE"
        assert req.subscribe == False
        response = build_symbol_resolution_report_server_msg(
            ServerMsg(), report_id=req.id, contract_symbol="CLE"
        )
        await ft.in_q.put(response)

    await asyncio.gather(TS.unsubscribe_symbol("CLE"), grab_and_respond())
    await conn.stop()
     

# --- CQG trade subscription function calls
@pytest.mark.asyncio
async def test_trade_subscription_request_valid()->None:
    conn,ft = make_conn()
    TS = TradeSessionCQG(conn)
    
    conn.start()
    conn._state_mgr.transition_to(ConnectionState.CONNECTED_LOGON)

    response1 = build_trade_subscription_statuses_server_msg(ServerMsg(), sub_id = 2)
    response2 = build_trade_snapshot_completions_server_msg(response1, sub_id = 2)
    
    result, _ = await asyncio.gather(
        TS.trade_subscription_request(2, SubScope.ORDERS),
        _inject_after_send(ft, response2)
        )    
    
    assert result is not None
    assert isinstance(result, tuple)
    assert len(result)==2
    
    assert isinstance(result[0], list)
    assert isinstance(result[1], list)

    assert result[0][0]['sub_id'] == 2
    assert result[0][0]['status_code'] == TrdSubStatus.StatusCode.STATUS_CODE_SUCCESS
    assert result[1][0]['sub_id'] == 2
    assert len(result[1][0]['sub_scopes']) == 4
    assert result[1][0]['sub_scopes'] == [1,2,3,4]
    await conn.stop()

@pytest.mark.asyncio
async def test_trade_subscription_request_builder_invalid() -> None:
    conn,ft = make_conn()
    TS = TradeSessionCQG(conn)
    conn.start()
    conn._state_mgr.transition_to(ConnectionState.CONNECTED_LOGON)
    
    with pytest.raises(TradeSessionRequestError):
        await TS.trade_subscription_request("2", SubScope.ORDERS) #<-- incorrect input
    await conn.stop()

@pytest.mark.asyncio
async def test_trade_subscription_request_timeout_invalid()->None:
    conn, ft = make_conn()
    TS = TradeSessionCQG(conn)
    conn.start()
    conn._state_mgr.transition_to(ConnectionState.CONNECTED_LOGON)
    
    with pytest.raises(TradeSessionTimeOutError): # No Server inputs
        await TS.trade_subscription_request(2, SubScope.ORDERS) 
    await conn.stop()
    
@pytest.mark.asyncio
async def test_unsubscribe_trade_request_valid()->None: 
    conn,ft = make_conn()
    TS = TradeSessionCQG(conn)
    TS._active_trade_subs[2] = {SubScope.ORDERS}

    conn.start()
    conn._state_mgr.transition_to(ConnectionState.CONNECTED_LOGON)

    response1 = build_trade_subscription_statuses_server_msg(ServerMsg(), sub_id = 2)
    
    result, _ = await asyncio.gather(
        TS.unsubscribe_trade_request(2, SubScope.ORDERS),
        _inject_after_send(ft, response1)
        )    
    assert result is not None
    assert isinstance(result[0], dict)

    assert result[0]['sub_id'] == 2
    assert result[0]['status_code'] == TrdSubStatus.StatusCode.STATUS_CODE_SUCCESS

    await conn.stop()

@pytest.mark.asyncio
async def test_unsubscribe_trade_request_builder_invalid() -> None:
    conn, ft = make_conn()
    TS = TradeSessionCQG(conn)
    TS._active_trade_subs[2] = {SubScope.ORDERS}

    conn.start()
    conn._state_mgr.transition_to(ConnectionState.CONNECTED_LOGON)

    with pytest.raises(TradeSubscriptionMissingError):
        await TS.unsubscribe_trade_request("2", SubScope.ORDERS)  # str instead of int
    await conn.stop()
    
@pytest.mark.asyncio
async def test_unsubscribe_trade_request_timeout_invalid() -> None:
    conn, ft = make_conn()
    TS = TradeSessionCQG(conn)
    TS._active_trade_subs[2] = {SubScope.ORDERS}
    
    conn.start()
    conn._state_mgr.transition_to(ConnectionState.CONNECTED_LOGON)

    with pytest.raises(TradeSessionTimeOutError):  # no server response injected
        await TS.unsubscribe_trade_request(2, SubScope.ORDERS)
    await conn.stop()
    
@pytest.mark.asyncio
async def test_trade_subscription_request_sub_id_already_in_use_invalid(caplog) -> None:
    conn, ft = make_conn()
    TS = TradeSessionCQG(conn)
    TS._active_trade_subs[2] = {SubScope.ORDERS}
    
    conn.start()
    with caplog.at_level(logging.WARNING, logger="EC_API.ordering.cqg.trade_session"):
        conn.start()
        conn._state_mgr.transition_to(ConnectionState.CONNECTED_LOGON)
        await TS.trade_subscription_request(2, SubScope.ORDERS)
        await asyncio.sleep(0.05)

    assert any("already in-use" in r.message for r in caplog.records)
    await conn.stop()

@pytest.mark.asyncio
async def test_request_historical_orders_valid() -> None:
    conn, ft = make_conn()
    conn._account_id = 12345
    TS = TradeSessionCQG(conn)
    conn.start()
    conn._state_mgr.transition_to(ConnectionState.CONNECTED_LOGON)

    rid = conn._rid + 1
    response = build_historical_orders_report_server_msg(
        ServerMsg(), report_id=rid, order_id="order_99", chain_order_id="chain_A"
    )

    from_date = datetime(2025, 1, 1, tzinfo=timezone.utc)
    to_date   = datetime(2025, 1, 31, tzinfo=timezone.utc)

    result, _ = await asyncio.gather(
        TS.request_historical_orders(from_date, to_date),
        _inject_after_send(ft, response),
    )

    assert result is not None
    orders = result.information_reports[0].historical_orders_report.order_statuses
    assert result.information_reports[0].id == rid
    assert orders[0].order_id == "order_99"
    assert orders[0].chain_order_id == "chain_A"
    await conn.stop()


@pytest.mark.asyncio
async def test_request_historical_orders_timeout() -> None:
    conn, ft = make_conn()
    conn._account_id = 12345
    TS = TradeSessionCQG(conn)
    conn.start()
    conn._state_mgr.transition_to(ConnectionState.CONNECTED_LOGON)

    from_date = datetime(2025, 1, 1, tzinfo=timezone.utc)
    to_date   = datetime(2025, 1, 31, tzinfo=timezone.utc)

    with pytest.raises(TradeSessionTimeOutError):
        await TS.request_historical_orders(from_date, to_date)

    await conn.stop()


@pytest.mark.asyncio
async def test_request_historical_orders_sends_correct_params() -> None:
    conn, ft = make_conn()
    conn._account_id = 12345
    TS = TradeSessionCQG(conn)
    conn.start()
    conn._state_mgr.transition_to(ConnectionState.CONNECTED_LOGON)

    from_date = datetime(2025, 1, 1, tzinfo=timezone.utc)
    to_date   = datetime(2025, 1, 31, tzinfo=timezone.utc)

    async def grab_and_respond() -> None:
        loop = asyncio.get_running_loop()
        client_msg = await loop.run_in_executor(None, ft.out_q.get)
        req = client_msg.information_requests[0]
        assert req.historical_orders_request.account_ids[0] == 12345
        assert req.historical_orders_request.from_date == int(from_date.timestamp())
        assert req.historical_orders_request.to_date   == int(to_date.timestamp())
        response = build_historical_orders_report_server_msg(
            ServerMsg(), report_id=req.id
        )
        await ft.in_q.put(response)

    await asyncio.gather(
        TS.request_historical_orders(from_date, to_date),
        grab_and_respond(),
    )
    await conn.stop()
