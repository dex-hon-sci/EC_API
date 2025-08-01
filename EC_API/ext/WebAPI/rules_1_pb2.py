# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: WebAPI/rules_1.proto
# Protobuf Python Version: 5.29.3
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    3,
    '',
    'WebAPI/rules_1.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from EC_API.ext.common import shared_1_pb2 as common_dot_shared__1__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x14WebAPI/rules_1.proto\x12\x07rules_1\x1a\x15\x63ommon/shared_1.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"\xb2\x05\n\x0bRuleRequest\x12\x12\n\nrequest_id\x18\x01 \x02(\t\x12\x11\n\tsubscribe\x18\n \x01(\x08\x12\x31\n\x10set_rule_request\x18\x02 \x01(\x0b\x32\x17.rules_1.SetRuleRequest\x12\x37\n\x13modify_rule_request\x18\x0c \x01(\x0b\x32\x1a.rules_1.ModifyRuleRequest\x12\x37\n\x13\x64\x65lete_rule_request\x18\x03 \x01(\x0b\x32\x1a.rules_1.DeleteRuleRequest\x12\x33\n\x11rule_list_request\x18\x04 \x01(\x0b\x32\x18.rules_1.RuleListRequest\x12\x44\n\x1arule_event_history_request\x18\x05 \x01(\x0b\x32 .rules_1.RuleEventHistoryRequest\x12?\n\x17rule_event_subscription\x18\t \x01(\x0b\x32\x1e.rules_1.RuleEventSubscription\x12\x62\n*create_or_modify_destination_group_request\x18\x06 \x01(\x0b\x32..rules_1.CreateOrModifyDestinationGroupRequest\x12L\n\x1e\x64\x65stination_group_list_request\x18\x08 \x01(\x0b\x32$.rules_1.DestinationGroupListRequest\x12\x63\n*update_destination_expiration_time_request\x18\x0b \x01(\x0b\x32/.rules_1.UpdateDestinationExpirationTimeRequestJ\x04\x08\x07\x10\x08\"\xfd\x06\n\nRuleResult\x12\x12\n\nrequest_id\x18\x01 \x02(\t\x12\x13\n\x0bresult_code\x18\x02 \x02(\r\x12\x1f\n\x07\x64\x65tails\x18\x03 \x01(\x0b\x32\x0e.shared_1.Text\x12/\n\x0fset_rule_result\x18\x04 \x01(\x0b\x32\x16.rules_1.SetRuleResult\x12\x35\n\x12modify_rule_result\x18\r \x01(\x0b\x32\x19.rules_1.ModifyRuleResult\x12\x35\n\x12\x64\x65lete_rule_result\x18\x05 \x01(\x0b\x32\x19.rules_1.DeleteRuleResult\x12\x31\n\x10rule_list_result\x18\x06 \x01(\x0b\x32\x17.rules_1.RuleListResult\x12\x42\n\x19rule_event_history_result\x18\x07 \x01(\x0b\x32\x1f.rules_1.RuleEventHistoryResult\x12L\n\x1erule_event_subscription_status\x18\x0b \x01(\x0b\x32$.rules_1.RuleEventSubscriptionStatus\x12`\n)create_or_modify_destination_group_result\x18\x08 \x01(\x0b\x32-.rules_1.CreateOrModifyDestinationGroupResult\x12J\n\x1d\x64\x65stination_group_list_result\x18\n \x01(\x0b\x32#.rules_1.DestinationGroupListResult\x12\x61\n)update_destination_expiration_time_result\x18\x0c \x01(\x0b\x32..rules_1.UpdateDestinationExpirationTimeResult\"\xa9\x01\n\nResultCode\x12\x17\n\x13RESULT_CODE_SUCCESS\x10\x00\x12\x1a\n\x16RESULT_CODE_SUBSCRIBED\x10\x01\x12\x17\n\x13RESULT_CODE_DROPPED\x10\x02\x12\x16\n\x12RESULT_CODE_UPDATE\x10\x03\x12\x1c\n\x18RESULT_CODE_DISCONNECTED\x10\x04\x12\x17\n\x13RESULT_CODE_FAILURE\x10\x65J\x04\x08\t\x10\n\"\xc6\x02\n\x0eRuleDefinition\x12\x0f\n\x07rule_id\x18\x01 \x02(\t\x12\x11\n\trule_tags\x18\x02 \x03(\t\x12 \n\x07\x61\x63tions\x18\x04 \x03(\x0b\x32\x0f.rules_1.Action\x12\x31\n\x10order_event_rule\x18\x05 \x01(\x0b\x32\x17.rules_1.OrderEventRule\x12.\n\x0e\x63ondition_rule\x18\x07 \x01(\x0b\x32\x16.rules_1.ConditionRule\x12\x15\n\x07\x65nabled\x18\x06 \x01(\x08:\x04true\x12(\n\nattributes\x18\x08 \x03(\x0b\x32\x14.shared_1.NamedValue\x12\x0f\n\x07\x64\x65leted\x18\t \x01(\x08\x12\x33\n\x0f\x65xpiration_time\x18\n \x01(\x0b\x32\x1a.google.protobuf.TimestampJ\x04\x08\x03\x10\x04\"{\n\x06\x41\x63tion\x12+\n\x0c\x64\x65stinations\x18\x04 \x03(\x0b\x32\x15.shared_1.Destination\x12\x1c\n\x14\x64\x65stination_group_id\x18\x05 \x01(\t\x12&\n\x07go_flat\x18\x06 \x01(\x0b\x32\x15.rules_1.GoFlatAction\"\x0e\n\x0cGoFlatAction\"\x8b\x01\n\x0eOrderEventRule\x12\x17\n\x0b\x61\x63\x63ount_ids\x18\x01 \x03(\x11\x42\x02\x18\x01\x12\x16\n\x0eorder_statuses\x18\x02 \x03(\r\x12\x1c\n\x14transaction_statuses\x18\x03 \x03(\r\x12*\n\x07\x66ilters\x18\x04 \x03(\x0b\x32\x19.rules_1.OrderEventFilter\"\x9c\x02\n\rConditionRule\x12\x17\n\x0ftriggering_type\x18\x01 \x01(\r\x12\'\n\nexpression\x18\x02 \x02(\x0b\x32\x13.rules_1.Expression\x12\x31\n\x12notification_title\x18\x03 \x01(\x0b\x32\x15.rules_1.TemplateText\x12\x30\n\x11notification_body\x18\x04 \x01(\x0b\x32\x15.rules_1.TemplateText\x12\x1a\n\x12suppression_period\x18\x05 \x01(\r\"H\n\x0eTriggeringType\x12\x1c\n\x18TRIGGERING_TYPE_ONE_TIME\x10\x00\x12\x18\n\x14TRIGGERING_TYPE_AUTO\x10\x01\"\x1c\n\x0cTemplateText\x12\x0c\n\x04text\x18\x01 \x01(\t\"\xde\x03\n\nExpression\x12\x12\n\x08operator\x18\x01 \x01(\rH\x00\x12\x12\n\x08\x66unction\x18\x04 \x01(\tH\x00\x12&\n\x0cleft_operand\x18\x02 \x01(\x0b\x32\x10.rules_1.Operand\x12\'\n\rright_operand\x18\x03 \x01(\x0b\x32\x10.rules_1.Operand\x12#\n\targuments\x18\x05 \x03(\x0b\x32\x10.rules_1.Operand\"\x9e\x02\n\x08Operator\x12\x10\n\x0cOPERATOR_ADD\x10\x00\x12\x15\n\x11OPERATOR_SUBTRACT\x10\x01\x12\x15\n\x11OPERATOR_MULTIPLY\x10\x02\x12\x13\n\x0fOPERATOR_DIVIDE\x10\x03\x12\x11\n\rOPERATOR_LESS\x10\n\x12\x17\n\x13OPERATOR_LESS_EQUAL\x10\x0b\x12\x12\n\x0eOPERATOR_EQUAL\x10\x0c\x12\x16\n\x12OPERATOR_NOT_EQUAL\x10\x12\x12\x1a\n\x16OPERATOR_GREATER_EQUAL\x10\r\x12\x14\n\x10OPERATOR_GREATER\x10\x0e\x12\x10\n\x0cOPERATOR_NOT\x10\x0f\x12\x10\n\x0cOPERATOR_AND\x10\x10\x12\x0f\n\x0bOPERATOR_OR\x10\x11\x42\x11\n\x0f\x65xpression_type\"\xe9\x01\n\x07Operand\x12\'\n\nexpression\x18\x01 \x01(\x0b\x32\x13.rules_1.Expression\x12#\n\x08\x63onstant\x18\x02 \x01(\x0b\x32\x11.rules_1.Constant\x12\x30\n\x0fmarket_variable\x18\x03 \x01(\x0b\x32\x17.rules_1.MarketVariable\x12\x32\n\x10\x61\x63\x63ount_variable\x18\x04 \x01(\x0b\x32\x18.rules_1.AccountVariable\x12*\n\x0cstudy_symbol\x18\x05 \x01(\x0b\x32\x14.rules_1.StudySymbol\"6\n\x08\x43onstant\x12\x14\n\x0c\x64ouble_value\x18\x01 \x01(\x01\x12\x14\n\x0cstring_value\x18\x02 \x01(\t\"\x95\x02\n\x0eMarketVariable\x12\x0e\n\x06symbol\x18\x01 \x01(\t\x12\x0c\n\x04type\x18\x02 \x01(\r\"\xe4\x01\n\x04Type\x12\x1e\n\x1aTYPE_LAST_TRADE_NET_CHANGE\x10\x01\x12!\n\x1dTYPE_LAST_TRADE_NET_CHANGE_PC\x10\x02\x12\x19\n\x15TYPE_LAST_TRADE_PRICE\x10\x03\x12\x1a\n\x16TYPE_LAST_TRADE_VOLUME\x10\x04\x12\x1e\n\x1aTYPE_CONTRACT_TOTAL_VOLUME\x10\x05\x12\x17\n\x13TYPE_BID_ASK_SPREAD\x10\x06\x12\x14\n\x10TYPE_TODAYS_HIGH\x10\x07\x12\x13\n\x0fTYPE_TODAYS_LOW\x10\x08\"\x92\x06\n\x0f\x41\x63\x63ountVariable\x12\x0c\n\x04type\x18\x01 \x01(\r\"\xea\x05\n\x04Type\x12\x14\n\x10TYPE_UNSPECIFIED\x10\x00\x12\x15\n\x11TYPE_TOTAL_MARGIN\x10\x01\x12\x18\n\x14TYPE_POSITION_MARGIN\x10\x02\x12&\n\"TYPE_NO_MULTIPLIER_POSITION_MARGIN\x10\x1b\x12\x19\n\x15TYPE_PURCHASING_POWER\x10\x03\x12\x0c\n\x08TYPE_OTE\x10\x04\x12\x10\n\x0cTYPE_OTE_UPL\x10\x1a\x12(\n$TYPE_OPEN_TRADE_LOSS_UNREALIZED_LOSS\x10\x05\x12\x0c\n\x08TYPE_MVO\x10\x06\x12\x0c\n\x08TYPE_NLV\x10\x07\x12\x0c\n\x08TYPE_MVF\x10\x08\x12\x16\n\x12TYPE_MARGIN_CREDIT\x10\t\x12\x16\n\x12TYPE_MARGIN_EXCESS\x10\n\x12\x14\n\x10TYPE_CASH_EXCESS\x10\x0b\x12\x18\n\x14TYPE_CURRENT_BALANCE\x10\r\x12\x14\n\x10TYPE_PROFIT_LOSS\x10\x0e\x12\x1f\n\x1bTYPE_UNREALIZED_PROFIT_LOSS\x10\x0f\x12\x17\n\x13TYPE_OTE_UPL_AND_PL\x10\x10\x12\x1a\n\x16TYPE_YESTERDAY_BALANCE\x10\x11\x12\x16\n\x12TYPE_YESTERDAY_OTE\x10\x17\x12\x16\n\x12TYPE_YESTERDAY_MVO\x10\x18\x12\x1d\n\x19TYPE_YESTERDAY_COLLATERAL\x10\x0c\x12\x16\n\x12TYPE_NET_CHANGE_PC\x10\x19\x12\x19\n\x15TYPE_TOTAL_FILLED_QTY\x10\x12\x12\x1c\n\x18TYPE_TOTAL_FILLED_ORDERS\x10\x13\x12 \n\x1cTYPE_LONG_OPEN_POSITIONS_QTY\x10\x14\x12!\n\x1dTYPE_SHORT_OPEN_POSITIONS_QTY\x10\x15\x12\x33\n/TYPE_MIN_DAYS_TILL_POSITION_CONTRACT_EXPIRATION\x10\x16J\x04\x08\x02\x10\x03\"\x1d\n\x0bStudySymbol\x12\x0e\n\x06symbol\x18\x01 \x01(\t\"\x8c\x02\n\tRuleEvent\x12\x1d\n\x05title\x18\x01 \x01(\x0b\x32\x0e.shared_1.Text\x12\x1c\n\x04\x62ody\x18\x02 \x01(\x0b\x32\x0e.shared_1.Text\x12\x0f\n\x07rule_id\x18\x03 \x01(\t\x12?\n\x17notification_properties\x18\x04 \x03(\x0b\x32\x1e.shared_1.NotificationProperty\x12\x36\n\x12when_utc_timestamp\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12%\n\rerror_details\x18\x06 \x01(\x0b\x32\x0e.shared_1.Text\x12\x11\n\trule_tags\x18\x07 \x03(\t\"6\n\x10OrderEventFilter\x12\x13\n\x0b\x66ilter_type\x18\x01 \x01(\r\x12\r\n\x05value\x18\x02 \x01(\t\"B\n\x0eSetRuleRequest\x12\x30\n\x0frule_definition\x18\x01 \x02(\x0b\x32\x17.rules_1.RuleDefinition\"\x0f\n\rSetRuleResult\"]\n\x11ModifyRuleRequest\x12\x0f\n\x07rule_id\x18\x01 \x02(\t\x12 \n\x07\x61\x63tions\x18\x02 \x03(\x0b\x32\x0f.rules_1.Action\x12\x15\n\rrule_revision\x18\x03 \x01(\x04\"\x12\n\x10ModifyRuleResult\";\n\x11\x44\x65leteRuleRequest\x12\x0f\n\x07rule_id\x18\x01 \x02(\t\x12\x15\n\rrule_revision\x18\x02 \x01(\x04\"\x12\n\x10\x44\x65leteRuleResult\"\x17\n\x0fRuleListRequestJ\x04\x08\x01\x10\x02\"X\n\x0eRuleListResult\x12\x31\n\x10rule_definitions\x18\x01 \x03(\x0b\x32\x17.rules_1.RuleDefinition\x12\x13\n\x0bis_snapshot\x18\x02 \x01(\x08\"\x9a\x01\n\x17RuleEventHistoryRequest\x12\x36\n\x12\x66rom_utc_timestamp\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x34\n\x10to_utc_timestamp\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x11\n\trule_tags\x18\x03 \x03(\t\"S\n\x16RuleEventHistoryResult\x12\'\n\x0brule_events\x18\x01 \x03(\x0b\x32\x12.rules_1.RuleEvent\x12\x10\n\x08\x63omplete\x18\x02 \x01(\x08\"*\n\x15RuleEventSubscription\x12\x11\n\trule_tags\x18\x01 \x03(\t\"F\n\x1bRuleEventSubscriptionStatus\x12\'\n\x0brule_events\x18\x01 \x03(\x0b\x32\x12.rules_1.RuleEvent\"\xb8\x01\n%CreateOrModifyDestinationGroupRequest\x12\x1c\n\x14\x64\x65stination_group_id\x18\x01 \x02(\t\x12\x34\n\x15\x64\x65stination_to_remove\x18\x02 \x01(\x0b\x32\x15.shared_1.Destination\x12;\n\x1c\x64\x65stination_to_add_or_update\x18\x03 \x01(\x0b\x32\x15.shared_1.Destination\"&\n$CreateOrModifyDestinationGroupResult\"\x1d\n\x1b\x44\x65stinationGroupListRequest\"S\n\x1a\x44\x65stinationGroupListResult\x12\x35\n\x12\x64\x65stination_groups\x18\x01 \x03(\x0b\x32\x19.rules_1.DestinationGroup\"]\n\x10\x44\x65stinationGroup\x12\x1c\n\x14\x64\x65stination_group_id\x18\x01 \x02(\t\x12+\n\x0c\x64\x65stinations\x18\x02 \x03(\x0b\x32\x15.shared_1.Destination\"\xa5\x01\n&UpdateDestinationExpirationTimeRequest\x12\x34\n\x10\x61pple_push_notif\x18\x01 \x01(\x0b\x32\x18.shared_1.ApplePushNotifH\x00\x12\x36\n\x11google_push_notif\x18\x02 \x01(\x0b\x32\x19.shared_1.GooglePushNotifH\x00\x42\r\n\x0b\x64\x65stination\"\'\n%UpdateDestinationExpirationTimeResult*B\n\x14OrderEventFilterType\x12*\n&ORDER_EVENT_FILTER_TYPE_CONTRIBUTOR_ID\x10\x01')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'WebAPI.rules_1_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_ORDEREVENTRULE'].fields_by_name['account_ids']._loaded_options = None
  _globals['_ORDEREVENTRULE'].fields_by_name['account_ids']._serialized_options = b'\030\001'
  _globals['_ORDEREVENTFILTERTYPE']._serialized_start=6208
  _globals['_ORDEREVENTFILTERTYPE']._serialized_end=6274
  _globals['_RULEREQUEST']._serialized_start=90
  _globals['_RULEREQUEST']._serialized_end=780
  _globals['_RULERESULT']._serialized_start=783
  _globals['_RULERESULT']._serialized_end=1676
  _globals['_RULERESULT_RESULTCODE']._serialized_start=1501
  _globals['_RULERESULT_RESULTCODE']._serialized_end=1670
  _globals['_RULEDEFINITION']._serialized_start=1679
  _globals['_RULEDEFINITION']._serialized_end=2005
  _globals['_ACTION']._serialized_start=2007
  _globals['_ACTION']._serialized_end=2130
  _globals['_GOFLATACTION']._serialized_start=2132
  _globals['_GOFLATACTION']._serialized_end=2146
  _globals['_ORDEREVENTRULE']._serialized_start=2149
  _globals['_ORDEREVENTRULE']._serialized_end=2288
  _globals['_CONDITIONRULE']._serialized_start=2291
  _globals['_CONDITIONRULE']._serialized_end=2575
  _globals['_CONDITIONRULE_TRIGGERINGTYPE']._serialized_start=2503
  _globals['_CONDITIONRULE_TRIGGERINGTYPE']._serialized_end=2575
  _globals['_TEMPLATETEXT']._serialized_start=2577
  _globals['_TEMPLATETEXT']._serialized_end=2605
  _globals['_EXPRESSION']._serialized_start=2608
  _globals['_EXPRESSION']._serialized_end=3086
  _globals['_EXPRESSION_OPERATOR']._serialized_start=2781
  _globals['_EXPRESSION_OPERATOR']._serialized_end=3067
  _globals['_OPERAND']._serialized_start=3089
  _globals['_OPERAND']._serialized_end=3322
  _globals['_CONSTANT']._serialized_start=3324
  _globals['_CONSTANT']._serialized_end=3378
  _globals['_MARKETVARIABLE']._serialized_start=3381
  _globals['_MARKETVARIABLE']._serialized_end=3658
  _globals['_MARKETVARIABLE_TYPE']._serialized_start=3430
  _globals['_MARKETVARIABLE_TYPE']._serialized_end=3658
  _globals['_ACCOUNTVARIABLE']._serialized_start=3661
  _globals['_ACCOUNTVARIABLE']._serialized_end=4447
  _globals['_ACCOUNTVARIABLE_TYPE']._serialized_start=3695
  _globals['_ACCOUNTVARIABLE_TYPE']._serialized_end=4441
  _globals['_STUDYSYMBOL']._serialized_start=4449
  _globals['_STUDYSYMBOL']._serialized_end=4478
  _globals['_RULEEVENT']._serialized_start=4481
  _globals['_RULEEVENT']._serialized_end=4749
  _globals['_ORDEREVENTFILTER']._serialized_start=4751
  _globals['_ORDEREVENTFILTER']._serialized_end=4805
  _globals['_SETRULEREQUEST']._serialized_start=4807
  _globals['_SETRULEREQUEST']._serialized_end=4873
  _globals['_SETRULERESULT']._serialized_start=4875
  _globals['_SETRULERESULT']._serialized_end=4890
  _globals['_MODIFYRULEREQUEST']._serialized_start=4892
  _globals['_MODIFYRULEREQUEST']._serialized_end=4985
  _globals['_MODIFYRULERESULT']._serialized_start=4987
  _globals['_MODIFYRULERESULT']._serialized_end=5005
  _globals['_DELETERULEREQUEST']._serialized_start=5007
  _globals['_DELETERULEREQUEST']._serialized_end=5066
  _globals['_DELETERULERESULT']._serialized_start=5068
  _globals['_DELETERULERESULT']._serialized_end=5086
  _globals['_RULELISTREQUEST']._serialized_start=5088
  _globals['_RULELISTREQUEST']._serialized_end=5111
  _globals['_RULELISTRESULT']._serialized_start=5113
  _globals['_RULELISTRESULT']._serialized_end=5201
  _globals['_RULEEVENTHISTORYREQUEST']._serialized_start=5204
  _globals['_RULEEVENTHISTORYREQUEST']._serialized_end=5358
  _globals['_RULEEVENTHISTORYRESULT']._serialized_start=5360
  _globals['_RULEEVENTHISTORYRESULT']._serialized_end=5443
  _globals['_RULEEVENTSUBSCRIPTION']._serialized_start=5445
  _globals['_RULEEVENTSUBSCRIPTION']._serialized_end=5487
  _globals['_RULEEVENTSUBSCRIPTIONSTATUS']._serialized_start=5489
  _globals['_RULEEVENTSUBSCRIPTIONSTATUS']._serialized_end=5559
  _globals['_CREATEORMODIFYDESTINATIONGROUPREQUEST']._serialized_start=5562
  _globals['_CREATEORMODIFYDESTINATIONGROUPREQUEST']._serialized_end=5746
  _globals['_CREATEORMODIFYDESTINATIONGROUPRESULT']._serialized_start=5748
  _globals['_CREATEORMODIFYDESTINATIONGROUPRESULT']._serialized_end=5786
  _globals['_DESTINATIONGROUPLISTREQUEST']._serialized_start=5788
  _globals['_DESTINATIONGROUPLISTREQUEST']._serialized_end=5817
  _globals['_DESTINATIONGROUPLISTRESULT']._serialized_start=5819
  _globals['_DESTINATIONGROUPLISTRESULT']._serialized_end=5902
  _globals['_DESTINATIONGROUP']._serialized_start=5904
  _globals['_DESTINATIONGROUP']._serialized_end=5997
  _globals['_UPDATEDESTINATIONEXPIRATIONTIMEREQUEST']._serialized_start=6000
  _globals['_UPDATEDESTINATIONEXPIRATIONTIMEREQUEST']._serialized_end=6165
  _globals['_UPDATEDESTINATIONEXPIRATIONTIMERESULT']._serialized_start=6167
  _globals['_UPDATEDESTINATIONEXPIRATIONTIMERESULT']._serialized_end=6206
# @@protoc_insertion_point(module_scope)
