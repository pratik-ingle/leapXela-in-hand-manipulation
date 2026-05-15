// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from xela_server_ros2:msg/SensorFull.idl
// generated code does not contain a copyright notice

#ifndef XELA_SERVER_ROS2__MSG__DETAIL__SENSOR_FULL__FUNCTIONS_H_
#define XELA_SERVER_ROS2__MSG__DETAIL__SENSOR_FULL__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "xela_server_ros2/msg/rosidl_generator_c__visibility_control.h"

#include "xela_server_ros2/msg/detail/sensor_full__struct.h"

/// Initialize msg/SensorFull message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * xela_server_ros2__msg__SensorFull
 * )) before or use
 * xela_server_ros2__msg__SensorFull__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_xela_server_ros2
bool
xela_server_ros2__msg__SensorFull__init(xela_server_ros2__msg__SensorFull * msg);

/// Finalize msg/SensorFull message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_xela_server_ros2
void
xela_server_ros2__msg__SensorFull__fini(xela_server_ros2__msg__SensorFull * msg);

/// Create msg/SensorFull message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * xela_server_ros2__msg__SensorFull__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_xela_server_ros2
xela_server_ros2__msg__SensorFull *
xela_server_ros2__msg__SensorFull__create();

/// Destroy msg/SensorFull message.
/**
 * It calls
 * xela_server_ros2__msg__SensorFull__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_xela_server_ros2
void
xela_server_ros2__msg__SensorFull__destroy(xela_server_ros2__msg__SensorFull * msg);

/// Check for msg/SensorFull message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_xela_server_ros2
bool
xela_server_ros2__msg__SensorFull__are_equal(const xela_server_ros2__msg__SensorFull * lhs, const xela_server_ros2__msg__SensorFull * rhs);

/// Copy a msg/SensorFull message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_xela_server_ros2
bool
xela_server_ros2__msg__SensorFull__copy(
  const xela_server_ros2__msg__SensorFull * input,
  xela_server_ros2__msg__SensorFull * output);

/// Initialize array of msg/SensorFull messages.
/**
 * It allocates the memory for the number of elements and calls
 * xela_server_ros2__msg__SensorFull__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_xela_server_ros2
bool
xela_server_ros2__msg__SensorFull__Sequence__init(xela_server_ros2__msg__SensorFull__Sequence * array, size_t size);

/// Finalize array of msg/SensorFull messages.
/**
 * It calls
 * xela_server_ros2__msg__SensorFull__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_xela_server_ros2
void
xela_server_ros2__msg__SensorFull__Sequence__fini(xela_server_ros2__msg__SensorFull__Sequence * array);

/// Create array of msg/SensorFull messages.
/**
 * It allocates the memory for the array and calls
 * xela_server_ros2__msg__SensorFull__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_xela_server_ros2
xela_server_ros2__msg__SensorFull__Sequence *
xela_server_ros2__msg__SensorFull__Sequence__create(size_t size);

/// Destroy array of msg/SensorFull messages.
/**
 * It calls
 * xela_server_ros2__msg__SensorFull__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_xela_server_ros2
void
xela_server_ros2__msg__SensorFull__Sequence__destroy(xela_server_ros2__msg__SensorFull__Sequence * array);

/// Check for msg/SensorFull message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_xela_server_ros2
bool
xela_server_ros2__msg__SensorFull__Sequence__are_equal(const xela_server_ros2__msg__SensorFull__Sequence * lhs, const xela_server_ros2__msg__SensorFull__Sequence * rhs);

/// Copy an array of msg/SensorFull messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_xela_server_ros2
bool
xela_server_ros2__msg__SensorFull__Sequence__copy(
  const xela_server_ros2__msg__SensorFull__Sequence * input,
  xela_server_ros2__msg__SensorFull__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // XELA_SERVER_ROS2__MSG__DETAIL__SENSOR_FULL__FUNCTIONS_H_
