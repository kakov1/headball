add_library(server server.c)

target_include_directories(server PUBLIC ${CMAKE_SOURCE_DIR}/inc)