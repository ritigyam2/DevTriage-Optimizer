cmake_minimum_required(VERSION 3.10)
project(AutoTriage_DAA_Phase_I CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include_directories(include)

add_executable(main src/main.cpp)
add_executable(test_runner tests/test_runner.cpp)
