# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [0.2.0] - 2026-05-11

### Added
- `stream()` function in `MonitorDataCQG` as the primary way to request and
receive real-time market data
- `tracker_loop()` function in `TradeSessionCCQG` to handle OrderID, CL_ORDER_ID, 
CHAIN_ORDER_ID, and the latest OrderStatus in the life-cycle of an order. It is
an event-driven async task that runs if the pending dictionary is no longer empty.
- `send()` function in `LiveOrderCQG` as the key method to route orders through 
the CQG server. Users can pass `RequestType` into the function and it will take 
care of the nuances behind order construction, format checking, and initiate
order tracking if the `RequestType` is `NewOrder`.
- Added server-side ping message response. The `pong` reply is now triggered 
directly in the `_router_loop()` of `ConnectCQG` with one of the highest priority.
- CQG-related trade subscription function calls in `TradeSessionCQG`. 
- CQG-related order request function calls in `LiveOrderCQG`. 
- CQG-related real-time market subscription function calls in `MonitorDataCQG`. 


### Changed
- Linter modifications for code formatting
- Mypy ran and fixed most type annotation across the package except the WIP 
`op_strategy` and `common` modules.
- Refactored `Payload` and `ExecutePayload` in a new format where we get rid of 
the time-interval inputs in `Payload`. It is now purely a vendor-agnostic wrapper
over `LiveOrder` objects and apply a `PreTradeRiskCheck` over the order details.
User will have to supply a toml file that specific the allowed range for specific
parameters, such as 'limit_price' and 'stop_price.' Note that `PreTradeRiskCheck`
is a static check for order details. For dynamic risk control, we will implement
a `InSessionRiskCheck` in the future.
- `ExecutePayload` is now stable and will be the preferred way for the users to 
send orders through exchanges.  
 
### Fixed

- `_router_loop()` handling of order statuses, position statuses, and account
summary is now changed. These three now have separate queues in the attributes 
of `ConnectCQG` and they are routed based on a cheap check.


## [0.1.5] - 2026-03-10
### Added
- A tests suite along with Dummy Server to test the more involved async process.
- First functioning draft of the `_router_loop()` in the `ConnectCQG` object. It 
serves as a message relay backbone for the messaging system.
- Completed version of `ConnectCQG`.
- The three `ConnectCQG` dunder methods: `__aenter__` plus `__aexit__` 
and `__del__` for last resort graceful exit of the session.
- CQG-related session function calls in `ConnectCQG`. 
- parser functions for all vendor-specific modules: `connect`, `monitor`, and 
`ordering`.
- Added message splitter at the beginning of the `_router_loop()` to disallow
incoming composite server message with more than one distinct top field hitting 
the router process.
- Added `SymbolRegistry` to handle symbol subscriptions across data and trade
services. 


## [0.1.0] - 2025-10-10

### Added
- A suite of `key_extractor` functions added to extract unique router keys in the form 
of 4-tuple for each server message that is not streaming data. The router keys are
used in the reclaiming of responses by callers in the `MessageRouter`.
- Added `StreamRouter` for streaming message and support Pub/Sub pattern for callers.
- Added `MessageRouter` for RPC-like message reclaim for callers via async futures.
- Added validation method for message builders to perform pre-trade check on the 
input parameters in order requests.
- Added builder functions for all CQG modules: `connect/cqg`, `monitor/cqg`, and `ordering/cqg`.
- Added a `TransportCQG` layer to handle synchronous message dispatch via a 
`_send_loop()` and `_recv_loop()`.
- First draft of `Connect` protocol object.
- First draft of `Monitor` protocol object.
- First draft of `Transport` protocol object.
- First draft of `Payload` and `ExecutePayload` methods


### Changed

All functions are implemented to be async-native from this point onward.

### Fixed