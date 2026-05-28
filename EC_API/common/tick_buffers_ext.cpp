#include <deque>
#include <string>
#include <array>
#include <Python.h>
#include <pybind11/pybind11.h>
#include "ticks.h"
#include "data_fields_cqg.h"
#include "data_extractors_cqg.h"

/*Extraction -> tick -> buffers*/
class SlidingWindowBuffer {
private:
    DataExtractionPolicy policy_;
    int rtmd_idx;

    std::deque<Tick> buffer_;
    
    double window_; // time window
    double sum_price_ = 0;
    double sum_pricevol_ = 0, sum_vol_ = 0;
    int n_ = 0;
    double vwap = 0;
    
public:
    /* 0. Constructor*/
    SlidingWindowBuffer(DataExtractionPolicy policy): 
        policy_{policy},
        rtmd_idx{get_parsed_rtmd_index_from_policy(policy)} {}

    void compute_and_update(Tick tick) {//accumulator calcultator
    
    }
    
    void add_tick(py::tuple& parsed_rtmd) {
        py::list data = parsed_rtmd[rtmd_idx];
        for (auto& raw : data) {
            auto tick = extract_raw_tick(raw.cast<py::tuple>(), policy_);
            if (tick) buffer_.push_back(*tick); //send them to the buffer
            compute_and_update(*tick); //update private attributes
            }
    }

};


class RingBuffer {
private:
    DataExtractionPolicy policy_;
    int rtmd_idx;

    std::array<Tick, 1024> buffer_;  // fixed size, no heap management needed
    int head_ = 0;
     
    double sum_price_ = 0;
    double sum_pricevol_ = 0, sum_vol_ = 0;
    int n_ = 0;

public:
    void compute_and_update() {}
    void add_tick() {}

};

PYBIND11_MODULE(tick_buffers_ext, m) {
    m.class_<SlidingWindowBuffer>(m, "SlidingWindowBuffer");
}