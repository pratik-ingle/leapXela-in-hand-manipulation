// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from xela_server_ros2:srv/XelaSensorStream.idl
// generated code does not contain a copyright notice

#ifndef XELA_SERVER_ROS2__SRV__DETAIL__XELA_SENSOR_STREAM__FUNCTIONS_H_
#define XELA_SERVER_ROS2__SRV__DETAIL__XELA_SENSOR_STREAM__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "xela_server_ros2/msg/rosidl_generator_c__visibility_control.h"

#include "xela_server_ros2/srv/detail/xela_sensor_stream__struct.h"

/// Initialize srv/XelaSensorStream message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * xela_server_ros2__srv__XelaSensorStream_Request
 * )) before or use
 * xela_server_ros2__srv__XelaSensorStream_Request__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_xela_server_ros2
bool
xela_server_ros2__srv__XelaSensorStream_Request__init(xela_server_ros2__srv__XelaSensorStream_Request * msg);

/// Finalize srv/XelaSensorStream message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_xela_server_ros2
void
xela_server_ros2__srv__XelaSensorStream_Request__fini(xela_server_ros2__srv__XelaSensorStream_Request * msg);

/// Create srv/XelaSensorStream message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * xela_server_ros2__srv__XelaSensorStream_Request__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_xela_server_ros2
xela_server_ros2__srv__XelaSensorStream_Request *
xela_server_ros2__srv__XelaSensorStream_Request__create();

