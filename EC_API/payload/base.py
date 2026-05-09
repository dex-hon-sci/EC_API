#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 14 19:37:54 2025

@author: dexter
"""
# Python imports
import logging
from datetime import timezone, datetime, timedelta
from dataclasses import dataclass, field
# EC_API imports
from EC_API.ordering.base import LiveOrder
from EC_API.payload.enums import PayloadStatus
from EC_API.ordering.enums import RequestType
from EC_API.payload.safety import PreTradeRiskCheck
from EC_API.ordering.trade_session import TradeSession
from EC_API.exceptions import ( 
    LiveOrderRequestError,
    LiveOrderTimeOutError,
    TradeSubscriptionMissingError,
    MissingSymbolResolutionError,
    MissingOrderIDError,
    RiskViolationError
    )
logger = logging.getLogger(__name__)

@dataclass(slots=True)
class Payload:
    """
    A vendor-agnoistic objects that contain the information needed for a 
    live order. 
    
    Payload only contains information about whether the order is sent or not,
    but not if the order has been filled or not.
    
    Upon instantiation, `Payload` objects perform a safety check for the 
    input parameters. The instantiation will fail if there are any illegal
    inputs.
    
    One Payload correspond to one order request.
    """
    order_request_type: RequestType = RequestType.NEW_ORDER
    order_info: dict = field(default_factory=dict)
    
    status: PayloadStatus = PayloadStatus.PENDING
    start_time: datetime = datetime.now(timezone.utc)\
                                    + timedelta(days=1)# In long text format
    end_time: datetime = datetime.now(timezone.utc)\
                                    + timedelta(days=2) # In long text format                                    
    risk_check: PreTradeRiskCheck | None = None
    
    def __post_init__(self) -> None:
        # Check the order instructions based on the order type
        # import checking classes and func specific for CQG type orders
        if self.risk_check is not None:
            try:
                self.risk_check.static_validate(self.order_info)
            except (KeyError, ValueError, AttributeError) as e:
                raise RiskViolationError(str(e))

class ExecutePayload:
    """
    A wrapper class for vendor-specific `LiveOrder` objects.
    
    This class is meant to route `Payload` data create `LiveOrder`-like 
    objects and perform their respective functions
    """
    # Execution object for CQG trade rounting connection
    def __init__(
            self, 
            payload: Payload,
            live_order: LiveOrder
        ):
        self.payload: Payload = payload
        self.live_order: LiveOrder = live_order # LiveOrder class, vendor-specific.
        self._trade_session: TradeSession = self.live_order._trade_session

        # Choose what enums are used for match cases in change payload status
        
    async def unload(self) -> None:
        """
        Sending order request base on vendor-specific format and logics.

        """
        # Only send payload that is pending.
        if self.payload.status == PayloadStatus.PENDING:
            try:
                await self.live_order.send(
                    request_type = self.payload.order_request_type, 
                    request_details = self.payload.order_info
                    )
                self.payload.status = PayloadStatus.SENT
                logger.info(
                    "Payload sent: %s %s",
                    self.payload.order_request_type,
                    self.payload.order_info.get('symbol_name', '')
                )
            except (TradeSubscriptionMissingError,
                    MissingSymbolResolutionError,
                    MissingOrderIDError) as e:
                self.payload.status = PayloadStatus.VOID
                logger.error("Payload blocked — setup error [%s]: %s", type(e).__name__, e)
            except LiveOrderTimeOutError as e:
                self.payload.status = PayloadStatus.VOID
                logger.warning(
                    "Payload timed out [%s %s]: %s",
                    self.payload.order_request_type,
                    self.payload.order_info.get('symbol_name', ''), e
                )
            except LiveOrderRequestError as e:
                self.payload.status = PayloadStatus.VOID
                logger.warning(
                    "Payload rejected [%s %s]: %s",
                    self.payload.order_request_type,
                    self.payload.order_info.get('symbol_name', ''), e
                )
        else:
            logger.warning(
                "Invalid Payload Status: Only pending payloads can be unloaded."
                )
        

    

    
