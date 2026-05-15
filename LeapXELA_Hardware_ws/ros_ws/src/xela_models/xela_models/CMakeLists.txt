cmake_minimum_required(VERSION 3.5)
project(xela_models)

find_package(ament_cmake REQUIRED)

install(DIRECTORY rviz
  DESTINATION share/${PROJECT_NAME})

install(DIRECTORY urdf
  DESTINATION share/${PROJECT_NAME})

install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME})

install(DIRECTORY mesh
  DESTINATION share/${PROJECT_NAME})

ament_package()