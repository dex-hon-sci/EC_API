class EC_APIError(Exception):
    """Base case for EC_API Error"""
    
# --- Transport
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

# --- Builders
class MsgBuilderError(EC_APIError):
    def __init__(self, message: str):
        super().__init__(message)

# --- Parsers
class MsgParserError(EC_APIError):
    def __init__(self, message: str):
        super().__init__(message)

# --- Routers
class RoutingError(EC_APIError):...

class DuplicateRouterKeyError(EC_APIError):
    def __init__(self, message: str):
        super().__init__(message)

class UnknownRouterKeyError(EC_APIError):
    def __init__(self, message: str):
        super().__init__(message)
        
class UnknownSubscriptionError(EC_APIError):
    def __init__(self, message: str):
        super().__init__(message)
        
class SubscriptionQueueMismatchError(EC_APIError):
    def __init__(self, message: str):
        super().__init__(message)
        
class MaxSymbolsExceededError(EC_APIError):
    def __init__(self, message: str):
        super().__init__(message)
        
class MaxSubscribersExceededError(EC_APIError):
    def __init__(self, message: str):
        super().__init__(message)
        
class InvalidDroppingPolicy(EC_APIError):
    def __init__(self, message: str):
        super().__init__(message)
    
# -----------
# --- Common
# --- Connect
class ConnectError(EC_APIError):...

class ConnectCancelledError(EC_APIError):
    def __init__(self, message: str):
        super().__init__(message)

class DisconnectError(EC_APIError):
    def __init__(self, message: str):
        super().__init__(message)

class AuthError(EC_APIError):
    def __init__(self, message: str):
        super().__init__(message)

# --- Monitor

# --- Ordering

# --- Payload

# --- OpStrategy
