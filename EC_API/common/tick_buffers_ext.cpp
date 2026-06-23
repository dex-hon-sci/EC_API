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

class SlidingWindowBuffer {
private:
    // Buffer setups
    DataExtractionPolicy policy_;
    int rtmd_idx; // The index of interest in rtmd tuple, initialised by policy_
    double window_; // time window. (micro-seconds)
    std::deque<TradeTick> tick_container_; // Tick Data Container
    std::vector<TradeTick> scratch_tick_container_; // temporary eviction room 
        
    // Stats
    StatConfig stat_config_; // A list of bools, input via Python
    std::array<StatBase*, static_cast<int>(StatType::COUNT_)> stats_; // StatBase Child objects all stat
    std::vector<std::unique_ptr<StatBase>> active_stats_; // Active Stats only
public:
    /* 0. Constructor*/
    SlidingWindowBuffer(
        DataExtractionPolicy policy, 
        double window, 
        double tick_size, 
        StatConfig stat_config = {}
        ): 
        
        policy_{policy},
        rtmd_idx{get_parsed_rtmd_index_from_policy(policy)},
        window_{window},
        stat_config_{stat_config} {
            init_stats(  
                stat_config_, 
                tick_container_,
                stats_, 
                active_stats_,
                tick_size
                );
        }

    void compute_and_update(const TradeTick& tick) {//accumulator calcultator
        // Evict stat data given old ticks in the scratch buffer
        while (!scratch_tick_container_.empty()) {
            auto ev = scratch_tick_container_.back();
            scratch_tick_container_.pop_back();
            for (auto& sts : stats_) { // evict for all stat objects
                sts->evict(ev);
            }
        }         
        for (auto& sts : stats_) {// update for all stat objects
            sts->update(tick);
            }; 
    }
    
    void add_tick(const TradeTick& tick) {
        tick_container_.push_back(tick);
        }

    void evict_tick(const double threshold) { // loop throigh the front of the container
        while (!tick_container_.empty() && tick_container_.front().timestamp < threshold) {
            TradeTick evicted_tick = tick_container_.front();
            tick_container_.pop_front();
            scratch_tick_container_.push_back(evicted_tick);
            };
        }   
    
    void on_tick(const py::object& parsed_rtmd) {
        if (!PyTuple_Check(parsed_rtmd.ptr())) return;
        
        const PyObject* data = PyTuple_GET_ITEM(parsed_rtmd.ptr(), rtmd_idx);

        if (!PyList_Check(data)) return;
        Py_ssize_t n = PyList_GET_SIZE(data);
        for (Py_ssize_t i = 0; i < n; i++) {
            PyObject* raw_data_ptr = PyList_GET_ITEM(data, i);
            if (!PyTuple_Check(raw_data_ptr)) continue;  //
            
            auto tick = extract_raw_tick(raw_data_ptr, policy_);
            
            if (tick) {
                double threshold_ = tick->timestamp - window_;
                
                add_tick(*tick);
                evict_tick(threshold_);
                compute_and_update(*tick);
                }
            }
    }
    
    py::object get_stat_snapshot(const StatType& stat_name) const {
        if (stat_name == StatType::OHLCV) {
            py::tuple tu(5);
            // ... to be continued     
            return tu;

        }
    }
};


class RingBuffer {
private:
    // Buffer Setups
    DataExtractionPolicy policy_;
    int rtmd_idx;
    std::array<TradeTick, 1024> tick_container_;  // fixed size, no heap management needed
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
    void evict_tick() {}
    void on_tick() {}

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
        .def(py::init<DataExtractionPolicy, double, double, StatConfig>())
        .def("on_tick", &SlidingWindowBuffer::on_tick);
        
    py::class_<RingBuffer>(m, "RingBuffer")
        .def(py::init<DataExtractionPolicy>())
        .def("on_tick", &RingBuffer::on_tick);
}