// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from xela_server_ros2:msg/Taxel.idl
// generated code does not contain a copyright notice

#ifndef XELA_SERVER_ROS2__MSG__DETAIL__TAXEL__STRUCT_H_
#define XELA_SERVER_ROS2__MSG__DETAIL__TAXEL__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/Taxel in the package xela_server_ros2.
typedef struct xela_server_ros2__msg__Taxel
{
  uint16_t x;
  uint16_t y;
  uint16_t z;
} xela_server_ros2__msg__Taxel;

// Struct for a sequence of xela_server_ros2__msg__Taxel.
typedef struct xela_server_ros2__msg__Taxel__Sequence
{
  xela_server_ros2__msg__Taxel * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} xela_server_ros2__msg__Taxel__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // XELA_SERVER_ROS2__MSG__DETAIL__TAXEL__STRUCT_H_
