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
            return ParsedRTMDCQG::Quote;
        default:
            throw std::invalid_argument("unhandled policy");
    }
}

template <typename T>
constexpr int idx(T field) {return static_cast<int>(field);}

std::optional<TradeTick> extract_trade_tick_CQG(const PyObject* raw_tick) {    
    // Data type check
    //if (!PyTuple_Check(raw_tick)) {return std::nullopt;}
    // max size check
    if (PyTuple_GET_SIZE(raw_tick) <= QuoteCQG::Q_CORRECT_PRICE_SCALE) return std::nullopt;

    // Quote type check
    PyObject* q_type = PyTuple_GET_ITEM(raw_tick, QuoteCQG::Q_TYPE);
    if (!PyLong_Check(q_type)) {return std::nullopt;}
    if (PyLong_AsLong(q_type)!=static_cast<int>(QuoteTypeCQG::Trade)) {return std::nullopt;}
    
    PyObject* ts = PyTuple_GET_ITEM(raw_tick, QuoteCQG::Q_UTC_TIME);
    PyObject* px = PyTuple_GET_ITEM(raw_tick, QuoteCQG::Q_SCALED_PRICE);
    PyObject* scl = PyTuple_GET_ITEM(raw_tick, QuoteCQG::Q_CORRECT_PRICE_SCALE);
    PyObject* v_sig = PyTuple_GET_ITEM(raw_tick, QuoteCQG::Q_VOL_SIGNIFICAND);
    PyObject* v_exp = PyTuple_GET_ITEM(raw_tick, QuoteCQG::Q_VOL_EXPONENT);
    
    if (!PyFloat_Check(ts) || !PyFloat_Check(px) || !PyFloat_Check(scl) || !PyFloat_Check(v_sig) || !PyFloat_Check(v_exp)) {return std::nullopt;}
    
    double timestamp = PyFloat_AS_DOUBLE(ts);
    double price = PyFloat_AS_DOUBLE(px) * PyFloat_AS_DOUBLE(scl);
    double volume = make_float(PyFloat_AS_DOUBLE(v_sig), PyFloat_AS_DOUBLE(v_exp), 0);
    
    return TradeTick{timestamp, price, volume};
}


std::optional<Tick> extract_raw_tick(const PyObject* raw_tick, DataExtractionPolicy policy) {    
    switch (policy) {
        case DataExtractionPolicy::ExtractTradeTickCQG:
            return extract_trade_tick_CQG(raw_tick);
        default:
            return std::nullopt;
    }
    
};

/*
  std::optional<TradeTick> extract_trade_tick_fast(PyObject* raw) {
      // bounds check first — GET_ITEM has no bounds checking
      if (PyTuple_GET_SIZE(raw) <= QuoteCQG::Q_CORRECT_PRICE_SCALE) return std::nullopt;

      PyObject* q_type = PyTuple_GET_ITEM(raw, QuoteCQG::Q_TYPE);
      if (!PyLong_Check(q_type)) return std::nullopt;
      if (PyLong_AsLong(q_type) != static_cast<int>(QuoteTypeCQG::Trade)) return
  std::nullopt;

      PyObject* ts  = PyTuple_GET_ITEM(raw, QuoteCQG::Q_UTC_TIME);
      PyObject* px  = PyTuple_GET_ITEM(raw, QuoteCQG::Q_SCALED_PRICE);
      PyObject* scl = PyTuple_GET_ITEM(raw, QuoteCQG::Q_CORRECT_PRICE_SCALE);
      PyObject* vsig = PyTuple_GET_ITEM(raw, QuoteCQG::Q_VOL_SIGNIFICAND);
      PyObject* vexp = PyTuple_GET_ITEM(raw, QuoteCQG::Q_VOL_EXPONENT);

      if (!PyFloat_Check(ts) || !PyFloat_Check(px) || !PyFloat_Check(scl)) return
  std::nullopt;

      double timestamp = PyFloat_AS_DOUBLE(ts);
      double price     = PyFloat_AS_DOUBLE(px) * PyFloat_AS_DOUBLE(scl);
      double volume    = make_float(PyFloat_AS_DOUBLE(vsig), PyFloat_AS_DOUBLE(vexp),
  0);

      return TradeTick{timestamp, price, volume, 0};
  }
*/