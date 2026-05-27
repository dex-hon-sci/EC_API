namespace CQGQuote {
    constexpr int Q_CONTRACT_ID = 0;
    constexpr int Q_TYPE = 1;
    constexpr int UTC_TIME = 2; //microseconds since epoch
    constexpr int SCALED_PRICE = 3;
    constexpr int CORRECT_PRICE_SCALE = 14;
    }
    
Q_CONTRACT_ID = 0  # [0]  contract_id              int
Q_TYPE = 1  # [1]  type                     int
Q_UTC_TIME = 2  # [2]  quote_utc_time           int   (microseconds since epoch)
Q_SCALED_PRICE = 3  # [3]  scaled_price             int
Q_SCALED_SOURCE_PRICE = 4  # [4]  scaled_source_price      int
Q_PRICE_YIELD = 5  # [5]  price_yield              float
Q_VOL_SIGNIFICAND = 6  # [6]  vol_significand          int
Q_VOL_EXPONENT = 7  # [7]  vol_exponent             int
Q_INDICATORS = 8  # [8]  indicators               tuple[int, ...]
Q_SALES_CONDITION = 9  # [9]  sales_condition          int
Q_TRADE_ATTRS = 10  # [10] trade_attributes         tuple (TradeAttrsCQG)
Q_SCALED_CURRENCY_RATE_PRICE = 11  # [11] scaled_currency_rate     int
Q_SCALED_PREMIUM = 12  # [12] scaled_premium           int
Q_MARKET_STATE = 13  # [13] market_state             tuple (MarketStateCQG)
Q_CORRECT_PRICE_SCALE = 14  # [14] correct_price_scale      float
Q_IS_SNAPSHOT = 15  # [15] is_snapshot              bool
