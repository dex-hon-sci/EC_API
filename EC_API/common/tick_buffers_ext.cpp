#include <deque>
#include <string>
#include <array>
#include <vector>
#include <Python.h>
#include <pybind11/pybind11.h>
#include "ticks.h"
#include "stats.h"
#include "data_fields_cqg.h"
#include "data_extractors_cqg.h"
namespace py = pybind11;

/*Extraction -> tick -> buffers*/
class SlidingWindowBuffer {
private:
    // Buffer setups
    DataExtractionPolicy policy_;
    int rtmd_idx; // The index of interest in rtmd tuple, initialised by policy_
    double window_; // time window. eviction condition
    std::deque<TradeTick> container_; // Data Container
    
    //Stats
    StatConfig stat_config_; // A list of bools, input via Python
    std::vector<StatBase*> stats_; // StatBase Child objects

public:
    /* 0. Constructor*/
    SlidingWindowBuffer(DataExtractionPolicy policy, double window, StatConfig stat_config = {}): 
        policy_{policy},
        rtmd_idx{get_parsed_rtmd_index_from_policy(policy)},
        window_{window},
        stat_config_{stat_config} {}

    void compute_and_update(const TradeTick& tick) {//accumulator calcultator
        if (container_.size() > window_) {
            TradeTick evicted_tick = container_.front();
            container_.pop_front();
            for (auto& sts : stats_) {
                sts->evict(evicted_tick);
            };
        for (auto& sts : stats_) {
            sts->update(tick);
            };
        }
    }
    
    void add_tick(const py::object& parsed_rtmd) {
        if (!PyTuple_Check(parsed_rtmd.ptr())) return;
        
        const PyObject* data = PyTuple_GET_ITEM(parsed_rtmd.ptr(), rtmd_idx);

        if (!PyList_Check(data)) return;
        Py_ssize_t n = PyList_GET_SIZE(data);
        
        for (Py_ssize_t i = 0; i < n; i++) {
            PyObject* raw_data_ptr = PyList_GET_ITEM(data, i);
            if (!PyTuple_Check(raw_data_ptr)) continue;  //
            
            auto tick = extract_raw_tick(raw_data_ptr, policy_);
            if (tick) {
                container_.push_back(*tick); //send them to the buffer
                compute_and_update(*tick); //update private attributes
                
                } 
            }
    }
    
    py::object get_stat_snapshot(const std::string& stat_name) const {
    py::tuple tu(5);
    return tu;}
};


class RingBuffer {
private:
    // Buffer Setups
    DataExtractionPolicy policy_;
    int rtmd_idx;
    std::array<TradeTick, 1024> container_;  // fixed size, no heap management needed
    int head_ = 0;
    
    // Stats
    StatConfig stat_config; 
    std::vector<StatBase*> stats_;

public:
    RingBuffer(DataExtractionPolicy policy):
        policy_{policy},
        rtmd_idx{get_parsed_rtmd_index_from_policy(policy)} {}

    void compute_and_update() {}
    void add_tick() {}

};

PYBIND11_MODULE(tick_buffers_ext, m) {
    py::enum_<StatType>(m, "StatType")
        .value("OHLCV", StatType::OHLCV)
        .value("VWAP", StatType::VWAP)
        .value("MOMENT", StatType::MOMENT)
        .value("MEDIAN", StatType::MEDIAN);

    py::enum_<DataExtractionPolicy>(m, "DataExtractionPolicy")
        .value("ExtractTradeTickCQG", DataExtractionPolicy::ExtractTradeTickCQG);
        
    py::class_<StatConfig>(m, "StatConfig")
        .def(py::init([](bool cal_ohlcv, bool cal_moment, bool cal_vwap, bool cal_median) {
                 return StatConfig{cal_ohlcv, cal_moment, cal_vwap, cal_median};
             }),
             py::arg("cal_ohlcv")  = false,
             py::arg("cal_moment") = false,
             py::arg("cal_vwap")   = false,
             py::arg("cal_median") = false);
           
    py::class_<SlidingWindowBuffer>(m, "SlidingWindowBuffer")
        .def(py::init<DataExtractionPolicy, double>())
        .def("add_tick", &SlidingWindowBuffer::add_tick);
        
    py::class_<RingBuffer>(m, "RingBuffer")
        .def(py::init<DataExtractionPolicy>())
        .def("add_tick", &RingBuffer::add_tick);
}