/// Destroy srv/XelaSensorStream message.
/**
 * It calls
 * xela_server_ros2__srv__XelaSensorStream_Request__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_xela_server_ros2
void
xela_server_ros2__srv__XelaSensorStream_Request__destroy(xela_server_ros2__srv__XelaSensorStream_Request * msg);

/// Check for srv/XelaSensorStream message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_xela_server_ros2
bool
xela_server_ros2__srv__XelaSensorStream_Request__are_equal(const xela_server_ros2__srv__XelaSensorStream_Request * lhs, const xela_server_ros2__srv__XelaSensorStream_Request * rhs);

/// Copy a srv/XelaSensorStream message.
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
xela_server_ros2__srv__XelaSensorStream_Request__copy(
  const xela_server_ros2__srv__XelaSensorStream_Request * input,
  xela_server_ros2__srv__XelaSensorStream_Request * output);

/// Initialize array of srv/XelaSensorStream messages.
/**
 * It allocates the memory for the number of elements and calls
 * xela_server_ros2__srv__XelaSensorStream_Request__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_xela_server_ros2
bool
xela_server_ros2__srv__XelaSensorStream_Request__Sequence__init(xela_server_ros2__srv__XelaSensorStream_Request__Sequence * array, size_t size);

/// Finalize array of srv/XelaSensorStream messages.
/**
 * It calls
 * xela_server_ros2__srv__XelaSensorStream_Request__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_xela_server_ros2
void
xela_server_ros2__srv__XelaSensorStream_Request__Sequence__fini(xela_server_ros2__srv__XelaSensorStream_Request__Sequence * array);

/// Create array of srv/XelaSensorStream messages.
/**
 * It allocates the memory for the array and calls
 * xela_server_ros2__srv__XelaSensorStream_Request__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_xela_server_ros2
xela_server_ros2__srv__XelaSensorStream_Request__Sequence *
xela_server_ros2__srv__XelaSensorStream_Request__Sequence__create(size_t size);

/// Destroy array of srv/XelaSensorStream messages.
/**
 * It calls
 * xela_server_ros2__srv__XelaSensorStream_Request__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_xela_server_ros2
void
xela_server_ros2__srv__XelaSensorStream_Request__Sequence__destroy(xela_server_ros2__srv__XelaSensorStream_Request__Sequence * array);

/// Check for srv/XelaSensorStream message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_xela_server_ros2
bool
xela_server_ros2__srv__XelaSensorStream_Request__Sequence__are_equal(const xela_server_ros2__srv__XelaSensorStream_Request__Sequence * lhs, const xela_server_ros2__srv__XelaSensorStream_Request__Sequence * rhs);

/// Copy an array of srv/XelaSensorStream messages.
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
xela_server_ros2__srv__XelaSensorStream_Request__Sequence__copy(
  const xela_server_ros2__srv__XelaSensorStream_Request__Sequence * input,
  xela_server_ros2__srv__XelaSensorStream_Request__Sequence * output);

/// Initialize srv/XelaSensorStream message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * xela_server_ros2__srv__XelaSensorStream_Response
 * )) before or use
 * xela_server_ros2__srv__XelaSensorStream_Response__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_xela_server_ros2
bool
xela_server_ros2__srv__XelaSensorStream_Response__init(xela_server_ros2__srv__XelaSensorStream_Response * msg);

/// Finalize srv/XelaSensorStream message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_xela_server_ros2
void
xela_server_ros2__srv__XelaSensorStream_Response__fini(xela_server_ros2__srv__XelaSensorStream_Response * msg);

/// Create srv/XelaSensorStream message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * xela_server_ros2__srv__XelaSensorStream_Response__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_xela_server_ros2
xela_server_ros2__srv__XelaSensorStream_Response *
xela_server_ros2__srv__XelaSensorStream_Response__create();

/// Destroy srv/XelaSensorStream message.
/**
 * It calls
 * xela_server_ros2__srv__XelaSensorStream_Response__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_xela_server_ros2
void
xela_server_ros2__srv__XelaSensorStream_Response__destroy(xela_server_ros2__srv__XelaSensorStream_Response * msg);

/// Check for srv/XelaSensorStream message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_xela_server_ros2
bool
xela_server_ros2__srv__XelaSensorStream_Response__are_equal(const xela_server_ros2__srv__XelaSensorStream_Response * lhs, const xela_server_ros2__srv__XelaSensorStream_Response * rhs);

/// Copy a srv/XelaSensorStream message.
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
xela_server_ros2__srv__XelaSensorStream_Response__copy(
  const xela_server_ros2__srv__XelaSensorStream_Response * input,
  xela_server_ros2__srv__XelaSensorStream_Response * output);

/// Initialize array of srv/XelaSensorStream messages.
/**
 * It allocates the memory for the number of elements and calls
 * xela_server_ros2__srv__XelaSensorStream_Response__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_xela_server_ros2
bool
xela_server_ros2__srv__XelaSensorStream_Response__Sequence__init(xela_server_ros2__srv__XelaSensorStream_Response__Sequence * array, size_t size);

/// Finalize array of srv/XelaSensorStream messages.
/**
 * It calls
 * xela_server_ros2__srv__XelaSensorStream_Response__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_xela_server_ros2
void
xela_server_ros2__srv__XelaSensorStream_Response__Sequence__fini(xela_server_ros2__srv__XelaSensorStream_Response__Sequence * array);

/// Create array of srv/XelaSensorStream messages.
/**
 * It allocates the memory for the array and calls
 * xela_server_ros2__srv__XelaSensorStream_Response__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_xela_server_ros2
xela_server_ros2__srv__XelaSensorStream_Response__Sequence *
xela_server_ros2__srv__XelaSensorStream_Response__Sequence__create(size_t size);

/// Destroy array of srv/XelaSensorStream messages.
/**
 * It calls
 * xela_server_ros2__srv__XelaSensorStream_Response__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_xela_server_ros2
void
xela_server_ros2__srv__XelaSensorStream_Response__Sequence__destroy(xela_server_ros2__srv__XelaSensorStream_Response__Sequence * array);

/// Check for srv/XelaSensorStream message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_xela_server_ros2
bool
xela_server_ros2__srv__XelaSensorStream_Response__Sequence__are_equal(const xela_server_ros2__srv__XelaSensorStream_Response__Sequence * lhs, const xela_server_ros2__srv__XelaSensorStream_Response__Sequence * rhs);

/// Copy an array of srv/XelaSensorStream messages.
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
xela_server_ros2__srv__XelaSensorStream_Response__Sequence__copy(
  const xela_server_ros2__srv__XelaSensorStream_Response__Sequence * input,
  xela_server_ros2__srv__XelaSensorStream_Response__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // XELA_SERVER_ROS2__SRV__DETAIL__XELA_SENSOR_STREAM__FUNCTIONS_H_
