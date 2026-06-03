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
    DataExtractionPolicy policy_;
    int rtmd_idx;
    std::deque<TradeTick> buffer_;
    
    double window_; // time window
    std::vector<StatBase*> stats_;

    
public:
    /* 0. Constructor*/
    SlidingWindowBuffer(DataExtractionPolicy policy, double window): 
        policy_{policy},
        rtmd_idx{get_parsed_rtmd_index_from_policy(policy)},
        window_{window} {}

    void compute_and_update(const TradeTick& tick) {//accumulator calcultator
        if (buffer_.size() > window_) {
            TradeTick evicted_tick = buffer_.front();
            buffer_.pop_front();
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
                buffer_.push_back(*tick); //send them to the buffer
                compute_and_update(*tick); //update private attributes
                
                } 
            }
    }
};


class RingBuffer {
private:
    DataExtractionPolicy policy_;
    int rtmd_idx;

    std::array<TradeTick, 1024> buffer_;  // fixed size, no heap management needed
    int head_ = 0;
     
public:
    RingBuffer(DataExtractionPolicy policy):
        policy_{policy},
        rtmd_idx{get_parsed_rtmd_index_from_policy(policy)} {}

    void compute_and_update() {}
    void add_tick() {}

};

PYBIND11_MODULE(tick_buffers_ext, m) {
    py::enum_<DataExtractionPolicy>(m, "DataExtractionPolicy")
        .value("ExtractTradeTickCQG", DataExtractionPolicy::ExtractTradeTickCQG);

    py::class_<SlidingWindowBuffer>(m, "SlidingWindowBuffer")
        .def(py::init<DataExtractionPolicy, double>())
        .def("add_tick", &SlidingWindowBuffer::add_tick);
        
    py::class_<RingBuffer>(m, "RingBuffer")
        .def(py::init<DataExtractionPolicy>())
        .def("add_tick", &RingBuffer::add_tick);
}