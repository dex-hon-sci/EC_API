#pragma once 

namespace QuoteCQG {
    constexpr int Q_CONTRACT_ID = 0;
    constexpr int Q_TYPE = 1;
    constexpr int Q_UTC_TIME = 2; //microseconds since epoch
    constexpr int Q_SCALED_PRICE = 3;
    constexpr int Q_SCALED_SOURCE_PRICE = 4;
    constexpr int Q_PRICE_YIELD = 5;
    constexpr int Q_VOL_SIGNIFICAND = 6;
    constexpr int Q_VOL_EXPONENT = 7;
    constexpr int Q_INDICATORS = 8;
    constexpr int Q_SALES_CONDITION = 9;
    constexpr int Q_TRADE_ATTRS = 10;
    constexpr int Q_SCALED_CURRENCY_RATE_PRICE = 11;
    constexpr int Q_SCALED_PREMIUM = 12;
    constexpr int Q_MARKET_STATE = 13;
    constexpr int Q_CORRECT_PRICE_SCALE = 14;
    constexpr int Q_IS_SNAPSHOT = 15;
    }
    
namespace MarketValueCQG {
    constexpr int MV_CONTRACT_ID = 0;
    constexpr int MV_SCALED_OPEN = 1;
    constexpr int MV_SCALED_HIGH = 2;
    constexpr int MV_SCALED_LOW = 3;
    constexpr int MV_SCALED_CLOSE = 4;
    constexpr int MV_VOL_SIGNIFICAND = 5;
    constexpr int MV_VOL_EXPONENT = 6;
    constexpr int MV_LAST_PRICE_NO_SETTLEMENT = 7;
    constexpr int MV_SCALE_EX_CLOSE_PRICE = 8;
    constexpr int MV_SCALED_YESTERDAY_SETTLEMENT = 9;
    constexpr int MV_SCALED_INDICATIVE_OPEN = 10;
    constexpr int MV_OI_SIGNIFICAND = 11;
    constexpr int MV_OI_EXPONENT = 12;
    constexpr int MV_INDICATIVE_OI_VOL_SIGNIFICAND = 13;
    constexpr int MV_INDICATIVE_OI_VOL_EXPONENT = 14;
    constexpr int MV_TICK_VOL = 15;
    constexpr int MV_SCALED_SETTLEMENT = 16;
    constexpr int MV_SCALED_MARKER_PRICE = 17;
    constexpr int MV_SCALED_LAST_TRADE_PRICE = 18;
    constexpr int MV_SCALED_TRADE_VOL_SIGNIFICAND = 19;
    constexpr int MV_SCALED_TRADE_VOL_EXPONENT = 20;
    constexpr int MV_LAST_TRADE_UTC_TIMESTAMP = 21; //(seconds.nanos)
    constexpr int MV_CLEARED_FIELDS = 22;
    constexpr int MV_TRADE_DATE = 23;
    constexpr int MV_SESSION_INDEX = 24;
    constexpr int MV_MARKET_YIELDS = 25;
    constexpr int MV_SCALED_CURRENCY_RATE_PRICE = 26;
    constexpr int MV_MARKET_STATE = 27;
    constexpr int MV_CORRECT_PRICE_SCALE = 28;
    constexpr int MV_IS_SNAPSHOT = 29;
}

namespace MarketYieldsCQG {
    constexpr int MY_YIELD_OPEN_PRICE = 0;  // [0]  yield_of_open_price              float
    constexpr int MY_YIELD_HIGH_PRICE = 1;  // [1]  yield_of_high_price              float
    constexpr int MY_YIELD_LOW_PRICE = 2 ; // [2]  yield_of_low_price               float
    constexpr int MY_YIELD_CLOSE_PRICE = 3;  // [3]  yield_of_close_price             float
    constexpr int MY_YIELD_YESTERDAY_SETTLEMENT = 4;  // [4]  yield_of_yesterday_settlement    float
    constexpr int MY_YIELD_INDICATIVE_OPEN = 5;  // [5]  yield_of_indicative_open         float
    constexpr int MY_YIELD_SETTLEMENT = 6;  // [6]  yield_of_settlement              float
}

namespace MarketStateCQG {
    constexpr int MS_EXCHANGE_STATE = 0;
    constexpr int MS_ALLOW_PLACE_ORDER = 1;  // [1]  allow_place_order                bool
    constexpr int MS_ALLOW_CANCEL_ORDER = 2;  // [2]  allow_cancel_order               bool
    constexpr int MS_ALLOW_MODIFY_ORDER = 3; // [3]  allow_modify_order               bool
    constexpr int MS_MATCH_ENABLED = 4;  // [4]  matching_enabled                 bool
    constexpr int MS_IS_SNAPSHOT = 5;  // [5]  is_snapshot                      bool
}

namespace TradeAttrsCQG {
    constexpr int TA_BUYER = 0;
    constexpr int TA_SELLER = 1;
    constexpr int TA_TRADE_TYPE = 2;
    constexpr int TA_MATCH_ID = 3;
    constexpr int TA_AGREEMENT_TIME_UTC = 4; //(seconds.nanos)
}