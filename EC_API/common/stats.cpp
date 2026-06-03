#include <stats.h>
#include <ticks.h>
#include <algorithm>

class OHLCVStat : public StateBase {
private:
    Buffer* buffer_;
    double tick_size_;
    OHLCVSnapshot ohlcv_snapshot;
public:      
    OHLCVStat(Buffer& buf, double tick_size): 
        buffer_{&buf},
        tick_size_{tick_size},
        ohlcv_snapshot{} {};
    OHLCVSnapshot get_snapshot() {
        return ohlcv_snapshot;
    };

    void update(const Tick& t) {
        if (t.price >= ohlcv_snapshot.high) {ohlcv_snapshot.high = t.price};
        else if (t.price <= ohlcv_snapshot.low) {ohlcv_snapshot.low = t.price};
        
        ohlcv_snapshot.open = buffer_->front().price;
        ohlcv_snapshot.close = buffer_->back().price;
        ohlcv_snapshot.volume += t.volume;
    };
    
    void evict(const Tick& t) {
        if (std::abs(t.price - ohlcv_snapshot.high) <= 0.5*tick_size_) { 
            auto it = std::max_element(buffer_->begin(), buffer_->end(), [](const Tick& a, const Tick& b) {return a.price < b.price;}); 
            ohlcv_snapshot.high = it->price;
            };
        else if (std::abs(t.price - ohlcv_snapshot.low) <= 0.5*tick_size_) {
            auto it = std::min_element(buffer_->begin(), buffer_->end(),[](const Tick& a, const Tick& b) {return a.price < b.price;});
            ohlcv_snapshot.low = it->price;
            };
    
        ohlcv_snapshot.volume -= t.volume;
    };
};

class VWAPStat : public StateBase {

};

class FirstSecondOrderStat : StateBase {
private:
        Buffer* buffer_;

public:
    void get_snapshot(const Tick t) {};
    void update(const Tick t) {};
    void evict(const Tick t) {};

};
//VWAPStat
//OHLCV