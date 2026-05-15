// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from xela_server_ros2:msg/SensorFull.idl
// generated code does not contain a copyright notice

#ifndef XELA_SERVER_ROS2__MSG__DETAIL__SENSOR_FULL__STRUCT_H_
#define XELA_SERVER_ROS2__MSG__DETAIL__SENSOR_FULL__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'model'
#include "rosidl_runtime_c/string.h"
// Member 'taxels'
#include "xela_server_ros2/msg/detail/taxel__struct.h"
// Member 'forces'
#include "xela_server_ros2/msg/detail/forces__struct.h"

/// Struct defined in msg/SensorFull in the package xela_server_ros2.
typedef struct xela_server_ros2__msg__SensorFull
{
  uint32_t message;
  double time;
  rosidl_runtime_c__String model;
  uint8_t sensor_pos;
  xela_server_ros2__msg__Taxel__Sequence taxels;
  xela_server_ros2__msg__Forces__Sequence forces;
} xela_server_ros2__msg__SensorFull;

// Struct for a sequence of xela_server_ros2__msg__SensorFull.
typedef struct xela_server_ros2__msg__SensorFull__Sequence
{
  xela_server_ros2__msg__SensorFull * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} xela_server_ros2__msg__SensorFull__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // XELA_SERVER_ROS2__MSG__DETAIL__SENSOR_FULL__STRUCT_H_
