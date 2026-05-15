cmake_minimum_required(VERSION 3.5)
project(leap_hand)

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclpy REQUIRED)
find_package(std_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)

################################################
## Declare ROS messages, services and actions ##
################################################

## Generate services in the 'srv' folder
rosidl_generate_interfaces(${PROJECT_NAME}
  "srv/LeapVelocity.srv"
  "srv/LeapPosition.srv"
  "srv/LeapEffort.srv"
  "srv/LeapState.srv"
  DEPENDENCIES std_msgs
)

###################################
## ament specific configuration  ##
###################################
ament_package()

#############
## Install ##
#############

# Install Python scripts
install(PROGRAMS
  scripts/leaphand_node.py
  scripts/ros2_example.py
  scripts/keyboard_node.py
  DESTINATION lib/${PROJECT_NAME}
)

# Install Python modules used by scripts in-place
install(FILES
  scripts/base.py
  DESTINATION lib/${PROJECT_NAME}
)

# Install non-code assets (config)
install(FILES
  scripts/pose.json
  DESTINATION share/${PROJECT_NAME}/config
)

# Install Python helper modules (importable by scripts)
install(DIRECTORY scripts/leap_hand_utils
  DESTINATION lib/${PROJECT_NAME}
)

# Install launch files
install(DIRECTORY launch/
  DESTINATION share/${PROJECT_NAME}/launch
)

#############
## Testing ##
#############

## Add gtest based cpp test target and link libraries
# find_package(ament_cmake_gtest REQUIRED)
# ament_add_gtest(${PROJECT_NAME}-test test/test_leap_hand.cpp)
# if(TARGET ${PROJECT_NAME}-test)
#   target_link_libraries(${PROJECT_NAME}-test ${PROJECT_NAME})
# endif()
