# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: WebAPI/metadata_2.proto
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
    'WebAPI/metadata_2.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from EC_API.ext.WebAPI import metadata_admin_2_pb2 as WebAPI_dot_metadata__admin__2__pb2
from EC_API.ext.WebAPI import strategy_definition_2_pb2 as WebAPI_dot_strategy__definition__2__pb2
from EC_API.ext.common import decimal_pb2 as common_dot_decimal__pb2
from EC_API.ext.common import shared_1_pb2 as common_dot_shared__1__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x17WebAPI/metadata_2.proto\x12\nmetadata_2\x1a\x1dWebAPI/metadata_admin_2.proto\x1a\"WebAPI/strategy_definition_2.proto\x1a\x14\x63ommon/decimal.proto\x1a\x15\x63ommon/shared_1.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"f\n\x17SymbolResolutionRequest\x12\x0e\n\x06symbol\x18\x01 \x01(\t\x12\x17\n\x0fpreferred_types\x18\x02 \x01(\t\x12\x1b\n\x13preferred_countries\x18\x03 \x01(\t*\x05\x08\x64\x10\xc8\x01\"b\n\x16SymbolResolutionReport\x12\x37\n\x11\x63ontract_metadata\x18\x01 \x02(\x0b\x32\x1c.metadata_2.ContractMetadata\x12\x0f\n\x07\x64\x65leted\x18\x02 \x01(\x08\".\n\x17\x43ontractMetadataRequest\x12\x13\n\x0b\x63ontract_id\x18\x01 \x02(\r\"Q\n\x16\x43ontractMetadataReport\x12\x37\n\x11\x63ontract_metadata\x18\x01 \x01(\x0b\x32\x1c.metadata_2.ContractMetadata\"P\n\x0fTickSizeByPrice\x12\x11\n\ttick_size\x18\x01 \x02(\x01\x12\x12\n\ntick_value\x18\x02 \x02(\x01\x12\x16\n\x0e\x62oundary_price\x18\x03 \x02(\x01\"[\n\x12\x43onversionMetadata\x12!\n\x19\x63urrency_rate_contract_id\x18\x01 \x01(\r\x12\"\n\x1a\x63urrency_hedge_contract_id\x18\x02 \x01(\r\"\xa8\x13\n\x10\x43ontractMetadata\x12\x13\n\x0b\x63ontract_id\x18\x01 \x02(\r\x12\x17\n\x0f\x63ontract_symbol\x18\x02 \x02(\t\x12\x1b\n\x13\x63qg_contract_symbol\x18\x46 \x01(\t\x12\x1b\n\x13\x63orrect_price_scale\x18\x03 \x02(\x01\x12\x1b\n\x13\x64isplay_price_scale\x18\x04 \x02(\r\x12\x13\n\x0b\x64\x65scription\x18\x05 \x02(\t\x12 \n\x14\x65xtended_description\x18+ \x01(\tB\x02\x18\x01\x12\r\n\x05title\x18\x06 \x02(\t\x12\x11\n\ttick_size\x18\x07 \x02(\x01\x12\x10\n\x08\x63urrency\x18\x08 \x02(\t\x12\x12\n\ntick_value\x18\t \x02(\x01\x12\x10\n\x08\x63\x66i_code\x18\n \x02(\t\x12\x16\n\x0eis_most_active\x18\x0b \x01(\x08\x12\x19\n\x11last_trading_date\x18\x0c \x01(\x12\x12\x19\n\x11\x66irst_notice_date\x18\r \x01(\x12\x12\"\n\x1aunderlying_contract_symbol\x18\x0e \x01(\t\x12\x14\n\x0cmargin_style\x18\x0f \x01(\r\x12\x1d\n\x15instrument_group_name\x18\x10 \x02(\t\x12\x17\n\x0fsession_info_id\x18\x11 \x02(\x11\x12\x0b\n\x03mic\x18\x12 \x01(\t\x12\x17\n\x0fmic_description\x18, \x01(\t\x12\x19\n\x11market_data_delay\x18\x14 \x01(\x12\x12\x18\n\x10\x65nd_of_day_delay\x18; \x01(\x12\x12#\n\x1bshort_instrument_group_name\x18\x15 \x02(\t\x12$\n\x1cinstrument_group_description\x18\x16 \x02(\t\x12\x38\n\x13tick_sizes_by_price\x18\x17 \x03(\x0b\x32\x1b.metadata_2.TickSizeByPrice\x12\x0e\n\x06strike\x18\x1a \x01(\x11\x12\x14\n\x0cstrike_price\x18\x1b \x01(\x01\x12\x1a\n\x12strike_price_scale\x18V \x01(\r\x12\x12\n\ndialect_id\x18\x1c \x01(\t\x12\x14\n\x0c\x63ountry_code\x18\x1d \x02(\t\x12\x46\n\x13strategy_definition\x18\x1e \x01(\x0b\x32).strategy_definition_2.StrategyDefinition\x12\x15\n\rcontract_size\x18\x1f \x01(\t\x12\x19\n\x11position_tracking\x18  \x01(\r\x12(\n\x19speculation_type_required\x18! \x01(\x08:\x05\x66\x61lse\x12\x1b\n\x13maturity_month_year\x18\" \x01(\t\x12\x15\n\rmaturity_date\x18\x35 \x01(\x12\x12\x38\n\x12price_display_mode\x18# \x01(\x0e\x32\x1c.metadata_2.PriceDisplayMode\x12\x18\n\x10\x66oreign_currency\x18\' \x01(\t\x12&\n\x0cvolume_scale\x18( \x01(\x0b\x32\x0c.cqg.DecimalB\x02\x18\x01\x12\"\n\x17volume_display_exponent\x18) \x01(\x11:\x01\x30\x12*\n\x14trade_size_increment\x18* \x01(\x0b\x32\x0c.cqg.Decimal\x12!\n\x19has_inverted_price_ladder\x18< \x01(\x08\x12$\n\x1c\x64om_ladder_compression_ratio\x18- \x01(\r\x12%\n\x16\x65xpect_off_tick_prices\x18. \x01(\x08:\x05\x66\x61lse\x12!\n\x13has_exchange_volume\x18/ \x01(\x08:\x04true\x12\x12\n\nhas_yields\x18= \x01(\x08\x12\x0c\n\x04isin\x18\x30 \x01(\t\x12\x16\n\x0einitial_margin\x18R \x01(\x01\x12\x1a\n\x12maintenance_margin\x18\x31 \x01(\x01\x12,\n\x16\x63ontract_size_in_units\x18\x32 \x01(\x0b\x32\x0c.cqg.Decimal\x12*\n\x12\x63ontract_size_unit\x18\x33 \x01(\x0b\x32\x0e.shared_1.Text\x12\x1a\n\x12last_delivery_date\x18\x34 \x01(\x12\x12G\n\x16\x63ontributor_parameters\x18\x36 \x03(\x0b\x32\'.metadata_admin_2.ContributorParameters\x12\x1b\n\x13listing_period_type\x18\x37 \x01(\r\x12\x1c\n\x14listing_period_value\x18\x38 \x01(\r\x12\x11\n\tsymbol_id\x18\x39 \x01(\t\x12\x16\n\x07\x64\x65leted\x18: \x01(\x08:\x05\x66\x61lse\x12\x1c\n\x14\x63ontributor_group_id\x18> \x01(\x11\x12\x1a\n\x12source_contract_id\x18? \x01(\r\x12\x0e\n\x06issuer\x18\x42 \x01(\t\x12\x1a\n\x12option_maturity_id\x18\x43 \x01(\t\x12;\n\x13\x63onversion_metadata\x18\x44 \x01(\x0b\x32\x1e.metadata_2.ConversionMetadata\x12\x1d\n\x15market_state_group_id\x18\x45 \x01(\x11\x12\x19\n\x11settlement_method\x18G \x01(\r\x12\x16\n\x0e\x65xercise_style\x18H \x01(\r\x12\x1a\n\x12pricing_convention\x18I \x01(\r\x12\"\n\x1ais_user_defined_instrument\x18J \x01(\x08\x12\x1f\n\x17\x62\x61r_building_tick_types\x18K \x03(\r\x12\x11\n\tquoted_in\x18L \x01(\t\x12\x19\n\x11product_symbol_id\x18M \x01(\t\x12\x1e\n\x16hedge_with_contract_id\x18N \x01(\r\x12!\n\x19\x61\x63tual_future_contract_id\x18O \x01(\r\x12\x13\n\x0b\x65xchange_id\x18P \x01(\x11\x12\x1d\n\x15supports_continuation\x18Q \x01(\x08\x12#\n\x1binstrument_business_type_id\x18S \x01(\r\x12\x15\n\rclose_sources\x18T \x03(\r\x12\x17\n\x0fopen_close_type\x18U \x01(\r\x12\x14\n\x0cis_synthetic\x18W \x01(\x08\"@\n\x0bMarginStyle\x12\x17\n\x13MARGIN_STYLE_FUTURE\x10\x01\x12\x18\n\x14MARGIN_STYLE_PREMIUM\x10\x02*\x06\x08\xac\x02\x10\xad\x02J\x04\x08\x18\x10\x19J\x04\x08\x19\x10\x1aJ\x04\x08$\x10\'\":\n\x1a\x43ontributorMetadataRequest\x12\x1c\n\x14\x63ontributor_group_id\x18\x01 \x01(\x11\"Z\n\x19\x43ontributorMetadataReport\x12=\n\x14\x63ontributor_metadata\x18\x01 \x03(\x0b\x32\x1f.metadata_2.ContributorMetadata\"a\n\x13\x43ontributorMetadata\x12\x16\n\x0e\x63ontributor_id\x18\x01 \x01(\x11\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12\x0f\n\x07\x64\x65leted\x18\x04 \x01(\x08\";\n\x19OptionMaturityListRequest\x12\x1e\n\x16underlying_contract_id\x18\x01 \x02(\r\"Y\n\x18OptionMaturityListReport\x12=\n\x11option_maturities\x18\x01 \x03(\x0b\x32\".metadata_2.OptionMaturityMetadata\"\x85\x03\n\x16OptionMaturityMetadata\x12\n\n\x02id\x18\x01 \x02(\t\x12\x0c\n\x04name\x18\x02 \x02(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x02(\t\x12\x10\n\x08\x63\x66i_code\x18\x04 \x01(\t\x12\x0f\n\x07\x64\x65leted\x18\x07 \x01(\x08\x12\x19\n\x11last_trading_date\x18\x08 \x01(\x12\x12H\n$last_trading_date_time_utc_timestamp\x18\x14 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x1b\n\x13maturity_month_year\x18\t \x01(\t\x12\x1d\n\x15instrument_group_name\x18\n \x01(\t\x12\x1e\n\x16instrument_group_empty\x18\x11 \x01(\x08\x12\x1b\n\x13listing_period_type\x18\x12 \x01(\r\x12\x1c\n\x14listing_period_value\x18\x13 \x01(\r\x12\x11\n\treserved1\x18\x05 \x01(\x08J\x04\x08\x06\x10\x07J\x04\x08\x0b\x10\x11\"5\n\x16InstrumentGroupRequest\x12\x1b\n\x13instrument_group_id\x18\x01 \x02(\t\"M\n\x15InstrumentGroupReport\x12\x34\n\x0binstruments\x18\x01 \x03(\x0b\x32\x1f.metadata_2.InstrumentGroupItem\"\xa3\x02\n\x13InstrumentGroupItem\x12\n\n\x02id\x18\x01 \x02(\t\x12\x0c\n\x04name\x18\x02 \x02(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x02(\t\x12\x10\n\x08\x63\x66i_code\x18\x04 \x01(\t\x12\x37\n\x11\x63ontract_metadata\x18\x06 \x01(\x0b\x32\x1c.metadata_2.ContractMetadata\x12\x0f\n\x07\x64\x65leted\x18\x07 \x01(\x08\x12\x19\n\x11last_trading_date\x18\x08 \x01(\x12\x12\x1b\n\x13maturity_month_year\x18\t \x01(\t\x12\x1d\n\x15instrument_group_name\x18\n \x01(\t\x12\x11\n\treserved1\x18\x05 \x01(\x08\x12\x11\n\treserved2\x18\x0b \x01(\tJ\x04\x08\x0c\x10\x11\";\n\x1aMarketStateMetadataRequest\x12\x1d\n\x15market_state_group_id\x18\x01 \x02(\x11\"n\n\x19MarketStateMetadataReport\x12Q\n\x1fmarket_state_attribute_metadata\x18\x01 \x03(\x0b\x32(.metadata_2.MarketStateAttributeMetadata\"\x8a\x01\n\x1cMarketStateAttributeMetadata\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05level\x18\x02 \x01(\r\x12<\n\x0evalue_metadata\x18\x03 \x03(\x0b\x32$.metadata_2.MarketStateValueMetadata\x12\x0f\n\x07\x64\x65leted\x18\x04 \x01(\x08\"O\n\x18MarketStateValueMetadata\x12\r\n\x05value\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12\x0f\n\x07\x64\x65leted\x18\x03 \x01(\x08\"\x19\n\x17\x45xchangeMetadataRequest\"Q\n\x16\x45xchangeMetadataReport\x12\x37\n\x11\x65xchange_metadata\x18\x01 \x03(\x0b\x32\x1c.metadata_2.ExchangeMetadata\"\xa9\x02\n\x10\x45xchangeMetadata\x12\x13\n\x0b\x65xchange_id\x18\x01 \x01(\x11\x12\x18\n\x10\x63ontributor_type\x18\x02 \x01(\r\x12\x14\n\x0c\x61\x62\x62reviation\x18\x03 \x01(\t\x12\x0c\n\x04name\x18\x04 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x05 \x01(\t\x12\x0f\n\x07\x64\x65leted\x18\x06 \x01(\x08\"\x9b\x01\n\x0f\x43ontributorType\x12\x1e\n\x1a\x43ONTRIBUTOR_TYPE_UNDEFINED\x10\x00\x12$\n CONTRIBUTOR_TYPE_US_EQUITY_STYLE\x10\x01\x12\x1e\n\x1a\x43ONTRIBUTOR_TYPE_OTC_STYLE\x10\x02\x12\"\n\x1e\x43ONTRIBUTOR_TYPE_CLUSTER_STYLE\x10\x03\":\n\"InstrumentGroupBySecuritiesRequest\x12\x14\n\x0csecurity_ids\x18\x01 \x03(\t\"Y\n!InstrumentGroupBySecuritiesReport\x12\x34\n\x0binstruments\x18\x01 \x03(\x0b\x32\x1f.metadata_2.InstrumentGroupItem\"V\n InstrumentGroupByExchangeRequest\x12\x13\n\x0b\x65xchange_id\x18\x01 \x01(\x11\x12\x1d\n\x15instrument_group_type\x18\x02 \x01(\r\"W\n\x1fInstrumentGroupByExchangeReport\x12\x34\n\x0binstruments\x18\x01 \x03(\x0b\x32\x1f.metadata_2.InstrumentGroupItem\"O\n\x19\x45xchangeSecuritiesRequest\x12\x13\n\x0b\x65xchange_id\x18\x01 \x01(\x11\x12\x1d\n\x15instrument_group_type\x18\x02 \x01(\r\"U\n\x18\x45xchangeSecuritiesReport\x12\x39\n\x13\x65xchange_securities\x18\x01 \x03(\x0b\x32\x1c.metadata_2.SecurityMetadata\"\x82\x02\n\x12ProcessingMetadata\x12\x10\n\x08\x63urrency\x18\x01 \x01(\t\x12\x11\n\ttick_size\x18\x02 \x01(\x01\x12\x12\n\ntick_value\x18\x03 \x01(\x01\x12,\n\x16\x63ontract_size_in_units\x18\x04 \x01(\x0b\x32\x0c.cqg.Decimal\x12*\n\x12\x63ontract_size_unit\x18\x05 \x01(\x0b\x32\x0e.shared_1.Text\x12+\n#currency_rate_instrument_group_name\x18\x06 \x01(\t\x12,\n$currency_hedge_instrument_group_name\x18\x07 \x01(\t\"\x86\x04\n\x10SecurityMetadata\x12\x13\n\x0bsecurity_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x0e \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x0f \x01(\t\x12\x10\n\x08\x63\x66i_code\x18\x02 \x01(\t\x12\x14\n\x08\x63urrency\x18\x03 \x01(\tB\x02\x18\x01\x12\x15\n\ttick_size\x18\x04 \x01(\x01\x42\x02\x18\x01\x12\x16\n\ntick_value\x18\x05 \x01(\x01\x42\x02\x18\x01\x12\x17\n\x0bperiod_type\x18\x06 \x01(\rB\x02\x18\x01\x12\x18\n\x0cperiod_value\x18\x07 \x01(\rB\x02\x18\x01\x12\x30\n\x16\x63ontract_size_in_units\x18\x08 \x01(\x0b\x32\x0c.cqg.DecimalB\x02\x18\x01\x12.\n\x12\x63ontract_size_unit\x18\t \x01(\x0b\x32\x0e.shared_1.TextB\x02\x18\x01\x12G\n\x16\x63ontributor_parameters\x18\n \x03(\x0b\x32\'.metadata_admin_2.ContributorParameters\x12\x11\n\tsymbol_id\x18\x0b \x01(\t\x12$\n\x1csource_instrument_group_name\x18\x0c \x01(\t\x12;\n\x13processing_metadata\x18\r \x03(\x0b\x32\x1e.metadata_2.ProcessingMetadata\x12\x0f\n\x07\x64\x65leted\x18\x10 \x01(\x08\"\x85\x01\n\x0f\x43ountryMetadata\x12\x12\n\ncountry_id\x18\x01 \x01(\x11\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12\x14\n\x0c\x61\x62\x62reviation\x18\x04 \x01(\t\x12\x14\n\x0c\x63ountry_code\x18\x06 \x01(\t\x12\x0f\n\x07\x64\x65leted\x18\x05 \x01(\x08\"\x14\n\x12\x43ountryListRequest\"C\n\x11\x43ountryListReport\x12.\n\tcountries\x18\x01 \x03(\x0b\x32\x1b.metadata_2.CountryMetadata*\xb4\x01\n\x14PositionTrackingType\x12\'\n#POSITION_TRACKING_TYPE_NET_POSITION\x10\x01\x12\x38\n4POSITION_TRACKING_TYPE_LONG_SHORT_WITH_IMPLIED_CLOSE\x10\x02\x12\x39\n5POSITION_TRACKING_TYPE_LONG_SHORT_WITH_EXPLICIT_CLOSE\x10\x03*v\n\x10PriceDisplayMode\x12 \n\x1cPRICE_DISPLAY_MODE_NUMERATOR\x10\x00\x12\x1e\n\x1aPRICE_DISPLAY_MODE_ROUNDED\x10\x01\x12 \n\x1cPRICE_DISPLAY_MODE_TRUNCATED\x10\x02*\xe0\x02\n\nPeriodType\x12\x15\n\x11PERIOD_TYPE_MONTH\x10\x00\x12\x17\n\x13PERIOD_TYPE_QUARTER\x10\x01\x12\x1b\n\x17PERIOD_TYPE_SEMI_ANNUAL\x10\x02\x12\x14\n\x10PERIOD_TYPE_YEAR\x10\x03\x12\x1b\n\x17PERIOD_TYPE_DAY_OF_WEEK\x10\x04\x12\x1c\n\x18PERIOD_TYPE_DAY_OF_MONTH\x10\x05\x12\x1b\n\x17PERIOD_TYPE_DAY_OF_YEAR\x10\x06\x12\x1d\n\x19PERIOD_TYPE_WEEK_OF_MONTH\x10\x07\x12\x1c\n\x18PERIOD_TYPE_WEEK_OF_YEAR\x10\x08\x12\x16\n\x12PERIOD_TYPE_SECOND\x10\t\x12\x16\n\x12PERIOD_TYPE_MINUTE\x10\n\x12\x14\n\x10PERIOD_TYPE_HOUR\x10\x0b\x12\x14\n\x10PERIOD_TYPE_DATE\x10\x0c*|\n\x11\x43QGInstrumentType\x12\x1e\n\x1a\x43QG_INSTRUMENT_TYPE_FUTURE\x10\x01\x12#\n\x1f\x43QG_INSTRUMENT_TYPE_CALL_OPTION\x10\x02\x12\"\n\x1e\x43QG_INSTRUMENT_TYPE_PUT_OPTION\x10\x03*N\n\x10SettlementMethod\x12\x1a\n\x16SETTLEMENT_METHOD_CASH\x10\x01\x12\x1e\n\x1aSETTLEMENT_METHOD_PHYSICAL\x10\x02*I\n\rExerciseStyle\x12\x1b\n\x17\x45XERCISE_STYLE_EUROPEAN\x10\x01\x12\x1b\n\x17\x45XERCISE_STYLE_AMERICAN\x10\x02*k\n\x11PricingConvention\x12\x1c\n\x18PRICING_CONVENTION_PRICE\x10\x01\x12\x1c\n\x18PRICING_CONVENTION_GROSS\x10\x02\x12\x1a\n\x16PRICING_CONVENTION_NET\x10\x03*h\n\x0b\x43loseSource\x12\x1b\n\x17\x43LOSE_SOURCE_LAST_QUOTE\x10\x01\x12\x1b\n\x17\x43LOSE_SOURCE_SETTLEMENT\x10\x02\x12\x1f\n\x1b\x43LOSE_SOURCE_EXCHANGE_CLOSE\x10\x03*i\n\rOpenCloseType\x12\x1c\n\x18OPEN_CLOSE_TYPE_NOT_USED\x10\x00\x12\x1c\n\x18OPEN_CLOSE_TYPE_OPTIONAL\x10\x01\x12\x1c\n\x18OPEN_CLOSE_TYPE_REQUIRED\x10\x02*B\n\x13InstrumentGroupType\x12+\n\'INSTRUMENT_GROUP_TYPE_EXCHANGE_STRATEGY\x10\x01')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'WebAPI.metadata_2_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_CONTRACTMETADATA'].fields_by_name['extended_description']._loaded_options = None
  _globals['_CONTRACTMETADATA'].fields_by_name['extended_description']._serialized_options = b'\030\001'
  _globals['_CONTRACTMETADATA'].fields_by_name['volume_scale']._loaded_options = None
  _globals['_CONTRACTMETADATA'].fields_by_name['volume_scale']._serialized_options = b'\030\001'
  _globals['_SECURITYMETADATA'].fields_by_name['currency']._loaded_options = None
  _globals['_SECURITYMETADATA'].fields_by_name['currency']._serialized_options = b'\030\001'
  _globals['_SECURITYMETADATA'].fields_by_name['tick_size']._loaded_options = None
  _globals['_SECURITYMETADATA'].fields_by_name['tick_size']._serialized_options = b'\030\001'
  _globals['_SECURITYMETADATA'].fields_by_name['tick_value']._loaded_options = None
  _globals['_SECURITYMETADATA'].fields_by_name['tick_value']._serialized_options = b'\030\001'
  _globals['_SECURITYMETADATA'].fields_by_name['period_type']._loaded_options = None
  _globals['_SECURITYMETADATA'].fields_by_name['period_type']._serialized_options = b'\030\001'
  _globals['_SECURITYMETADATA'].fields_by_name['period_value']._loaded_options = None
  _globals['_SECURITYMETADATA'].fields_by_name['period_value']._serialized_options = b'\030\001'
  _globals['_SECURITYMETADATA'].fields_by_name['contract_size_in_units']._loaded_options = None
  _globals['_SECURITYMETADATA'].fields_by_name['contract_size_in_units']._serialized_options = b'\030\001'
  _globals['_SECURITYMETADATA'].fields_by_name['contract_size_unit']._loaded_options = None
  _globals['_SECURITYMETADATA'].fields_by_name['contract_size_unit']._serialized_options = b'\030\001'
  _globals['_POSITIONTRACKINGTYPE']._serialized_start=6703
  _globals['_POSITIONTRACKINGTYPE']._serialized_end=6883
  _globals['_PRICEDISPLAYMODE']._serialized_start=6885
  _globals['_PRICEDISPLAYMODE']._serialized_end=7003
  _globals['_PERIODTYPE']._serialized_start=7006
  _globals['_PERIODTYPE']._serialized_end=7358
  _globals['_CQGINSTRUMENTTYPE']._serialized_start=7360
  _globals['_CQGINSTRUMENTTYPE']._serialized_end=7484
  _globals['_SETTLEMENTMETHOD']._serialized_start=7486
  _globals['_SETTLEMENTMETHOD']._serialized_end=7564
  _globals['_EXERCISESTYLE']._serialized_start=7566
  _globals['_EXERCISESTYLE']._serialized_end=7639
  _globals['_PRICINGCONVENTION']._serialized_start=7641
  _globals['_PRICINGCONVENTION']._serialized_end=7748
  _globals['_CLOSESOURCE']._serialized_start=7750
  _globals['_CLOSESOURCE']._serialized_end=7854
  _globals['_OPENCLOSETYPE']._serialized_start=7856
  _globals['_OPENCLOSETYPE']._serialized_end=7961
  _globals['_INSTRUMENTGROUPTYPE']._serialized_start=7963
  _globals['_INSTRUMENTGROUPTYPE']._serialized_end=8029
  _globals['_SYMBOLRESOLUTIONREQUEST']._serialized_start=184
  _globals['_SYMBOLRESOLUTIONREQUEST']._serialized_end=286
  _globals['_SYMBOLRESOLUTIONREPORT']._serialized_start=288
  _globals['_SYMBOLRESOLUTIONREPORT']._serialized_end=386
  _globals['_CONTRACTMETADATAREQUEST']._serialized_start=388
  _globals['_CONTRACTMETADATAREQUEST']._serialized_end=434
  _globals['_CONTRACTMETADATAREPORT']._serialized_start=436
  _globals['_CONTRACTMETADATAREPORT']._serialized_end=517
  _globals['_TICKSIZEBYPRICE']._serialized_start=519
  _globals['_TICKSIZEBYPRICE']._serialized_end=599
  _globals['_CONVERSIONMETADATA']._serialized_start=601
  _globals['_CONVERSIONMETADATA']._serialized_end=692
  _globals['_CONTRACTMETADATA']._serialized_start=695
  _globals['_CONTRACTMETADATA']._serialized_end=3167
  _globals['_CONTRACTMETADATA_MARGINSTYLE']._serialized_start=3077
  _globals['_CONTRACTMETADATA_MARGINSTYLE']._serialized_end=3141
  _globals['_CONTRIBUTORMETADATAREQUEST']._serialized_start=3169
  _globals['_CONTRIBUTORMETADATAREQUEST']._serialized_end=3227
  _globals['_CONTRIBUTORMETADATAREPORT']._serialized_start=3229
  _globals['_CONTRIBUTORMETADATAREPORT']._serialized_end=3319
  _globals['_CONTRIBUTORMETADATA']._serialized_start=3321
  _globals['_CONTRIBUTORMETADATA']._serialized_end=3418
  _globals['_OPTIONMATURITYLISTREQUEST']._serialized_start=3420
  _globals['_OPTIONMATURITYLISTREQUEST']._serialized_end=3479
  _globals['_OPTIONMATURITYLISTREPORT']._serialized_start=3481
  _globals['_OPTIONMATURITYLISTREPORT']._serialized_end=3570
  _globals['_OPTIONMATURITYMETADATA']._serialized_start=3573
  _globals['_OPTIONMATURITYMETADATA']._serialized_end=3962
  _globals['_INSTRUMENTGROUPREQUEST']._serialized_start=3964
  _globals['_INSTRUMENTGROUPREQUEST']._serialized_end=4017
  _globals['_INSTRUMENTGROUPREPORT']._serialized_start=4019
  _globals['_INSTRUMENTGROUPREPORT']._serialized_end=4096
  _globals['_INSTRUMENTGROUPITEM']._serialized_start=4099
  _globals['_INSTRUMENTGROUPITEM']._serialized_end=4390
  _globals['_MARKETSTATEMETADATAREQUEST']._serialized_start=4392
  _globals['_MARKETSTATEMETADATAREQUEST']._serialized_end=4451
  _globals['_MARKETSTATEMETADATAREPORT']._serialized_start=4453
  _globals['_MARKETSTATEMETADATAREPORT']._serialized_end=4563
  _globals['_MARKETSTATEATTRIBUTEMETADATA']._serialized_start=4566
  _globals['_MARKETSTATEATTRIBUTEMETADATA']._serialized_end=4704
  _globals['_MARKETSTATEVALUEMETADATA']._serialized_start=4706
  _globals['_MARKETSTATEVALUEMETADATA']._serialized_end=4785
  _globals['_EXCHANGEMETADATAREQUEST']._serialized_start=4787
  _globals['_EXCHANGEMETADATAREQUEST']._serialized_end=4812
  _globals['_EXCHANGEMETADATAREPORT']._serialized_start=4814
  _globals['_EXCHANGEMETADATAREPORT']._serialized_end=4895
  _globals['_EXCHANGEMETADATA']._serialized_start=4898
  _globals['_EXCHANGEMETADATA']._serialized_end=5195
  _globals['_EXCHANGEMETADATA_CONTRIBUTORTYPE']._serialized_start=5040
  _globals['_EXCHANGEMETADATA_CONTRIBUTORTYPE']._serialized_end=5195
  _globals['_INSTRUMENTGROUPBYSECURITIESREQUEST']._serialized_start=5197
  _globals['_INSTRUMENTGROUPBYSECURITIESREQUEST']._serialized_end=5255
  _globals['_INSTRUMENTGROUPBYSECURITIESREPORT']._serialized_start=5257
  _globals['_INSTRUMENTGROUPBYSECURITIESREPORT']._serialized_end=5346
  _globals['_INSTRUMENTGROUPBYEXCHANGEREQUEST']._serialized_start=5348
  _globals['_INSTRUMENTGROUPBYEXCHANGEREQUEST']._serialized_end=5434
  _globals['_INSTRUMENTGROUPBYEXCHANGEREPORT']._serialized_start=5436
  _globals['_INSTRUMENTGROUPBYEXCHANGEREPORT']._serialized_end=5523
  _globals['_EXCHANGESECURITIESREQUEST']._serialized_start=5525
  _globals['_EXCHANGESECURITIESREQUEST']._serialized_end=5604
  _globals['_EXCHANGESECURITIESREPORT']._serialized_start=5606
  _globals['_EXCHANGESECURITIESREPORT']._serialized_end=5691
  _globals['_PROCESSINGMETADATA']._serialized_start=5694
  _globals['_PROCESSINGMETADATA']._serialized_end=5952
  _globals['_SECURITYMETADATA']._serialized_start=5955
  _globals['_SECURITYMETADATA']._serialized_end=6473
  _globals['_COUNTRYMETADATA']._serialized_start=6476
  _globals['_COUNTRYMETADATA']._serialized_end=6609
  _globals['_COUNTRYLISTREQUEST']._serialized_start=6611
  _globals['_COUNTRYLISTREQUEST']._serialized_end=6631
  _globals['_COUNTRYLISTREPORT']._serialized_start=6633
  _globals['_COUNTRYLISTREPORT']._serialized_end=6700
# @@protoc_insertion_point(module_scope)
