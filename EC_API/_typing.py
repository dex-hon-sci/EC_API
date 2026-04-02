import numpy as np
from typing import TypeVar
from typing import Any, Callable
#from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg


# Generic types
Typ = TypeVar("T")
Func = TypeVar("F", bound=Callable[..., Any])
# Config

# Arrays
Array = np.ndarray  # ready to be used for n-dim data
Array1D = np.ndarray
Array2D = np.ndarray
Array3D = np.ndarray
Record = np.void
RecordArray = np.ndarray

# --- MsgType
ServerMsgType = TypeVar("T")
ClientMsgType = TypeVar("T")
# --- Routers
# (msg_family, msg_type, id_field_name, id)
RouterKey = tuple[str, str, str, int|str]
type Extractor_func = Callable[ServerMsgType]

# (msg_family, msg_type, is_repeated, is_)
KeyHit = tuple[str, int, bool, bool]

# --- Parsers
type Parser_func = Callable[ServerMsgType]

# --- Connect
LogonResultType = dict[str, Any]
LogoffResultType = dict[str, Any]
RestoreResultType = dict[str, Any]
PongType = tuple[str, str, int, int] # ('pong', token, ping_time, pong_time)
# --- Monitor
# contract_id, O, H, L, C, volume_significand, volume_exponent, volume_significand, correct_price_scale
MarketValueType = tuple[int, int, int, int, int, int, int]

# contract_id, quote_utc_time, type, scaled_price, scaled_source_price
QuotesValueType = tuple[int, int, Any, int, int]

# --- LiveOrder
