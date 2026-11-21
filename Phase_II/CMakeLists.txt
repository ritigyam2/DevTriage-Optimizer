cmake_minimum_required(VERSION 3.10)
project(AutoTriage_DAA_Phase_II CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include_directories(include)

add_executable(main src/main.cpp)
add_executable(scenario_benchmarks src/scenario_benchmarks.cpp)
add_executable(test_chunk2_dnc tests/test_chunk2_dnc.cpp)
add_executable(test_chunk3_greedy tests/test_chunk3_greedy.cpp)
add_executable(test_chunk4_dp tests/test_chunk4_dp.cpp)
add_executable(test_chunk5_backtracking_bb tests/test_chunk5_backtracking_bb.cpp)
add_executable(test_chunk6_flow_strings_crt tests/test_chunk6_flow_strings_crt.cpp)
