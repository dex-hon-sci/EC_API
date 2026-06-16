#pragma once 
#include <cstdint>
#include <deque>
#include <array>
#include <ticks.h>


struct StatConfig {
    const bool cal_ohlcv = false;
    const bool cal_moment = false;
    const bool cal_vwap = false;
    const bool cal_median = false;
};

/* Snapshots collections */
struct OHLCVSnapshot {
    double open, high, low, close;
    int volume;
};


struct MomentSnapshot {
    double mean, variance, skewness, kurtosis;
};

struct VWAPSnapshot {
    double vwap;
};

struct MedianSnapshot {};

struct GreeksSnapshot {};



/* Concrete classes for Stat*/
class StatBase {
public:
    virtual void update(const TradeTick& t) {};
    virtual void evict(const TradeTick& t) {};
    virtual ~StatBase() {};
};

// OHLCV, update O(1), evict O(N) worst case
template <typename ContainerT>
class OHLCVStat : public StatBase {
private:
    ContainerT* container_;
    double tick_size_;
    OHLCVSnapshot ohlcv_snapshot;
public:      
    OHLCVStat(ContainerT& buf, double tick_size);
    void update(const TradeTick& t) override;
    void evict(const TradeTick& t) override;
    OHLCVSnapshot get_snapshot() const;
};

// 1st-4nd order moments normalised
template <typename ContainerT>
class MomentStat : public StatBase {
private:
    ContainerT* container_;
    double sum_p;
    double sum_p_2;
    double sum_p_3;
    double sum_p_4;
    int count;
    MomentSnapshot moment_snapshot;
public:
    MomentStat(ContainerT& buf);
    void update(const TradeTick& t) override;
    void evict(const TradeTick& t) override;
    MomentSnapshot get_snapshot() const;
};

// 
template <typename ContainerT>
class VWAPStat : public StatBase {
private:
    ContainerT* container_;
    double sum_pv;
    double sum_v;
    VWAPSnapshot vwap_snapshot;
public:
    VWAPStat(ContainerT& buf);
    void update(const TradeTick& t) override;
    void evict(const TradeTick& t) override;
    VWAPSnapshot get_snapshot() const;
};


class MedianStat : public StatBase {};

