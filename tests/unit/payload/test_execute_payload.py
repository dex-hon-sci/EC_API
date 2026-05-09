#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 03:44:56 2026

@author: dexter
"""

# =============================================================================
# # ---- Error
# @pytest.mark.asyncio
# async def test_execute_payload_new_order_request_send_on_exception_returns_none(conn) -> None:
#     request_details = {
#         "symbol_name": "CLE",
#         "cl_order_id": "1231314",
#         "order_type": OrderType.LMT,
#         "duration": Duration.GTC,
#         "side": Side.BUY,
#         "qty": 2,
#         "is_manual": False,
#         "limit_price": 150,
#         "exec_instructions": ExecInstruction.NONE,
#     }
#     metadata = {'CLE': "something", "contract_id": 1}
# 
#     async with TradeSessionCQG(conn) as TS:
#         TS._symbol_registry.register('CLE', metadata)
#         TS._active_trade_subs[1] = [SubScope.ORDERS]
# 
#         result = await LiveOrderCQG(TS).send(
#             RequestType.NEW_ORDER,
#             request_details=request_details,
#         )
# 
#         assert result is None
#         assert TS.cl_to_chain == {}
#         assert TS._pending_chain_q == []
# =============================================================================
