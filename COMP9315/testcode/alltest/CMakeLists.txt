cmake_minimum_required(VERSION 3.8)
project(alltest)

message("hi\n")
message(${alltest_SOURCE_DIR})
message(${PROJECT_BINARY_DIR})

set(CMAKE_C_STANDARD 99)

set(SOURCE_FILES x1.c)
add_executable(untitled ${SOURCE_FILES})
