
class EC_APIError(Exception):
    """Base case for EC_API Error"""

# ---
class ConnectError(EC_APIError):...
class DisconnectError(EC_APIError):...

class AuthError(EC_APIError):...

# ----
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
    def __int__(self, message: str):
        super().__init__(message)