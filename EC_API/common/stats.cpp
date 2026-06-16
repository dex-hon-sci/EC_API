#include <stats.h>
#include <ticks.h>
#include <algorithm>
#include <cmath>


// OHLCVStat: O(1) for update, O(N) at worst in evict
template <typename ContainerT>
OHLCVStat<ContainerT>::OHLCVStat(ContainerT& container, double tick_size):
        container_{&container},
        tick_size_{tick_size},
        ohlcv_snapshot{} {}
        
template <typename ContainerT>
void OHLCVStat<ContainerT>::update(const TradeTick& t) {
    if (t.price >= ohlcv_snapshot.high) {ohlcv_snapshot.high = t.price;}
    else if (t.price <= ohlcv_snapshot.low) {ohlcv_snapshot.low = t.price;}
    
    ohlcv_snapshot.open = container_->front().price;
    ohlcv_snapshot.close = container_->back().price;
    ohlcv_snapshot.volume += t.volume;
}

template <typename ContainerT>
void OHLCVStat<ContainerT>::evict(const TradeTick& t) {
    if (std::abs(t.price - ohlcv_snapshot.high) <= 0.5*tick_size_) { 
        auto it = std::max_element(container_->begin(), container_->end(), [](const TradeTick& a, const TradeTick& b) {return a.price < b.price;}); 
        ohlcv_snapshot.high = it->price;
        }
    else if (std::abs(t.price - ohlcv_snapshot.low) <= 0.5*tick_size_) {
        auto it = std::min_element(container_->begin(), container_->end(),[](const TradeTick& a, const TradeTick& b) {return a.price < b.price;});
        ohlcv_snapshot.low = it->price;
        }

    ohlcv_snapshot.volume -= t.volume;
}

template <typename ContainerT>
OHLCVSnapshot OHLCVStat<ContainerT>::get_snapshot() const {return ohlcv_snapshot;}


// MomentStat: O(1) on both update and evict
template <typename ContainerT>
MomentStat<ContainerT>::MomentStat(ContainerT& container):
    container_{&container}, 
    sum_p{}, sum_p_2{}, sum_p_3{}, sum_p_4{}, 
    count{}, 
    moment_snapshot{} {
      for (const TradeTick& t : *container_)
          update(t);
    }
    
template <typename ContainerT>   
void MomentStat<ContainerT>::update(const TradeTick& t) {
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
}

template <typename ContainerT>
void MomentStat<ContainerT>::evict(const TradeTick& t) {
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
}

template <typename ContainerT>
MomentSnapshot MomentStat<ContainerT>::get_snapshot() const {return moment_snapshot;}

// VWAPStat O(1) on both update and evict
template <typename ContainerT>
VWAPStat<ContainerT>::VWAPStat(ContainerT& container): 
    container_{&container},
    sum_pv{}, 
    sum_v{},
    vwap_snapshot{} {
     for (const TradeTick& t : *container_)
         update(t);
    }
    
template <typename ContainerT>
void VWAPStat<ContainerT>::update(const TradeTick& t) {
  sum_pv += t.price * t.volume;
  sum_v  += t.volume;
  vwap_snapshot.vwap = sum_pv / sum_v;
}

template <typename ContainerT>
void VWAPStat<ContainerT>::evict(const TradeTick& t) {
  sum_pv -= t.price * t.volume;
  sum_v  -= t.volume;         
  vwap_snapshot.vwap = sum_pv / sum_v;
}

template <typename ContainerT>
VWAPSnapshot VWAPStat<ContainerT>::get_snapshot() const {return vwap_snapshot;}


