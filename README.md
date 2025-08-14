EC_API:: A wrapper package utilising WebSocket for Algo Trading 
===============================================================

## : Overview
EC_API provides easy-to-use functions for xxx.
In the current version, we use CQG WebAPI to fascilate trade 
routing through their WebSocket and TSL layers. 

## : Usage

Here are some examples for the usage. 
We use CQG connection as an example in this demostration.

To facilitate connections, 
```python
from EC_API.connect.base import ConnectCQG

HOST_NAME = 'wss://demo.traderoute.com:000'
USR_NAME = 'USR_NAME'
PASSWORD = 'PASSWORD'
ACCOUNT_ID = 0000000

# create an connection before trading
CONNECT = ConnectCQG(HOST_NAME, USR_NAME, PASSWORD)
```

To send a new order request directly via EC_API native functions.

```python
from EC_API.utility.base import random_string
from EC_API.ordering.CQG_LiveOrder import CQGLiveOrder
new_order_details =  { 
    "symbol_name": "CLEV25",
    "cl_order_id": "1231314",
    "order_type": ORDER_TYPE_LMT, 
    "duration": DURATION_GTC, 
    "side": SIDE_BUY,
    "qty_significant": 2,
    "qty_exponent": 0, 
    "is_manual": bool = False,
    "scaled_limit_price": 1000,
    "good_thru_date": datetime.datetime(2025,9,9),
    "exec_instructions": EXEC_INSTRUCTION_AON
    }
                      
try:
  CLOrder1 = CQGLiveOrder(CONNECT, 
                         symbol_name = new_order_details['symbol_name'], 
                         request_id =100, 
                         account_id = ACCOUNT_ID)
  CLOrder1.send(request_type=RequestType.NEW_ORDER, 
                request_details = new_order_details) # Specific the request type
```
Result:
```plaintext

```

To send modify order request in a similar fashion
```python

modify_order_details =  { 
    "symbol_name": "CLEV25",
    "order_id": ORDER_ID, 
    "ogri_cl_order_id": "1231314", # The original cl_order_id
    "cl_order_id": "1231315", # new cl_order_id
    "duration": DURATION_GTD, # Change from GTC to GTD
    "qty": 10, # change qty to from 2 to 10
    "scaled_limit_price": 1100, # change LMT proce from 1000 to 1100
    }
                      
try:
  CLOrder2 = CQGLiveOrder(CONNECT, 
                         symbol_name = modify_order_details['symbol_name'], 
                         request_id =102, 
                         account_id = ACCOUNT_ID)
  CLOrder2.send(request_type=RequestType.MODIFY.ORDER, 
                request_details = modify_order_details)

```


However, it is recommended to send order request to the exhange's 
server using *Payload* objects. The payload class provided format
checking and safety regulation for the input parameters. 

To send orders with *Payload*, you can use this:

```python 
from EC_API.payload.base import Payload, ExecutePayload_CQG

ORDER_INFO = {
   "symbol_name": "CLEV25",
   "cl_order_id": "1231314",
   "order_type": ORDER_TYPE_LMT, 
   "duration": DURATION_GTC, 
   "side": SIDE_BUY,
   "qty_significant": 2,
   "qty_exponent": 0, 
   "is_manual": False,
   "scaled_limit_price": 1000,
   "good_thru_date": datetime.datetime(2025,9,9),
   "exec_instructions": EXEC_INSTRUCTION_AON
    }

# Construct Payload object
PL1 = Payload(
  request_id = 100,
  status = PayloadStatus.PENDING,
  order_request_type = RequestType.NEW_ORDER,
  start_time = datetime.datetime.now(timezone.utc) +\
               datetime.timedelta(minutes=5)
  end_time = datetime.datetime.now(timezone.utc) +\
             datetime.timedelta(days=1)
  order_info = ORDER_INFO,
  check_method = CQGFormatCheck
  )

# ExecutePayload 
try:
  EP = ExecutePayload_CQG(CONNECT, PL1, ACCOUNT_ID)
  EP.unload()

```
Result:
```plaintext

```
To monitor Position,

To monitor

##: Project Organization (under construction)
