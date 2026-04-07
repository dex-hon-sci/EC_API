class EC_APIError(Exception):
    """Base case for EC_API Error"""
    
# --- State Control ---
class StateControlError(EC_APIError):...

class StartStateError(StateControlError):
    def __init__(self, message: str):
        super().__init__(message)
        
class InvalidCurrentStateError(StateControlError):
    def __init__(self, message: str):
        super().__init__(message)

class InvalidNextStateError(StateControlError):
    def __init__(self, message: str):
        super().__init__(message)
    
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
        
# --- Symbol Registry ---
class SymbolRegistryError(EC_APIError):...

class SymbolNotInRegistryError(SymbolRegistryError):
    def __init__(self, message: str):
        super().__init__(message)

class MetaDataMissingError(SymbolRegistryError):
    def __init__(self, message: str):
        super().__init__(message)

class DuplicateSymbolError(SymbolRegistryError):
    def __init__(self, message: str):
        super().__init__(message)

# --- Subscription Manager ---
class SubscriptionError(EC_APIError):...

# ----------- Live objects (exist in runtime)
# --- Connect ---
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

class ContractIDMissingError(MonitorError):
    def __init__(self, message: str):
        super().__init__(message)


# --- Ordering
class TradeSessionError(EC_APIError):...

class TradeSubscriptionMissingError(TradeSessionError):
    def __init__(self, message: str):
        super().__init__(message)

# --- Payload
class PayloadError(EC_APIError):...

# Safety check error
class PriceRangeGuardViolation(PayloadError):
    def __init__(self, message: str):
        super().__init__(message)

# --- OpStrategy
class OpStrategyError(EC_APIError):...
