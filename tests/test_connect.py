#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 10:40:12 2025

@author: dexter
"""
import time
import logging

from EC_API.ext.WebAPI.webapi_2_pb2 import ClientMsg
from EC_API.ext.WebAPI.user_session_2_pb2 import (
    LogonResult, LoggedOff, Logon, \
    RestoreOrJoinSession, 
    RestoreOrJoinSessionResult
)
from EC_API.connect.base import ConnectCQG


host_name = 'wss://demoapi.cqg.com:443'
user_name = ''
password = ''

symbol_name = 'CLE'
invalid_pw = "fakepassword"

client_app_id='WebApiTest', 
client_version='python-client-test-2-230',
protocol_version_major = 2
protocol_version_minor = 240

# Define logger object
logger = logging.getLogger(__name__)
# =============================================================================
# logging.basicConfig(filename='./log/test_run_API_access.log', 
#                     level=logging.INFO,
#                     format="%(asctime) s%(levelname)s %(message)s",
#                     datefmt="%Y-%m-%d %H:%M:%S")
# =============================================================================
logging.basicConfig(filename='./log/temp.log', 
                    level=logging.INFO,
                    format="%(asctime) s%(levelname)s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")

def test_logonlogoff() -> None:
    # Successful Logon and Logoff
    
    # 1.  Create a Web Socket connection with Web API server.
    logger.info('========(Start test_logonlogoff)========')

    CONNECT = ConnectCQG(host_name,user_name, password)
    
    logger.info('1. Create a Web Socket connection with Web API server.')

    # 2.  Send Logon message with valid credentials - user_name, password,
    # client_app_id, private_label, client_version, protocol_version_minor, protocol_version_major.
    logon_server_msg = CONNECT.logon()
    
    # Test logon crendtial inputs
    assert CONNECT._user_name == user_name
    assert CONNECT._password == password
    assert CONNECT.client_app_id == "WebApiTest"
    assert CONNECT.client_version == 'python-client-test-2-240'
    assert CONNECT.protocol_version_minor == 240
    assert CONNECT.protocol_version_major == 2 
    
    logger.info('2. Send Logon message with valid credentials ')
    logger.info(f'user_name: {CONNECT._user_name}')
    logger.info(f'password: {CONNECT._password}')
    logger.info(f'client_app_id: {CONNECT.client_app_id}')
    logger.info(f'private_label: {CONNECT.private_label}')    
    logger.info(f'client_version: {CONNECT.client_version}')    
    logger.info(f'protocol_version_minor: {CONNECT.protocol_version_minor}')    
    logger.info(f'protocol_version_major: {CONNECT.protocol_version_major}')    

    # 3.  Receive LogonResult with result_code='SUCCESS', session_token, 
    # base_time, user_id, and server_time.
    assert logon_server_msg.logon_result.result_code == LogonResult.ResultCode.RESULT_CODE_SUCCESS
    
    if logon_server_msg.logon_result.result_code == LogonResult.ResultCode.RESULT_CODE_SUCCESS:
        logger.info('3. Receive LogonResult with result_code="SUCCESS" ')

        logger.info('LogonResult result_code: SUCCESS')
        logger.info(f'LogonResult session_token : {logon_server_msg.logon_result.session_token}')
        logger.info(f'LogonResult base_time: {logon_server_msg.logon_result.base_time}')
        logger.info(f'LogonResult user_id: {logon_server_msg.logon_result.user_id}')
        logger.info(f'LogonResult server_time: {logon_server_msg.logon_result.server_time}')
        
    # 4.  (Note that time attributes that are 64-bit signed integers 
    # contain offset in milliseconds from base_time attribute of the logon and 
    # session restore/join results. E.g. your logon_time=base_time+server_time. 
    # Find more API rules in webapi_2.proto)
    # 
    # 5.  Send Logoff message.
    logoff_server_msg = CONNECT.logoff()
    
    logger.info('5. Send Logoff message')

    # 6.  Receive LoggedOff with logoff_reason=’ BY_REQUEST’.
    assert logoff_server_msg.logged_off.logoff_reason == LoggedOff.LOGOFF_REASON_BY_REQUEST

    if logoff_server_msg.logged_off.logoff_reason == LoggedOff.LOGOFF_REASON_BY_REQUEST:
        logger.info('6. Receive LoggedOff with logoff_reason: BY_REQUEST')
        
    CONNECT.disconnect()
    
    logger.info('========(End test_logonlogoff)========')

    # 7.  (Note: the session_token in the LogonResult is a key information 
    # to provide in trouble shootings.)
    
    
def test_invalid_logon() -> None:
    # Invalid Logon

    # 1.  Send Logon message with invalid credentials - 
    # user_name, password, client_app_id, private_label.
    CONNECT = ConnectCQG(host_name,user_name, invalid_pw)

    # valid username but Invalid password input
    logon_server_msg = CONNECT.logon()
    
    logger.info('========(Start test_invalid_logon)========')
    logger.info('1. Send Logon message with invalid credentials')

    # 2.  Receive LogonResult with result_code='FAILURE'.
    assert logon_server_msg.logon_result.result_code == LogonResult.ResultCode.RESULT_CODE_FAILURE
    if logon_server_msg.logon_result.result_code == LogonResult.ResultCode.RESULT_CODE_FAILURE:
        logger.info('2. Receive LogonResult with result_code="FAILURE"')
    logger.info('========(End test_invalid_logon)========')
    
    logoff_server_msg = CONNECT.logoff()
    CONNECT.disconnect()


def test_concurrent_sessions() -> None:
    # Concurrent Session
    CONNECT = ConnectCQG(host_name,user_name, password)

    logger.info('========(Start test_concurrent_sessions)========')

    # 1.  Send Logon message with valid credentials - 
    # user_name, password, client_app_id, private_label, client_version, 
    # protocol_version_minor, protocol_version_major.
    client_msg, logon_obj, logon_server_msg = CONNECT.logon()
                                        #drop_concurrent_session=True)
    logger.info('1. Send Logon message with invalid credentials')
    print('server_msg1',logon_obj, logon_server_msg)

    # 2.  Receive LogonResult with result_code='SUCCESS'.
    assert logon_server_msg.logon_result.result_code == LogonResult.ResultCode.RESULT_CODE_SUCCESS
    if logon_server_msg.logon_result.result_code == LogonResult.ResultCode.RESULT_CODE_SUCCESS:
        logger.info('2. Receive LogonResult with result_code="SUCCESS".')

    # 3.  Send a Logon message with the same credentials and 
    # drop_concurrent_session=true.
    #client2 = webapi_client.WebApiClient()
    #client2.connect(host_name)
    CONNECT2 = ConnectCQG(host_name, user_name, password)

    # Logon but with the option to drop concurrent session
    client_msg2, logon_obj2, logon_server_msg2 = CONNECT2.logon(drop_concurrent_session= True)
    
    logger.info('3.Send a Logon message with the same credentials and drop_concurrent_session=true ')

    # 4.  Receive LogonResult with result_code='SUCCESS'.
    print('concurrent', 
          logon_server_msg2.logon_result.result_code,
          logon_server_msg.logon_result.result_code)
    print('server_msg2', client_msg2, logon_obj2, logon_server_msg2)
    assert logon_server_msg2.logon_result.result_code == LogonResult.ResultCode.RESULT_CODE_SUCCESS
    if logon_server_msg.logon_result.result_code == LogonResult.ResultCode.RESULT_CODE_SUCCESS:
        logger.info('4. Receive LogonResult with result_code="SUCCESS".')

    # 5.  Expect the concurrent session to be disconnected.
    logger.info('5. Concurrent session to be disconnected')

    # 6.  Send Logoff message.
    logoff_obj, logoff_server_msg = CONNECT2.logoff()
    
    logger.info('6. Send Logoff message.')
    CONNECT2.disconnect()
    logger.info('========(End test_concurrent_sessions)========')



def test_restore_session() -> None:
    # Test restore session message
    #1.  Send Logon message with valid credentials - user_name, password, 
    # client_app_id, private_label, client_version, session_settings =1
    # (SESSION_SETTING_ALLOW_SESSION_RESTORE), protocol_version_minor, protocol_version_major.
    CONNECT = ConnectCQG(host_name, user_name, password)

    logger.info('========(Start test_restore_session)========')

    # Allow session restore
    ALLOW_RESTORE = Logon.SessionSetting.SESSION_SETTING_ALLOW_SESSION_RESTORE
    logon_server_msg1 = CONNECT.logon(session_settings = ALLOW_RESTORE)
    
    #assert Logon.SessionSetting.SESSION_SETTING_ALLOW_SESSION_RESTORE in CONNECT.session_settings
    logger.info('1. Send Logon message with valid credentials.')
    session_token = logon_server_msg1.logon_result.session_token
        
    #2.  Disconnect the user ungracefully.
    #disconnect the wifi
    #client.websocket_client._close()
    print("Disconnect the user ungracefully")
    import os
    os.system("nmcli radio wifi off")
    time.sleep(10) # wait for 10 seconds
    #reconnect the wifi
    os.system("nmcli radio wifi on")
    time.sleep(10) # wait 10 seconds to ensure enough time for reconnection
    logger.info('2. Disconnect the user ungracefully.')
    
    #3.  Send RestoreOrJoinSession message with a valid session token 
    # and client_app_id, protocol_version_minor, protocol_version_major within 60 seconds.
    server_msg_restore = CONNECT.restore_request()

    logger.info('3. Send RestoreOrJoinSession message with a valid session token')
    
    #4.Receive RestoreOrJoinSessionResult with result_code='RESULT_CODE_SUCCESS'.
    assert server_msg_restore.restore_or_join_session_result.result_code == RestoreOrJoinSessionResult.ResultCode.RESULT_CODE_SUCCESS
    logger.info('4. Receive RestoreOrJoinSessionResult: RESULT_CODE_SUCCESS')
    logger.info(f'4. RestoreOrJoinSessionResult: {server_msg_restore}')
    print('server_msg_restore', server_msg_restore,
          RestoreOrJoinSessionResult.ResultCode.RESULT_CODE_SUCCESS)
    
    logger.info('========(End test_restore_session)========')
    
def test_restore_session_invalid_token() -> None: 
    #Restore Session with Invalid Session Token

    # 1. Send Logon message with valid credentials - user_name, password, 
    # client_app_id, private_label, client_version, session_settings=1 
    # (SESSION_SETTING_ALLOW_SESSION_RESTORE) , protocol_version_minor, 
    # protocol_version_major.
    CONNECT = ConnectCQG(host_name, user_name, password)
    logger.info('========(Start test_restore_session_invalid_token)========')

    logon_server_msg1 = CONNECT.logon(session_settings = 
                     Logon.SessionSetting.SESSION_SETTING_ALLOW_SESSION_RESTORE)
    
    #assert Logon.SessionSetting.SESSION_SETTING_ALLOW_SESSION_RESTORE in logon_obj1.session_settings
    logger.info('1. Send Logon message with valid credentials - user_name, password, \
                client_app_id, private_label, client_version, session_settings=1 \
                (SESSION_SETTING_ALLOW_SESSION_RESTORE) , protocol_version_minor,\
                protocol_version_major.')

    # Invalid token
    invalid_session_token = logon_server_msg1.logon_result.session_token+"XXXXXX"


    # 2. Disconnect the user ungracefully.
    #client.disconnect()
    #time.sleep(1)
    #logger.info('2. Disconnect the user ungracefully.')
    print("Disconnect the user ungracefully")
    import os
    os.system("nmcli radio wifi off")
    time.sleep(10) # wait for 10 seconds
    #reconnect the wifi
    os.system("nmcli radio wifi on")
    time.sleep(10) # wait 10 seconds to ensure enough time for reconnection
    logger.info('2. Disconnect the user ungracefully.')

    # 3. Send RestoreOrJoinSession message with an invalid session token and 
    # client_app_id, protocol_version_minor, protocol_version_major within 60 seconds.
    
    server_msg_restore = CONNECT.restore_request(session_token= invalid_session_token)

    logger.info('3. Send RestoreOrJoinSession message with a valid session token')

    # 4. Receive RestoreOrJoinSessionResult with 
    # result_code='RESULT_CODE_UNKNOWN_SESSION'.
    assert server_msg_restore.restore_or_join_session_result.result_code == \
           RestoreOrJoinSessionResult.ResultCode.RESULT_CODE_UNKNOWN_SESSION

    print('server_msg_special_2', server_msg_restore,
          RestoreOrJoinSessionResult.ResultCode.RESULT_CODE_SUCCESS)
    logger.info('4. Receive RestoreOrJoinSessionResult with \
                result_code=RESULT_CODE_UNKNOWN_SESSION.')
    logger.info(f'4. RestoreOrJoinSessionResult: {server_msg_restore}')
    logger.info('========(End test_restore_session_invalid_token)========')

    return

    
def test_pingpong_msg(): # WIP
    # Test Ping Pong messages
    CONNECT = ConnectCQG(host_name,user_name, password)
    logger.info('========(Start test_pingpong_msg)========')

    # Logon
    client_msg, logon_obj, logon_server_msg = CONNECT.logon()
    print("logon_server_msg", logon_server_msg)
    # Check if the logon is successful
    assert logon_server_msg.logon_result.result_code == LogonResult.ResultCode.RESULT_CODE_SUCCESS
    
    if logon_server_msg.logon_result.result_code == LogonResult.ResultCode.RESULT_CODE_SUCCESS:
        logger.info('LogonResult result_code: SUCCESS')

    # Receive Ping message
    server_msg = CONNECT.client.receive_server_message()

    # Check Ping message 
    assert server_msg.ping.token == "WebAPI Server Heartbeat"
    assert type(server_msg.ping.ping_utc_time) == int  
    logger.info('Ping Token: "WebAPI Server Heartbeat"')
    logger.info(f'Ping ping_utc_time: {server_msg.ping.ping_utc_time}')
    
    client_msg2 = ClientMsg()
    client_msg2.pong.token = "WebAPI Server Heartbeat"
    client_msg2.pong.ping_utc_time = server_msg.ping.ping_utc_time
    client_msg2.pong.pong_utc_time = int(time.time())
    
    client.send_client_message(client_msg2)
    
    server_msg2 = CONNECT.client.receive_server_message()
    
    logger.info('Ping Token: "WebAPI Server Heartbeat"')

    print('server_msg2', server_msg2.user_messages, server_msg2)
    
    logger.info('========(End test_pingpong_msg)========')
