#include <deque>
#include <pybind11/pybind11.h>


/*Extraction -> tick -> buffers*/

void extract_raw_tick() {};

struct TradeTick {double timestamp, price, volume};


class SlidingWindowBuffer {
    int _n = 0;
public:
    void add_raw_tick() {};
    void add_tick() {};

};


class RingBuffer {

};

PYBIND11_MOFULE(tick_buffers_exy, m) {


}