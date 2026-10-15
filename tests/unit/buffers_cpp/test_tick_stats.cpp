#include <gtest/gtest.h>
#include <deque>
#include <stats.h>
#include <ticks.h>


//Happy Paths -- Deque init
//test OHLCV init 
TEST(OHLCVStat, InitSuccess) {
    std::deque<TradeTick> window;
    OHLCVStat<std::deque<TradeTick>> stat_obj(window, 0.01);

    OHLCVSnapshot snap = stat_obj.get_snapshot();
    EXPECT_DOUBLE_EQ(snap.open, 0.0);
    EXPECT_DOUBLE_EQ(snap.high, std::numeric_limits<double>::lowest());
    EXPECT_DOUBLE_EQ(snap.low, std::numeric_limits<double>::max());
    EXPECT_DOUBLE_EQ(snap.close, 0.0);
    EXPECT_EQ(snap.volume, 0);
}

//test OHLCV update
TEST(OHLCVStat, UpdateSucess) {
    //init
    std::deque<TradeTick> window;
    OHLCVStat<std::deque<TradeTick>> stat_obj(window, 0.01);
    
    //ingest data and update stat
    window.push_back({0.0,100.0,10});
    stat_obj.update(window.back());
    window.push_back({1.0,105.0,5});
    stat_obj.update(window.back());
    window.push_back({2.0,98.0,3});
    stat_obj.update(window.back());

    // tests
    OHLCVSnapshot snap = stat_obj.get_snapshot();
    EXPECT_DOUBLE_EQ(snap.open, 100.0);
    EXPECT_DOUBLE_EQ(snap.high, 105.0);
    EXPECT_DOUBLE_EQ(snap.low,98.0);
    EXPECT_DOUBLE_EQ(snap.close,98.0);
    EXPECT_EQ(snap.volume, 18);
}
//test OHLCV evict
TEST(OHLCVStat, EvictSuccess) {
    //init
    std::deque<TradeTick> window;
    OHLCVStat<std::deque<TradeTick>> stat_obj(window, 0.01);
    
    window.push_back({0.0,100.0,10});
    stat_obj.update(window.back());
    window.push_back({1.0,105.0,5});
    
    TradeTick evicted = window.front();
    window.pop_front();
    
    stat_obj.evict(evicted);
    stat_obj.update(window.back());
    
    OHLCVSnapshot snap = stat_obj.get_snapshot();
    EXPECT_DOUBLE_EQ(snap.open, 105.0);
    EXPECT_DOUBLE_EQ(snap.high, 105.0);
    EXPECT_DOUBLE_EQ(snap.low,105.0);
    EXPECT_DOUBLE_EQ(snap.close,105.0);
    EXPECT_EQ(snap.volume, 5);
}

//test MomentStat init 
TEST(MomentStat, InitSuccess) {
    std::deque<TradeTick> window;
    MomentStat<std::deque<TradeTick>> stat_obj(window);
    
    MomentSnapshot snap = stat_obj.get_snapshot();
    EXPECT_DOUBLE_EQ(snap.mean,0);
    EXPECT_DOUBLE_EQ(snap.variance,0);
    EXPECT_DOUBLE_EQ(snap.skewness,0);
    EXPECT_DOUBLE_EQ(snap.kurtosis,0);
}

//test MomentStat get_snapshots
TEST(MomentStat, GetSnapshotSuccess) {

}

//test MomentStat update
TEST(MomentStat, UpdateSuccess) {

}

//test MomentStat evict
TEST(MomentStat, EvictSuccess) {}


//test VWAPStat init 
//test VWAPStat get_snapshots
TEST(VWAPStat, InitSuccess) {
    std::deque<TradeTick> window;
    VWAPStat<std::deque<TradeTick>> stat_obj(window);
    
    VWAPSnapshot snap = stat_obj.get_snapshot();
    EXPECT_DOUBLE_EQ(snap.vwap,0);
}

//test VWAPStat update
TEST(VWAPStat, UpdateSuccess) {}

//test VWAPStat evict
TEST(VWAPStat, EvictSuccess) {}


//Sad Paths -- Deque init

