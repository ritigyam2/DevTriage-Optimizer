cmake_minimum_required(VERSION 3.10)
project(AutoTriage_DAA_Workspace LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Add Phase I and Phase II subprojects
add_subdirectory(Phase_I)
add_subdirectory(Phase_II)
