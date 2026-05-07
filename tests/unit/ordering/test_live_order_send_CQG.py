import asyncio
import pytest
from EC_API.connect.cqg.base import ConnectCQG
from EC_API.ordering.cqg.live_order import LiveOrderCQG
from EC_API.ordering.cqg.trade_session import TradeSessionCQG
from EC_API.exceptions import (
    LiveOrderTimeOutError,
    LiveOrderRequestError
    )
from tests.unit.fixtures.proxy_clients import FakeCQGClient