# Offline GNU Makefile for Phase I (C++17)
CXX = C:/MinGW/bin/g++.exe
CXXFLAGS = -std=c++17 -O3 -Wall -Wextra -Iinclude

all: main.exe test_runner.exe

main.exe: src/main.cpp include/*.hpp
	$(CXX) $(CXXFLAGS) src/main.cpp -o main.exe

test_runner.exe: tests/test_runner.cpp include/*.hpp
	$(CXX) $(CXXFLAGS) tests/test_runner.cpp -o test_runner.exe

test: test_runner.exe
	./test_runner.exe

clean:
	del /Q main.exe test_runner.exe 2>NUL
