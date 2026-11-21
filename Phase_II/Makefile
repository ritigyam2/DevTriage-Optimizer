# Offline GNU Makefile for Phase II (C++17)
CXX = C:/MinGW/bin/g++.exe
CXXFLAGS = -std=c++17 -O3 -Wall -Wextra -Iinclude

all: main.exe scenario_benchmarks.exe test_chunk2_dnc.exe test_chunk3_greedy.exe test_chunk4_dp.exe test_chunk5_backtracking_bb.exe test_chunk6_flow_strings_crt.exe

main.exe: src/main.cpp include/core/*.hpp include/algorithms/*/*.hpp
	$(CXX) $(CXXFLAGS) src/main.cpp -o main.exe

scenario_benchmarks.exe: src/scenario_benchmarks.cpp include/core/*.hpp include/algorithms/*/*.hpp
	$(CXX) $(CXXFLAGS) src/scenario_benchmarks.cpp -o scenario_benchmarks.exe

test_chunk2_dnc.exe: tests/test_chunk2_dnc.cpp include/algorithms/divide_and_conquer/*.hpp
	$(CXX) $(CXXFLAGS) tests/test_chunk2_dnc.cpp -o test_chunk2_dnc.exe

test_chunk3_greedy.exe: tests/test_chunk3_greedy.cpp include/algorithms/greedy/*.hpp
	$(CXX) $(CXXFLAGS) tests/test_chunk3_greedy.cpp -o test_chunk3_greedy.exe

test_chunk4_dp.exe: tests/test_chunk4_dp.cpp include/algorithms/dynamic_programming/*.hpp
	$(CXX) $(CXXFLAGS) tests/test_chunk4_dp.cpp -o test_chunk4_dp.exe

test_chunk5_backtracking_bb.exe: tests/test_chunk5_backtracking_bb.cpp include/algorithms/backtracking_bb/*.hpp
	$(CXX) $(CXXFLAGS) tests/test_chunk5_backtracking_bb.cpp -o test_chunk5_backtracking_bb.exe

test_chunk6_flow_strings_crt.exe: tests/test_chunk6_flow_strings_crt.cpp include/algorithms/flow_matching/*.hpp include/algorithms/number_theory/*.hpp include/algorithms/string_matching/*.hpp include/core/*.hpp
	$(CXX) $(CXXFLAGS) tests/test_chunk6_flow_strings_crt.cpp -o test_chunk6_flow_strings_crt.exe

test: all
	./scenario_benchmarks.exe
	./test_chunk2_dnc.exe
	./test_chunk3_greedy.exe
	./test_chunk4_dp.exe
	./test_chunk5_backtracking_bb.exe
	./test_chunk6_flow_strings_crt.exe

clean:
	del /Q main.exe scenario_benchmarks.exe test_chunk2_dnc.exe test_chunk3_greedy.exe test_chunk4_dp.exe test_chunk5_backtracking_bb.exe test_chunk6_flow_strings_crt.exe 2>NUL
