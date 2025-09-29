# *EC_API*: A wrapper package utilising WebSocket for Algo Trading 


## Overview
`EC_API` provides easy-to-use functions for algorithmic trading. 
It is a wrapper package that utilises Websocket messaging to fasicilates 
trades, real-time data monitor, open posoitions tradcking, and etc.

In the current version, we only support trade and real-time data monitoring 
through CQG WebAPI which connect to their trade routing server through 
WebSocket and TSL layers. 

## Module Reviews
`EC_API` contains the following modules:
| Module | Description |
|-----------|-------------|
| `connect` | Connection modiule that is in charge of authetication and message<br> hear-back. |
| `ext` | External codes. Trade routing API codes are in here.  |
| `monitor` | Monitor module takes care of information request, open-order<br>tracking, and real-time data request. Specify `DataFeed` input<br>for strategy here.|
| `msg_validation` | It is in charge of server message validation. After sending<br>a client request, the server repsonse message goes through<br>message validation process in this module. The functions match<br>the message ID and map them with the acceptable message type<br>to ensure accurate pairing between client-server messages. |
| `op_strategy` | It defines the format for operational strategy (`OpStrategy`).<br> Key components for strategy building, such as `OpSignal`<br>that controls the life-cycle of signals, as well as `ActionNode`<br> and `ActionTree` (a finite-state machine) that controls<br>order flow and execution are in this module. |
| `ordering` | It handles `LiveOrder` type objects and how we send order request<br>to the exchanges. |
| `payload` | It contains the `Payload` class where parameters validation and<br>safety check for client message is done before sending it to the<br>server. It is recommended to conduct all trading via<br>`ExecutePayload` types of method. |
| `utility` | It contains utility functions for the package.  |


## Usage
Here are some examples for the usage. 
We use CQG connection as an example in this demostration.


### (1) Sending Orders
To facilitate a connection, 
```python
from EC_API.connect.cqg.connect import ConnectCQG

HOST_NAME = 'wss://demo.traderoute.com:000'
USR_NAME = 'USR_NAME'
PASSWORD = 'PASSWORD'
ACCOUNT_ID = 0000000

# create an connection before trading
CONNECT = ConnectCQG(HOST_NAME, USR_NAME, PASSWORD)
```

To send a new order request directly via `EC_API` native functions 
(not recommended) from the `ordering` module.

```python
from datetime import timezone, datetime, timedelta
from EC_API.ordering.cqg.live_order import CQGLiveOrder
from EC_API.ordering.enums import (
    OrderType, Duration, Side,
    ExecInstruction,
    RequestType
    )
new_order_details =  { 
    "symbol_name": "CLEV25",
    "cl_order_id": "1231314",
    "order_type": OrderType.ORDER_TYPE_LMT,  # For Limit orders
    "duration": Duration.DURATION_GTC,      # With a Duration of Good-till-Cancel
    "side": Side.SIDE_BUY,              # Buy order
    "qty_significant": 2,
    "qty_exponent": 0, 
    "scaled_limit_price": 1000,
    "good_thru_date": datetime(2025,9,9),
    "exec_instructions": ExecInstruction.EXEC_INSTRUCTION_AON
    }
                      
try:
  CLOrder1 = CQGLiveOrder(CONNECT, 
                         symbol_name = new_order_details['symbol_name'], 
                         request_id = 100, 
                         account_id = ACCOUNT_ID)
  # Specify the request type as you send the order
  CLOrder1.send(request_type = RequestType.NEW_ORDER, 
                request_details = new_order_details)  
```

To send a modify order request in a similar fashion
```python

modify_order_details =  { 
    "symbol_name": "CLEV25",
    "ogri_cl_order_id": "1231314", # The original cl_order_id
    "cl_order_id": "1231315", # new cl_order_id
    "duration": Duration.DURATION_GTD, # Change from GTC to GTD
    "qty": 10, # change qty to from 2 to 10
    "scaled_limit_price": 1100, # change LMT proce from 1000 to 1100
    }
                      
try:
  CLOrder2 = CQGLiveOrder(CONNECT, 
                         symbol_name = modify_order_details['symbol_name'], 
                         request_id =102, 
                         account_id = ACCOUNT_ID)
  CLOrder2.send(request_type = RequestType.MODIFY.ORDER, 
                request_details = modify_order_details)

```

However, it is recommended to send order requests to the exchanges'' 
server using an `Payload` object. The payload class provided format
checking and safety regulation for the input parameters. 

To send orders with `Payload`, you can use this:

