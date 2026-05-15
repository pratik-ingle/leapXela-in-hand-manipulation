// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from xela_server_ros2:srv/XelaSensorStream.idl
// generated code does not contain a copyright notice

#ifndef XELA_SERVER_ROS2__SRV__DETAIL__XELA_SENSOR_STREAM__STRUCT_H_
#define XELA_SERVER_ROS2__SRV__DETAIL__XELA_SENSOR_STREAM__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in srv/XelaSensorStream in the package xela_server_ros2.
typedef struct xela_server_ros2__srv__XelaSensorStream_Request
{
  uint8_t sensor;
} xela_server_ros2__srv__XelaSensorStream_Request;

// Struct for a sequence of xela_server_ros2__srv__XelaSensorStream_Request.
typedef struct xela_server_ros2__srv__XelaSensorStream_Request__Sequence
{
  xela_server_ros2__srv__XelaSensorStream_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} xela_server_ros2__srv__XelaSensorStream_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'data'
#include "xela_server_ros2/msg/detail/sensor_full__struct.h"

/// Struct defined in srv/XelaSensorStream in the package xela_server_ros2.
typedef struct xela_server_ros2__srv__XelaSensorStream_Response
{
  xela_server_ros2__msg__SensorFull__Sequence data;
} xela_server_ros2__srv__XelaSensorStream_Response;

// Struct for a sequence of xela_server_ros2__srv__XelaSensorStream_Response.
typedef struct xela_server_ros2__srv__XelaSensorStream_Response__Sequence
{
  xela_server_ros2__srv__XelaSensorStream_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} xela_server_ros2__srv__XelaSensorStream_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // XELA_SERVER_ROS2__SRV__DETAIL__XELA_SENSOR_STREAM__STRUCT_H_
