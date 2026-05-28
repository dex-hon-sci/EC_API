#include <cmath>
#include <optional>
#include <Python.h>
#include <pybind11/pybind11.h>
#include "ticks.h"
#include "data_extractors_cqg.h"

namespace py = pybind11;

double make_float(double significand, double exponent, int sign) {
    return (sign == 0 ? 1.0 : -1.0) * significand * pow(10, exponent);
}

int get_parsed_rtmd_index_from_policy(DataExtractionPolicy policy) {
    switch (policy) {
        case DataExtractionPolicy::ExtractTradeTickCQG:
            return static_cast<int>(QuoteTypeCQG::Q_TYPE)
    }
}

template <typename T>
constexpr int idx(T field) {return static_cast<int>(field);}

std::optional<TradeTick> extract_trade_tick_CQG(py::tuple& raw_tick) {    
    if (raw_tick[ParsedRTMDCQG::Quote][q_idx_cqg(QuoteCQG::Q_TYPE)] != QuoteTypeCQG::Trade) {return std::nullopt;}
    int rtmd_q = idx<ParsedRTMDCQG>(ParsedRTMDCQG::Quote)
    double timestamp = raw_tick[rtmd_q][idx<>QuoteCQG(QuoteCQG::Q_UTC_TIME)];
    double price = raw_tick[rtmd_q][idx<QuoteCQG>(QuoteCQG::Q_SCALED_PRICE)] *raw_tick[rtmd_q][idx<QuoteCQG>(QuoteCQG::Q_CORRECT_PRICE_SCALE)];
    double volume = make_float(raw_tick[rtmd_q][idx<QuoteCQG>(QuoteCQG::Q_VOL_SIGNIFICAND)], raw_tick[rtmd_q][idx<QuoteCQG>(QuoteCQG::Q_VOL_EXPONENT)], 0);
    return TradeTick{timestamp, price, volume};
}


Tick extract_raw_tick(py::tuple* raw_tick, DataExtractionPolicy* policy) {
    if !PyTuple_Check(raw_tick) {
        return std::nullopt
    }
    
    switch (policy) {
        case DataExtractionPolicy::ExtractTradeTickCQG:
            return extract_trade_tick_CQG(raw_tick);
    }
    
};
