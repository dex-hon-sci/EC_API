# Change Lof 
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [0.2.0] 2026-05-11

### Added
- `stream()` function in `MonitorDataCQG` as the primary way to request and
recieve real-time market data
- `tracker_loop()` function in `TradeSessionCCQG` to handle OrderID, CL_ORDER_ID, 
CHAIN_ORDER_ID, and the latest OrderStatus in the life-cycle of an order. It is
an event-driven async task that runs if the pending
- `send()` function in `LiveOrderCQG` as the key method to route orders through 
the CQG server. Users can pass `RequestType` into the function and it will take 
care of the nauinces behind order construction, format checking, and initiate
order tracking if it is the `RequestType` is `NewOrder`.
- CQG-related function calls in `TradeSessionCQG`. 
- CQG-related function calls in `LiveOrderCQG`. 
- CQG-related function calls in `MonitorDataCQG`. 


### Changed
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

## [0.1.5] 2025-11-10
- ConnectCQG
- ConnectCQG dunder methods
- ConnectCQG functions calls


## [0.1.0] 2025-11-10

### Added

- _router_loop

- key_extractor
- stream_router
- message_router
- symbol_registry


   Currently Fully Tested Modules for CQG are:

Connect
Monitor
Transport
Payload
All builders+parsers functions for message translation are tested.
Data -Streaming functions are tested.


### Changed

All functions are implemented to be async-native from thid point onward.

### Fixed