```python 
from EC_API.payload.base import Payload, ExecutePayload
from EC_API.payload.cqg.safety import CQGFormatCheck # Import safety standard specific to cqg
from EC_API.ordering.enums import (
    OrderType, Duration, Side,
    ExecInstruction,
    RequestType
    )
from EC_API.ordering.cqg.live_order import CQGLiverOrder
ORDER_INFO = {
   "symbol_name": "CLEV25",
   "cl_order_id": "1231314",
   "order_type": OrderType.ORDER_TYPE_LMT, 
   "duration": Duration.DURATION_GTC, 
   "side": Side.SIDE_BUY,
   "qty_significant": 2,
   "qty_exponent": 0, 
   "is_manual": False,
   "scaled_limit_price": 1000,
   "good_thru_date": datetime(2025,9,9),
   "exec_instructions": ExecInstruction.EXEC_INSTRUCTION_AON
    }

# Construct Payload object
PL1 = Payload(
  request_id = 100,
  status = PayloadStatus.PENDING,
  order_request_type = RequestType.NEW_ORDER,
  start_time = datetime.now(timezone.utc) +\
               timedelta(minutes=5)
  end_time = datetime.now(timezone.utc) +\
             timedelta(days=1)
  order_info = ORDER_INFO,
  check_method = CQGFormatCheck # Setup the format checking policy
  )

# ExecutePayload 
try: # Specify the type of live order we are using here.
  EP = ExecutePayload(CONNECT, PL1, ACCOUNT_ID, live_order=CQGLiveOrder).unload()

```
### (2) Strategy Building
`EC_API` follows the following standard schema for operational strategy:
![plot](./images/op_strategy_module.jpg)


To build a Operational Strategy, One need to use the following workflow and data structure.

We will follow the schematic above.
First, we specifiy the trigger conditions and `Payload` objects to be sent.
```
from datetime import datetime, timedelta, timezone
from EC_API.op_strategy.action import ActionNode, ActionTree
from EC_API.op_strategy.signal import OpSignal
from EC_API.payload.cqg.safety import CQGFormatCheck
from EC_API.payload.base import Payload
from EC_API.payload.enums import PayloadStatus
from EC_API.ordering.enums import RequestType

# Global variables
account_id = 1000
checks = CQGFormatCheck #Define checking schema for Payloads


# Trigger Conditions
# a, b, c, d, a2 = 100, 50, 60, 70, 80
TE_trigger =  lambda ctx: ctx.price >= a
mod_TE_trigger = lambda ctx: b < ctx.price < a
TP_trigger_1 = lambda ctx: ctx.price <= c
TP_trigger_2 = lambda ctx: ctx.price <= d
cancel_trigger = lambda ctx: ctx.price < b
overtime_cond = lambda ctx: ctx.timestamp >= (datetime.now(tz=timezone.utc) + timedelta(seconds=5)).timestamp()

# Define Payloads


```

After that we have to define `ActionNode` and `ActionTree`:
```
# Define Action Nodes
cancel_node = ActionNode("CancelEntry", 
                         payloads = [cancel_PL_A], 
                         trigger_cond = cancel_trigger, 
                         transitions={})
TP_node_1 = ActionNode("TakeProfit1", 
                       payloads=[TP_PL1_A], 
                       trigger_cond = TP_trigger_1, 
                       transitions={})
TP_node_2 = ActionNode("TakeProfit2", 
                       payloads =[TP_PL2_A], 
                       trigger_cond = TP_trigger_2, 
                       transitions={})
TE_node_mod = ActionNode("ModifyTargetEntry", 
                         payloads=[TE_mod_PL_A], 
                         trigger_cond = mod_TE_trigger, 
                         transitions={
                             "TakeProfit2": (TP_trigger_2, TP_node_2)
                             })
TE_node = ActionNode("TargetEntry", 
                     payloads=[TE_PL_A], # Have two assets for testing. Same direction
                     trigger_cond = TE_trigger, 
                     transitions = { # Same transition and trigger conditions
                         "TakeProfit1": (TP_trigger_1, TP_node_1),
                         "ModifyTargetEntry": (mod_TE_trigger, TE_node_mod),
                         "CancelEntry": (cancel_trigger, cancel_node)   
                         })
overtime_node = ActionNode("OvertimeExit", 
                           payloads=[overtime_PL_A], 
                           trigger_cond=overtime_cond, 
                           transitions={})

# Define Action Tree
tree = ActionTree(TE_node, overtime_cond, overtime_node)

```
Then, we have to define the `OpSignal` (Operation Signal) objects where the `ActionTree` lives:
```
```

Finally, we can write the `OpStrategy` type class that produces  `OpSignal`.
```

```
Note that for a fully automated Algo-Trading setup, the `OpSignal` and `OpStrategy`
both live in the "Data Loop" where the raw market data from the websocket are
ingested. The raw ticks has to be stored in `TickBuffer` objects via the 
built-in method of the `DataFeed` class. `OpSignal` and `OpStrategy` interact 
with `DataFeed` and decided when to send out the corresponding orders or what 
signal to be generated, respectively.

As a short summary, each classes are in control of a separate function, from
a top-to-down persepctive, we have:
(1) `OpStrategy` reads the `DataFeed` controls the production `OpSignal` and 
    the cool-down mechanism that limit the frequency of signal production;
(2) `OpSignal` reads the `DataFeed` and controls xxx;
(3) `ActionTree` controls the traversal along the `ActionNode` chain and the
    sequence of execution of the `ActionNode` objects;
(4) `ActionNode` controls when is the `Payload` insertion triggered;
(5) `Payload` controls how the desired orders is sent to an Exchange (`LiveOrder`
    type objects), and what format checking policy (via `FormatCheck` type 
    objects) is used to validate our orders.



