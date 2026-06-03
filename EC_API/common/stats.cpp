#include <stats.h>
#include <ticks.h>
#include <algorithm>
#include <cmath>


// O(1) for update, O(N) at worst in evict
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
    
    OHLCVSnapshot get_snapshot() const {return ohlcv_snapshot;};

};

// O(1) on both update and evict
class MomentStat : public StateBase {
private:
    Buffer* buffer_;
    double sum_p;
    double sum_p_2;
    double sum_p_3;
    double sum_p_4;
    int count;
    MomentSnapshot moment_snapshot;

public:
    MomentStat(Buffer& buf):
        buffer_{&buf}, 
        sum_p{}, sum_p_2{}, sum_p_3{}, sum_p_4{}, 
        count{}, 
        moment_snapshot{} {
          for (const Tick& t : *buffer_)
              update(t);
        };
    
    void update(const Tick& t) {
        double p = t.price;
        sum_p += p;
        sum_p_2 += std::pow(p,2);
        sum_p_3 += std::pow(p,3);
        sum_p_4 += std::pow(p,4);
        count++;
        
        double mean_ = sum_p / count;
        double variance_ = (sum_p_2/count) - std::pow(mean_, 2); 
        
        moment_snapshot.mean = mean_;
        moment_snapshot.variance = variance_;
        moment_snapshot.skewness = (((sum_p_3/count) - 3*mean_*(sum_p_2 / count) + 2* std::pow(mean_, 3)) / pow(variance_, 1.5)); 
        moment_snapshot.kurtosis = (((sum_p_4 -4 * mean_ * sum_p_3 + 6 * sum_p_2 * std::pow(mean_,2))/count) - 3* std::pow(mean_,4)) /  pow(variance_, 2);
    };
    void evict(const Tick& t) {
        double p = t.price;
        sum_p -= p;
        sum_p_2 -= std::pow(p, 2);
        sum_p_3 -= std::pow(p, 3);
        sum_p_4 -= std::pow(p, 4);
        count--;
                
        double mean_ = sum_p / count;
        double variance_ = (sum_p_2/count) - std::pow(mean_, 2); 
        
        moment_snapshot.mean = mean_;
        moment_snapshot.variance = variance_;
        moment_snapshot.skewness = (((sum_p_3/count) - 3*mean_*(sum_p_2 / count) + 2* std::pow(mean_, 3)) / pow(variance_, 1.5)); 
        moment_snapshot.kurtosis = (((sum_p_4 -4 * mean_ * sum_p_3 + 6 * sum_p_2 * std::pow(mean_,2))/count) - 3* std::pow(mean_,4)) /  pow(variance_, 2);
    };
    
    MomentSnapshot get_snapshot() const {return moment_snapshot;};
};


class VWAPStat : public StateBase {
private:
    //Buffer* buffer_;
    double sum_pv;
    double sum_v;
    VWAPSnapshot vwap_snapshot;
public:
    VWAPStat(Buffer& buf): 
        buffer_{&buf},
        sum_pv{}, 
        sum_v{},
        vwap_snapshot{} {
         for (const Tick& t : *buffer_)
             update(t);
        };

    void update(const Tick& t) {
      sum_pv += t.price * t.volume;
      sum_v  += t.volume;
      vwap_snapshot.vwap = sum_pv / sum_v;
    };

    void evict(const Tick& t) {
      sum_pv -= t.price * t.volume;
      sum_v  -= t.volume;         
      vwap_snapshot.vwap = sum_pv / sum_v;
    };
    
    VWAPSnapshot get_snapshot() const {return vwap_snapshot;}

};

class MedianStat : public StateBase {
private:
    Buffer* buffer_;
    MedianSnapshot vwap_snapshot;
    
public:

};



//VWAPStat
//OHLCV