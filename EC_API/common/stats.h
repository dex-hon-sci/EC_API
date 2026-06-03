#pragma once 
#include <ticks.h>
#include <deque>
#include <array>

using Buffer = std::variant<std::deque<Tick>,std::array<Tick, 1024>>;

struct OHLCVSnapshot {
    double open, high, low, close;
    int volume;
};

struct VWAPSnapshot {};

struct GreeksSnapshot {};


//
enum class StatConfig: uint32_t {

};


class StatBase {
public:
    virtual void get_snapshot() {};
    virtual void update(const Tick t) {};
    virtual void evict(const Tick t) {};
};

//
class OHLCVStat : StateBase {
private:
    Buffer* buffer_;
    double tick_size;
    OHLCVSnapshot ohlcv_snapshot;
public:      
    OHLCVStat(Buffer& buf);
    void update(const Tick& t) override;
    void evict(const Tick& t) override;
    OHLCVSnapshot get_snapshot() const;
};
