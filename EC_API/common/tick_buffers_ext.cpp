#include <Python.h>
#include <deque>
#include <string>
#include <pybind11/pybind11.h>


/*Extraction -> tick -> buffers*/

void extract_raw_tick(PyObject* obj, std::string instruction) {
// Pick the right list first, then loop through it 
// only read the right indices, copy them to a Tick struct 
    if !PyList_Check(obj) {
        throw std::invalid_argument("Expected a list")
    }
};

struct TradeTick {double timestamp, price, volume};
struct Tick {double timestamp, price, volume};


class SlidingWindowBuffer {
    double _window; // time window
    std::deque<Tick> _ticks;
    double _sum_price = 0, sum_price = 0; 
    double _sum_pricevol = 0, _sum_vol = 0;
    int _n = 0;
    
public:
    SldingWindowBuffer() {}
    void add_tick() {
        extract_raw_tick
    
    };

};


class RingBuffer {

};

PYBIND11_MOFULE(tick_buffers_exy, m) {


}