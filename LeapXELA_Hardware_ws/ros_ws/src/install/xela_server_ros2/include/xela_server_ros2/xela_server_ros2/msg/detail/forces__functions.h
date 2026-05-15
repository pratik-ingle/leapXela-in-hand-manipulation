// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from xela_server_ros2:msg/Forces.idl
// generated code does not contain a copyright notice

#ifndef XELA_SERVER_ROS2__MSG__DETAIL__FORCES__FUNCTIONS_H_
#define XELA_SERVER_ROS2__MSG__DETAIL__FORCES__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "xela_server_ros2/msg/rosidl_generator_c__visibility_control.h"

#include "xela_server_ros2/msg/detail/forces__struct.h"

/// Initialize msg/Forces message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * xela_server_ros2__msg__Forces
 * )) before or use
 * xela_server_ros2__msg__Forces__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_xela_server_ros2
bool
xela_server_ros2__msg__Forces__init(xela_server_ros2__msg__Forces * msg);

/// Finalize msg/Forces message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_xela_server_ros2
void
xela_server_ros2__msg__Forces__fini(xela_server_ros2__msg__Forces * msg);

/// Create msg/Forces message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * xela_server_ros2__msg__Forces__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_xela_server_ros2
xela_server_ros2__msg__Forces *
xela_server_ros2__msg__Forces__create();

/// Destroy msg/Forces message.
/**
 * It calls
 * xela_server_ros2__msg__Forces__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_xela_server_ros2
void
xela_server_ros2__msg__Forces__destroy(xela_server_ros2__msg__Forces * msg);

/// Check for msg/Forces message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_xela_server_ros2
bool
xela_server_ros2__msg__Forces__are_equal(const xela_server_ros2__msg__Forces * lhs, const xela_server_ros2__msg__Forces * rhs);

/// Copy a msg/Forces message.
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
xela_server_ros2__msg__Forces__copy(
  const xela_server_ros2__msg__Forces * input,
  xela_server_ros2__msg__Forces * output);

/// Initialize array of msg/Forces messages.
/**
 * It allocates the memory for the number of elements and calls
 * xela_server_ros2__msg__Forces__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_xela_server_ros2
bool
xela_server_ros2__msg__Forces__Sequence__init(xela_server_ros2__msg__Forces__Sequence * array, size_t size);

/// Finalize array of msg/Forces messages.
/**
 * It calls
 * xela_server_ros2__msg__Forces__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_xela_server_ros2
void
xela_server_ros2__msg__Forces__Sequence__fini(xela_server_ros2__msg__Forces__Sequence * array);

/// Create array of msg/Forces messages.
/**
 * It allocates the memory for the array and calls
 * xela_server_ros2__msg__Forces__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_xela_server_ros2
xela_server_ros2__msg__Forces__Sequence *
xela_server_ros2__msg__Forces__Sequence__create(size_t size);

/// Destroy array of msg/Forces messages.
/**
 * It calls
 * xela_server_ros2__msg__Forces__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_xela_server_ros2
void
xela_server_ros2__msg__Forces__Sequence__destroy(xela_server_ros2__msg__Forces__Sequence * array);

/// Check for msg/Forces message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_xela_server_ros2
bool
xela_server_ros2__msg__Forces__Sequence__are_equal(const xela_server_ros2__msg__Forces__Sequence * lhs, const xela_server_ros2__msg__Forces__Sequence * rhs);

/// Copy an array of msg/Forces messages.
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
xela_server_ros2__msg__Forces__Sequence__copy(
  const xela_server_ros2__msg__Forces__Sequence * input,
  xela_server_ros2__msg__Forces__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // XELA_SERVER_ROS2__MSG__DETAIL__FORCES__FUNCTIONS_H_
