#include <Python.h>
#include <deque>
#include <string>
#include <pybind11/pybind11.h>
#include <data_fields_cqg.h>
#include <data_extractors_cqg.h>

/*Extraction -> tick -> buffers*/
struct TradeTick {double timestamp, price, volume};
struct Tick {double timestamp, price, volume};

Tick extract_raw_tick(py::tuple* obj, std::string instruction) {
// Pick the right list first, then loop through it 
// only read the right indices, copy them to a Tick struct 
    if !PyList_Check(obj) {
        throw std::invalid_argument("Expected a list")
    }
    if instruction == NULL {
        std::string instruction = "policy_1";
    }
    
    if instruction == "policy_1" {
        Tick extracted_tick = Tick{obj[0],obj[1],obj[2]};
    }
    else if instruction == "policy_2" {
        Tick extracted_tick = Tick{obj[4],obj[5],obj[6]};
    }
    else if instruction == "policy_2" {
        Tick extracted_tick = Tick{obj[4],obj[5],obj[6]};
    
    return extracted_tick
};



class SlidingWindowBuffer {
private:
    double _window; // time window
    std::deque<Tick> _ticks;
    double _sum_price = 0, sum_price = 0; 
    double _sum_pricevol = 0, _sum_vol = 0;
    int _n = 0;
    
public:
    /* 0. Constructor*/
    SlidingWindowBuffer() {}
    
    void add_tick(PyObject* obj) {
        extract_raw_tick();

    /* 1. Copy Constructor*/
    //SlidingWindowBuffer(const SldingWindowBuffer& other) {}
    /* 2. Copy Assignment*/
    //SlidingWindowBuffer& operator=(const SldingWindowBuffer& other) {}
    /* 3. Move Constructor*/
    //SlidingWindowBuffer(SlidingWindowBuffer&& other) : {}
    /* 4. Move Assignment*/
    //SlidingWindowBuffer& operator=(SldingWindowBuffer&& other) {}
    /* 5. Destructor*/
    //~SldingWindowBuffer() {}

    
    };

};


class RingBuffer {
private:
    double _sum_price = 0, sum_price = 0; 
    double _sum_pricevol = 0, _sum_vol = 0;
    int _n = 0;

public:
    /* 1. Copy Constructor*/
    //RingBuffer(const RingBuffer& other) {}
    /* 2. Copy Assignment*/
    //RingBuffer& operator=(const RingBuffer& other) {}
    /* 3. Move Constructor*/
    //RingBuffer(RingBuffer&& other) : {}
    /* 4. Move Assignment*/
    //RingBuffer& operator=(RingBuffer&& other) {}
    /* 5. Destructor*/
    //~RingBuffer() {}

};

PYBIND11_MOFULE(tick_buffers_exy, m, py::mod_gil_not_used()) {

    m.class_("SlidingWindowBuffer", &SlidingWindowBuffer)
}