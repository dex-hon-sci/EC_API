cmake_minimum_required(VERSION 3.15)
project(EC_API_cpp_tests LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

execute_process(
    COMMAND python -m pybind11 --cmakedir
    OUTPUT_VARIABLE pybind11_CMAKE_DIR
    OUTPUT_STRIP_TRAILING_WHITESPACE
)
list(APPEND CMAKE_PREFIX_PATH ${pybind11_CMAKE_DIR})

find_package(GTest REQUIRED)      
find_package(pybind11 REQUIRED) 

add_executable(test_tick_stats
    tests/unit/buffers_cpp/test_tick_stats.cpp
)
target_include_directories(test_tick_stats PRIVATE EC_API/common)
target_link_libraries(test_tick_stats PRIVATE
    GTest::gtest_main
    pybind11::embed
)

enable_testing()
include(GoogleTest)
gtest_discover_tests(test_tick_stats)
