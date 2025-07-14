#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 26 16:27:39 2025

@author: dexter

A script that make payload based on existing Strategies.

It also manage the logisitc of the payloads. 
"""
import datetime
from EC_API.payload import Payload

class PayloadFactory(object):
    # Sole responsiplility is to make payload given a method (Strategy)
    # Order(from Signal) to Payload
    
    def __init__(self):
        self.gen_method = None
        self.signal = None
        return 
    
    def make(self):
        # Unpack Signal, put start_time, end_time into the Payload
        
        # Assign cl_order
        
        # Payload
        return
    
    
class PayloadLogisitc():
    # Storage: Inactive payload Storage.
    # Chamber: Load the chamber on the day of planned executions.
    # ShellPile: Discarded Payloads, either sent or canceled.
    
    # Chamber is loaded with payload that is going to be active on that day
    
    def __init__(self):
        # Connect to DB
        self.from_DB = None
        self.to_DB = None
        return 
    
    def move():
        # Simple copy and delete function
        return 
    
# one example
# SendPayload:
    #factory: PayloadFactory
    #Payload = factory.create_payload()
    #Payload.send()
    
# class TradeEngine(abstract):
#   def sendpayload(str):
#   def create_payload():
# =============================================================================
# #@util.time_it
# def gen_new_xlfile(xl_template_filename: str, output_filename: str, 
#                    date_interest: datetime.datetime, 
#                    signal_result_dict: dict,
#                    cell_loc_dict: dict = CELL_LOC_DICT, 
#                    contract_num_dict: dict = CONTRACT_NUM_DICT):
#     """
#     Generate a new excel file.
# 
#     Parameters
#     ----------
#     xl_template_filename : TYPE
#         DESCRIPTION.
#     output_filename : TYPE
#         DESCRIPTION.
#     date_interest : TYPE
#         DESCRIPTION.
#     signal_result_dict : TYPE
#         DESCRIPTION.
#     cell_loc_dict : TYPE, optional
#         DESCRIPTION. The default is CELL_LOC_DICT.
#     contract_num_dict : TYPE, optional
#         DESCRIPTION. The default is CONTRACT_NUM_DICT.
# 
#     Returns
#     -------
#     wb_obj : TYPE
#         DESCRIPTION.
# 
#     """
#     wb_obj = openpyxl.load_workbook(xl_template_filename, keep_vba=True)
# 
#     wb_obj = enter_new_value(wb_obj, date_interest, cell_loc_dict, 
#                              signal_result_dict, 
#                              contract_num_dict, output_filename)
# 
#     wb_obj.save(output_filename)
# 
#     return wb_obj
# 
# def gen_timetable(start_date: datetime.datetime,
#                   end_date: datetime.datetime, exchange='NYSE'):
#     # establish a timetable for reference
#     temp_timetable = mcal.get_calendar(exchange).schedule(start_date=start_date,
#                                                         end_date=end_date)
#     temp_timetable['Date'] = temp_timetable.index
#     timetable = temp_timetable.reset_index(drop=True)
#     
#     print("DingDIng", timetable)
# 
#     return timetable
# 
# def validate_lag_data(data_table: pd.DataFrame, 
#                       lag_timetable: pd.DataFrame, 
#                       data_table_date_proxy: str = 'PERIOD',
#                       lag_timetable_date_proxy: str = 'Date',
#                       data_table_start_index: int = 0,
#                       lag_size: int=5):
#     
#     for i in range(-1, -1*(1+lag_size),-1):
#         # This is a loop backward, from -1 to -5, for example.
#         check = (data_table[data_table_date_proxy].iloc[i+data_table_start_index] == \
#                  lag_timetable[lag_timetable_date_proxy].iloc[i])
#         print(i,'data', data_table[data_table_date_proxy].iloc[i+data_table_start_index])
#         print(i,'lag',lag_timetable[lag_timetable_date_proxy].iloc[i])
#         if not check:
#             raise Exception("One of the lag data does not align with the \
#                             lag time table.")
#     def old_method():
#         syms_NYSE = ['CLc1','CLc2', 'HOc1', 'HOc2', 'RBc1', 'RBc2']
#         syms_ICE = ['QOc1','QOc2', 'QPc1', 'QPc2']
#         
#         syms = syms_NYSE+syms_ICE
#         
#         # Define the date of interest
#         date_interest = datetime.datetime.today()#datetime.datetime(2024,11,29)
#         date_interest = datetime.datetime.combine(date_interest.date(),
#                                                   datetime.time(0,0,0))
#         
#         
#         print("date_interest", date_interest)
#         is_open_NYSE = util.market_is_open(date_interest.strftime("%Y-%m-%d"),
#                                            exchange="NYSE")
#         is_open_ICE = util.market_is_open(date_interest.strftime("%Y-%m-%d"),
#                                           exchange="ICE")
#         print("is_open_NYSE",is_open_NYSE)
#         print("is_open_ICE",is_open_ICE)
#         # check if market is open today
#         if is_open_NYSE or is_open_ICE:
#             LAG_SIZE = 5
#             # set the start and end date for query
#             END_DATE = date_interest.strftime("%Y-%m-%d")
#             START_DATE = (date_interest - datetime.timedelta(days=10)).strftime("%Y-%m-%d")
#             print("START_DATE, END_DATE", START_DATE, END_DATE)
#             
#             # establish a timetable for reference
#             timetable_NYSE = gen_timetable(START_DATE,END_DATE,exchange='NYSE')
#             timetable_ICE = gen_timetable(START_DATE,END_DATE,exchange='ICE')
#             
#             # get the index for date_interest asa reference point
#             date_interst_index_NYSE = timetable_NYSE[timetable_NYSE['Date']==date_interest].index.item()
#             date_interst_index_ICE = timetable_ICE[timetable_ICE['Date']==date_interest].index.item()
#             print('index',date_interst_index_NYSE, date_interst_index_ICE)
#             # Define the lag_timetable using the above and lag_size
#             lag_timetable_NYSE = timetable_NYSE[date_interst_index_NYSE-LAG_SIZE:date_interst_index_NYSE]
#             lag_timetable_ICE = timetable_ICE[date_interst_index_ICE-LAG_SIZE:date_interst_index_ICE]
#             
#             print("index", date_interst_index_NYSE, date_interst_index_ICE)
#             print("lag_timetable", lag_timetable_NYSE, lag_timetable_ICE)
#             
#             #Check if the APC data is up-to-date
#             check_APC_update = [(SIGNAL_PKL[sym]["PERIOD"].iloc[-1] == date_interest) 
#                               for sym in syms]
#             
#             if False in check_APC_update: raise Exception("APCs are not all up-to-dates")
#             
#             # Check for date alignment with the lag timetable
#             run_alignment_validation(lag_timetable_NYSE, 
#                                      syms_NYSE, lag_size=LAG_SIZE)
#             run_alignment_validation(lag_timetable_ICE, 
#                                      syms_ICE, lag_size=LAG_SIZE)
#             
#             #Make the trading spreadsheet
#             print("Market Open")
#             # Input and output filename
#             XL_TEMPLATE_FILENAME = XLS_TEMPLATE_FILEPATH  + \
#                                    "\\argus_exact_MR_strategy_wb_light_auto_off.xlsm"
#                                    #"\\argus_exact_MR_strategy_manual.xlsx"
#             OUTPUT_FILENAME = XLS_TEMPLATE_FILEPATH  + \
#                               "\\XLS_trading_sheet_MR_{}.xlsm".format(
#                                                 date_interest.strftime('%Y_%m_%d'))
#             print("OUTPUT_FILENAME", OUTPUT_FILENAME)
#             #Define the end date as the date of interest
#             #START_DATE2 = (date_interest - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
#             #Check and update everything
#             # Run the strategy by list
#      
#             SIGNAL_RESULT_DICT = run_MR(date_interest)
#         
#             # Generate the excel file
#             gen_new_xlfile(XL_TEMPLATE_FILENAME, OUTPUT_FILENAME, 
#                            date_interest, SIGNAL_RESULT_DICT, 
#                            cell_loc_dict = CELL_LOC_DICT, 
#                            contract_num_dict=CONTRACT_NUM_DICT)
#             
#             # Send email to Leigh
#             send_trading_sheet_email()
#             
#             # Run batch script that open the excel file
#             os.chdir("C:\\trading_operation")
#             os.startfile("open_xls.bat")
# =============================================================================


