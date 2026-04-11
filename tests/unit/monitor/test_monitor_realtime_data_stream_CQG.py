import pytest
from EC_API.connect.cqg.base import ConnectCQG
from EC_API.connect.enums import ConnectionState
from EC_API.monitor.cqg.realtime_data import MonitorDataCQG


def make_stream():
    return 

@pytest.mark.asyncio
async def test_monitor_data_CQG_stream_valid():
    async with ConnectCQG(
        "host_name", "user_name", "password", 
        immediate_connect= False, client=object()
        ) as conn:
        MD = MonitorDataCQG(conn)
        
        conn._state_mgr.transition_to(ConnectionState.CONNECTED_LOGON)
    
# test for no logon
# test for error in realtime_requests..
# test for error in unsubscribe requests...