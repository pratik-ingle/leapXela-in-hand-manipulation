// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from xela_server_ros2:msg/Forces.idl
// generated code does not contain a copyright notice

#ifndef XELA_SERVER_ROS2__MSG__DETAIL__FORCES__STRUCT_H_
#define XELA_SERVER_ROS2__MSG__DETAIL__FORCES__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/Forces in the package xela_server_ros2.
typedef struct xela_server_ros2__msg__Forces
{
  float x;
  float y;
  float z;
} xela_server_ros2__msg__Forces;

// Struct for a sequence of xela_server_ros2__msg__Forces.
typedef struct xela_server_ros2__msg__Forces__Sequence
{
  xela_server_ros2__msg__Forces * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} xela_server_ros2__msg__Forces__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // XELA_SERVER_ROS2__MSG__DETAIL__FORCES__STRUCT_H_
