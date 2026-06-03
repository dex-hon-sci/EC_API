#pragma once 
#include <ticks.h>
#include <deque>
#include <array>

using Buffer = std::variant<std::deque<Tick>,std::array<Tick, 1024>>;

/* Snapshots collections */
struct OHLCVSnapshot {
    double open, high, low, close;
    int volume;
};


struct MomentSnapshot {
    double mean, variance, skewness, kurtosis
}

struct VWAPSnapshot {};

struct MedianSnapshot {};

struct GreeksSnapshot {};


//
enum class StatConfig: uint32_t {

};

/* Concrete classes for Stat*/
class StatBase {
public:
    virtual void update(const Tick t) {};
    virtual void evict(const Tick t) {};
    virtual void get_snapshot() {};
};

// OHLCV, update O(1), evict O(N) worst case
class OHLCVStat : public StateBase {
private:
    Buffer* buffer_;
    double tick_size;
    OHLCVSnapshot ohlcv_snapshot;
public:      
    OHLCVStat(Buffer& buf, double tick_size);
    void update(const Tick& t) override;
    void evict(const Tick& t) override;
    OHLCVSnapshot get_snapshot() const;
};

// 1st-4nd order moments normalised
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
    MomentStat(Buffer& buf);
    void update(const Tick& t) override;
    void evict(const Tick& t) override;
    MomentSnapshot get_snapshot() const;
};

class MedianStat : public StateBase {};

class VWAPStat : public StateBase {};
