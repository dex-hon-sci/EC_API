#include <gtest/gtest.h>
#include <deque>
#include <stats.h>
#include <ticks.h>

//test OHLCV init 
TEST(OHLCVStat, InitSuccess) {}

//test OHLCV get_snapshots

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
    OHLCVStat<std::deque<TradeTick>> StatObj(window, 0.01);

}


//test MomentStat init 

//test MomentStat update

//test MomentStat evict

//test MomentStat get_snapshots

//test MomentStat to_py_tuple