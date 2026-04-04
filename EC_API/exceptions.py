class EC_APIError(Exception):
    """Base case for EC_API Error"""
    
# --- Transport ---
class TransportError(EC_APIError): pass

class TransportSendError(TransportError):
    def __init__(self, message: str):
        super().__init__(message)

class TransportRecvError(TransportError):
    def __init__(self, message: str):
        super().__init__(message)
        
class TransportConnectError(TransportError):
    def __init__(self, message: str):
        super().__init__(message)

class TransportDisconnectError(TransportError):
    def __init__(self, message: str):
        super().__init__(message)

# --- Builders ---
class MsgBuilderError(EC_APIError):
    def __init__(self, message: str):
        super().__init__(message)

# --- Parsers ---
class MsgParserError(EC_APIError):
    def __init__(self, message: str):
        super().__init__(message)

# --- Routers ---
class RoutingError(EC_APIError):...

class DuplicateRouterKeyError(RoutingError):
    def __init__(self, message: str):
        super().__init__(message)

class UnknownRouterKeyError(RoutingError):
    def __init__(self, message: str):
        super().__init__(message)
        
class UnknownSubscriptionError(RoutingError):
    def __init__(self, message: str):
        super().__init__(message)
        
class SubscriptionQueueMismatchError(RoutingError):
    def __init__(self, message: str):
        super().__init__(message)
        
class MaxSymbolsExceededError(RoutingError):
    def __init__(self, message: str):
        super().__init__(message)
        
class MaxSubscribersExceededError(RoutingError):
    def __init__(self, message: str):
        super().__init__(message)
        
class InvalidDroppingPolicy(RoutingError):
    def __init__(self, message: str):
        super().__init__(message)
# -----------
# --- Connect
class ConnectError(EC_APIError):...

class ConnectCancelledError(ConnectError):
    def __init__(self, message: str):
        super().__init__(message)

class DisconnectError(ConnectError):
    def __init__(self, message: str):
        super().__init__(message)

class AuthError(ConnectError):
    def __init__(self, message: str):
        super().__init__(message)

# --- Monitor
class MonitorError(EC_APIError):...

# --- Ordering
class TradeSessionError(EC_APIError):...

# --- Payload
class PayloadError(EC_APIError):...

# Safety check error

# --- OpStrategy
class OpStrategyError(EC_APIError):...
