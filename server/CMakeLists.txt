cmake_minimum_required(VERSION 3.14)
project(headball C)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)

find_package(Threads REQUIRED)

include_directories(
    ${CMAKE_SOURCE_DIR}/inc
    ${CMAKE_SOURCE_DIR}/src 
)

add_library(server_lib 
    src/server.c 
    inc/server.h
)

add_executable(server main.c)

target_link_libraries(server PRIVATE 
    server_lib
    pthread 
    Threads::Threads
)
