cmake_minimum_required(VERSION 3.16)

project(mujoco_c_example LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# MuJoCo installs a CMake package config (e.g. /usr/local/lib/cmake/mujoco).
find_package(mujoco CONFIG REQUIRED)
find_package(glfw3 REQUIRED)
find_package(OpenGL REQUIRED)

add_executable(load_model load_model.cc)
target_link_libraries(load_model PRIVATE mujoco::mujoco glfw OpenGL::GL)

add_executable(load_only load_only.cc)
target_link_libraries(load_only PRIVATE mujoco::mujoco)

