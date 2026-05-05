// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from leap_hand:srv/LeapEffort.idl
// generated code does not contain a copyright notice

#ifndef LEAP_HAND__SRV__DETAIL__LEAP_EFFORT__STRUCT_H_
#define LEAP_HAND__SRV__DETAIL__LEAP_EFFORT__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in srv/LeapEffort in the package leap_hand.
typedef struct leap_hand__srv__LeapEffort_Request
{
  uint8_t structure_needs_at_least_one_member;
} leap_hand__srv__LeapEffort_Request;

// Struct for a sequence of leap_hand__srv__LeapEffort_Request.
typedef struct leap_hand__srv__LeapEffort_Request__Sequence
{
  leap_hand__srv__LeapEffort_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} leap_hand__srv__LeapEffort_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'effort'
#include "rosidl_runtime_c/primitives_sequence.h"

/// Struct defined in srv/LeapEffort in the package leap_hand.
typedef struct leap_hand__srv__LeapEffort_Response
{
  rosidl_runtime_c__double__Sequence effort;
} leap_hand__srv__LeapEffort_Response;

// Struct for a sequence of leap_hand__srv__LeapEffort_Response.
typedef struct leap_hand__srv__LeapEffort_Response__Sequence
{
  leap_hand__srv__LeapEffort_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} leap_hand__srv__LeapEffort_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // LEAP_HAND__SRV__DETAIL__LEAP_EFFORT__STRUCT_H_