### (3) Monitoring and Data Feed
To monitor Open Orders in your account,
```python
from EC_API.monitor.cqg.trade_info import MonitorTradeCQG

# Check open orders for the past 9 hours
to_date = datetime.now(timezone.utc) - timedelta(hours=1)
from_date = datetime.now(timezone.utc) - timedelta(hours=10)

Mon = MonitorTradeCQG(CONNECT, ACCOUNT_ID)
Mon.request_historical_orders(from_date, to_date)

```

To monitor Real-time Data (WIP)
```python

```


## Project Structure
-----------------------
    ├── EC_API
    │   ├── connect                   <- In charge of server connections and authetications.
    │   │   ├── base.py
    │   │   ├── cqg                   <- cqg specfic codes in each modules. Patches and new service can be added easily.
    │   │   │   ├── connect.py                      
    │   │   │   └── __init__.py
    │   │   ├── hearback.py           <- Universal decorators functions for receiving server msg.
    │   │   └── __init__.py
    │   ├── ext                       <- External codes. Service provider's API can be added here.
    │   │   ├── common
    │   │   │   ├── decimal_pb2.py
    │   │   │   ├── __init__.py
    │   │   │   └── shared_1_pb2.py
    │   │   ├── __init__.py
    │   │   └── WebAPI                <- Generated format files from CQG WebAPI protocol buffer.
    │   │       ├── account_authorization_2_pb2.py
    │   │       ├── api_limit_2_pb2.py
    │   │       ├── economic_calendar_2_pb2.py
    │   │       ├── historical_2_pb2.py
    │   │       ├── __init__.py
    │   │       ├── instrument_definition_2_pb2.py
    │   │       ├── market_data_2_pb2.py
    │   │       ├── metadata_2_pb2.py
    │   │       ├── metadata_admin_2_pb2.py
    │   │       ├── order_2_pb2.py
    │   │       ├── otc_1_pb2.py
    │   │       ├── rules_1_pb2.py
    │   │       ├── strategy_2_pb2.py
    │   │       ├── strategy_definition_2_pb2.py
    │   │       ├── symbol_browsing_2_pb2.py
    │   │       ├── trade_routing_2_pb2.py
    │   │       ├── trading_account_2_pb2.py
    │   │       ├── trading_session_2_pb2.py
    │   │       ├── user_attribute_2_pb2.py
    │   │       ├── user_session_2_pb2.py
    │   │       ├── webapi_2_pb2.py
    │   │       ├── webapi_client.py
    │   │       └── websocket.py
    │   ├── __init__.py
    │   ├── monitor                   <- All functions related to monitoring.
    │   │   ├── base.py
    │   │   ├── cqg
    │   │   │   ├── realtime_data.py
    │   │   │   ├── trade_info.py
    │   │   │   └── __init__.py
    │   │   ├── data_feed.py
    │   │   ├── mock
    │   │   │   ├── realtime_data.py
    │   │   │   └── __init__.py
    │   │   ├── stat_metrics.py
    │   │   ├── tick.py
    │   │   ├── tick_stats.py
    │   │   ├── __init__.py
    │   ├── msg_validation            <- In charge of validating server message.
    │   │   ├── base.py
    │   │   ├── cqg
    │   │   │   ├── connect_enums.py
    │   │   │   ├── historical_enums.py
    │   │   │   ├── mapping.py        <- CQG-specific valid client-server msg mappings.
    │   │   │   ├── market_data_enums.py
    │   │   │   ├── meta_enums.py
    │   │   │   ├── trade_enums.py
    │   │   │   ├── valid_msg_check.py
    │   │   │   └── __init__.py
    │   │   ├── __init__.py
    │   ├── ops_strategy              <- In charge of operation strategy (Service Agnostic).
    │   │   ├── action.py
    │   │   ├── base.py
    │   │   ├── enums.py
    │   │   ├── signal.py
    │   │   └── __init__.py
    │   │ 
    │   ├── ordering                  <- In charge of sending orders to the exchanges.
    │   │   ├── base.py
    │   │   ├── cqg
    │   │   │   ├── live_order.py
    │   │   │   └── __init__.py
    │   │   ├── enums.py
    │   │   ├── __init__.py
    │   ├── payload                   <- Define the unified payload format for order requests (Service Agnostic).
    │   │   ├── base.py
    │   │   ├── cqg
    │   │   │   ├── safety.py         <- CQG-specific safety parameters and format checks.
    │   │   │   └── __init__.py    
    │   │   ├── enums.py
    │   │   ├── __init__.py
    │   │   └── safety.py
    │   ├── _typing.py
    │   ├── utility
    │   │   ├── base.py
    │   │   └── __init__.py
    │   └── _version.py
    ├── tests
    │   ├── ordering_cases.py
    │   ├── test_connect.py
    │   ├── test_monitor_CQG.py
    │   ├── test_msg_validation.py
    │   ├── test_ordering_CQG.py
    │   ├── test_payload_CQG.py
    │   ├── __init__.py
    ├── main.py
-----------------------