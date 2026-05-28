#pragma once 
#include <optional>
#inclide "ticks.h"

enum class DataExtractionPolicy : uint8_t {
    ExtractTradeTickCQG = 0,
};


enum class QuoteTypeCQG : int {
    Trade = 0,
    BestBid = 1,
    BestAsk = 2,
    Bid = 3,
    Ask = 4,
    Settlement = 5,
    ImpliedBid = 10,
    ImpliedAsk = 11,
};

std::optional<TradeTick> extract_trade_tick_CQG(const py::tuple& quote);
std::optional<Tick> extract_raw_tick(const py::tuple& quote, DataExtractionPolicy policy);

int get_parsed_rtmd_index_from_policy(DataExtractionPolicy policy);