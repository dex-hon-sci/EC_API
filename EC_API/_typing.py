from typing import TypeVar
from typing import Any, Callable

# --- MsgType
ServerMsgType = TypeVar("T")
ClientMsgType = TypeVar("T")

# --- Routers
RouterKey = tuple[str, str, str, int|str] # (msg_family, msg_type, id_field_name, id)
KeyHit = tuple[str, int, bool, bool] # (msg_family, msg_type, is_repeated, is_)

type Extractor_func = Callable[ServerMsgType]

# --- Builders
type Builder_func = Callable[Any, ClientMsgType]

# --- Parsers
type Parser_func = Callable[Any, ServerMsgType]

# --- Connect
LogonResultType = dict[str, Any]
LogoffResultType = dict[str, Any]
RestoreResultType = dict[str, Any]
PongType = tuple[str, str, int, int] # ('pong', token, ping_time, pong_time)
#--- Connect:metadata
ContractMetaDataType = list[dict[str, str]]

# --- Monitor
# (contract_id, O, H, L, C, volume_significand, volume_exponent, volume_significand, correct_price_scale)
MarketValueType = tuple[int, int, int, int, int, int, int]

# (contract_id, quote_utc_time, type, scaled_price, scaled_source_price)
QuotesValueType = tuple[int, int, Any, int, int]

# --- LiveOrder
