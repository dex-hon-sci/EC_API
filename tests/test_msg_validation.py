#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 11:22:26 2025

@author: dexter
"""
from EC_API.msg_validation.cqg.valid_msg_check import CQGValidMsgCheck


def test_MsgCheckPara_onoff()-> None:
    CQG_check = CQGValidMsgCheck()

    # Check if the MsgCheckPara are inherented in the Operation class and
    # properly initialised
    assert CQG_check.recv_status == False
    assert CQG_check.recv_succes_status == False
    assert CQG_check.recv_reject_status == False
    #assert CQG_check.recv_trade_snapshot == False
    assert CQG_check.recv_result == False
    
    # Change all attributes to True
    CQG_check.recv_status = True
    CQG_check.recv_succes_status = True
    CQG_check.recv_reject_status = True
    #CQG_check.recv_trade_snapshot = True
    CQG_check.recv_result = True

    assert CQG_check.recv_status == True
    assert CQG_check.recv_succes_status == True
    assert CQG_check.recv_reject_status == True
    #assert CQG_check.recv_trade_snapshot == True
    assert CQG_check.recv_result == True

# test_all_types_of mseesage repsonse
    
