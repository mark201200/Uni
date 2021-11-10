cmake_minimum_required(VERSION 3.7)
project(Testmq C)

set(CMAKE_C_STANDARD 99)


add_executable(main main.c)
add_executable(worker worker.c)
target_link_libraries(main rt)
target_link_libraries(worker rt)