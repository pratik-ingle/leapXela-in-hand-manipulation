// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from leap_hand:srv/LeapVelocity.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "leap_hand/srv/detail/leap_velocity__rosidl_typesupport_introspection_c.h"
#include "leap_hand/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "leap_hand/srv/detail/leap_velocity__functions.h"
#include "leap_hand/srv/detail/leap_velocity__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void leap_hand__srv__LeapVelocity_Request__rosidl_typesupport_introspection_c__LeapVelocity_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  leap_hand__srv__LeapVelocity_Request__init(message_memory);
}

void leap_hand__srv__LeapVelocity_Request__rosidl_typesupport_introspection_c__LeapVelocity_Request_fini_function(void * message_memory)
{
  leap_hand__srv__LeapVelocity_Request__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember leap_hand__srv__LeapVelocity_Request__rosidl_typesupport_introspection_c__LeapVelocity_Request_message_member_array[1] = {
  {
    "structure_needs_at_least_one_member",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(leap_hand__srv__LeapVelocity_Request, structure_needs_at_least_one_member),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers leap_hand__srv__LeapVelocity_Request__rosidl_typesupport_introspection_c__LeapVelocity_Request_message_members = {
  "leap_hand__srv",  // message namespace
  "LeapVelocity_Request",  // message name
  1,  // number of fields
  sizeof(leap_hand__srv__LeapVelocity_Request),
  leap_hand__srv__LeapVelocity_Request__rosidl_typesupport_introspection_c__LeapVelocity_Request_message_member_array,  // message members
  leap_hand__srv__LeapVelocity_Request__rosidl_typesupport_introspection_c__LeapVelocity_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  leap_hand__srv__LeapVelocity_Request__rosidl_typesupport_introspection_c__LeapVelocity_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t leap_hand__srv__LeapVelocity_Request__rosidl_typesupport_introspection_c__LeapVelocity_Request_message_type_support_handle = {
  0,
  &leap_hand__srv__LeapVelocity_Request__rosidl_typesupport_introspection_c__LeapVelocity_Request_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_leap_hand
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, leap_hand, srv, LeapVelocity_Request)() {
  if (!leap_hand__srv__LeapVelocity_Request__rosidl_typesupport_introspection_c__LeapVelocity_Request_message_type_support_handle.typesupport_identifier) {
    leap_hand__srv__LeapVelocity_Request__rosidl_typesupport_introspection_c__LeapVelocity_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &leap_hand__srv__LeapVelocity_Request__rosidl_typesupport_introspection_c__LeapVelocity_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "leap_hand/srv/detail/leap_velocity__rosidl_typesupport_introspection_c.h"
// already included above
// #include "leap_hand/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "leap_hand/srv/detail/leap_velocity__functions.h"
// already included above
// #include "leap_hand/srv/detail/leap_velocity__struct.h"


// Include directives for member types
// Member `velocity`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void leap_hand__srv__LeapVelocity_Response__rosidl_typesupport_introspection_c__LeapVelocity_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  leap_hand__srv__LeapVelocity_Response__init(message_memory);
}

void leap_hand__srv__LeapVelocity_Response__rosidl_typesupport_introspection_c__LeapVelocity_Response_fini_function(void * message_memory)
{
  leap_hand__srv__LeapVelocity_Response__fini(message_memory);
}

size_t leap_hand__srv__LeapVelocity_Response__rosidl_typesupport_introspection_c__size_function__LeapVelocity_Response__velocity(
  const void * untyped_member)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return member->size;
}

const void * leap_hand__srv__LeapVelocity_Response__rosidl_typesupport_introspection_c__get_const_function__LeapVelocity_Response__velocity(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void * leap_hand__srv__LeapVelocity_Response__rosidl_typesupport_introspection_c__get_function__LeapVelocity_Response__velocity(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void leap_hand__srv__LeapVelocity_Response__rosidl_typesupport_introspection_c__fetch_function__LeapVelocity_Response__velocity(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    leap_hand__srv__LeapVelocity_Response__rosidl_typesupport_introspection_c__get_const_function__LeapVelocity_Response__velocity(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void leap_hand__srv__LeapVelocity_Response__rosidl_typesupport_introspection_c__assign_function__LeapVelocity_Response__velocity(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    leap_hand__srv__LeapVelocity_Response__rosidl_typesupport_introspection_c__get_function__LeapVelocity_Response__velocity(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

bool leap_hand__srv__LeapVelocity_Response__rosidl_typesupport_introspection_c__resize_function__LeapVelocity_Response__velocity(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  rosidl_runtime_c__double__Sequence__fini(member);
  return rosidl_runtime_c__double__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember leap_hand__srv__LeapVelocity_Response__rosidl_typesupport_introspection_c__LeapVelocity_Response_message_member_array[1] = {
  {
    "velocity",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(leap_hand__srv__LeapVelocity_Response, velocity),  // bytes offset in struct
    NULL,  // default value
    leap_hand__srv__LeapVelocity_Response__rosidl_typesupport_introspection_c__size_function__LeapVelocity_Response__velocity,  // size() function pointer
    leap_hand__srv__LeapVelocity_Response__rosidl_typesupport_introspection_c__get_const_function__LeapVelocity_Response__velocity,  // get_const(index) function pointer
    leap_hand__srv__LeapVelocity_Response__rosidl_typesupport_introspection_c__get_function__LeapVelocity_Response__velocity,  // get(index) function pointer
    leap_hand__srv__LeapVelocity_Response__rosidl_typesupport_introspection_c__fetch_function__LeapVelocity_Response__velocity,  // fetch(index, &value) function pointer
    leap_hand__srv__LeapVelocity_Response__rosidl_typesupport_introspection_c__assign_function__LeapVelocity_Response__velocity,  // assign(index, value) function pointer
    leap_hand__srv__LeapVelocity_Response__rosidl_typesupport_introspection_c__resize_function__LeapVelocity_Response__velocity  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers leap_hand__srv__LeapVelocity_Response__rosidl_typesupport_introspection_c__LeapVelocity_Response_message_members = {
  "leap_hand__srv",  // message namespace
  "LeapVelocity_Response",  // message name
  1,  // number of fields
  sizeof(leap_hand__srv__LeapVelocity_Response),
  leap_hand__srv__LeapVelocity_Response__rosidl_typesupport_introspection_c__LeapVelocity_Response_message_member_array,  // message members
  leap_hand__srv__LeapVelocity_Response__rosidl_typesupport_introspection_c__LeapVelocity_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  leap_hand__srv__LeapVelocity_Response__rosidl_typesupport_introspection_c__LeapVelocity_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t leap_hand__srv__LeapVelocity_Response__rosidl_typesupport_introspection_c__LeapVelocity_Response_message_type_support_handle = {
  0,
  &leap_hand__srv__LeapVelocity_Response__rosidl_typesupport_introspection_c__LeapVelocity_Response_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_leap_hand
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, leap_hand, srv, LeapVelocity_Response)() {
  if (!leap_hand__srv__LeapVelocity_Response__rosidl_typesupport_introspection_c__LeapVelocity_Response_message_type_support_handle.typesupport_identifier) {
    leap_hand__srv__LeapVelocity_Response__rosidl_typesupport_introspection_c__LeapVelocity_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &leap_hand__srv__LeapVelocity_Response__rosidl_typesupport_introspection_c__LeapVelocity_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "leap_hand/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "leap_hand/srv/detail/leap_velocity__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers leap_hand__srv__detail__leap_velocity__rosidl_typesupport_introspection_c__LeapVelocity_service_members = {
  "leap_hand__srv",  // service namespace
  "LeapVelocity",  // service name
  // these two fields are initialized below on the first access
  NULL,  // request message
  // leap_hand__srv__detail__leap_velocity__rosidl_typesupport_introspection_c__LeapVelocity_Request_message_type_support_handle,
  NULL  // response message
  // leap_hand__srv__detail__leap_velocity__rosidl_typesupport_introspection_c__LeapVelocity_Response_message_type_support_handle
};

static rosidl_service_type_support_t leap_hand__srv__detail__leap_velocity__rosidl_typesupport_introspection_c__LeapVelocity_service_type_support_handle = {
  0,
  &leap_hand__srv__detail__leap_velocity__rosidl_typesupport_introspection_c__LeapVelocity_service_members,
  get_service_typesupport_handle_function,
};

// Forward declaration of request/response type support functions
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, leap_hand, srv, LeapVelocity_Request)();

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, leap_hand, srv, LeapVelocity_Response)();

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_leap_hand
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, leap_hand, srv, LeapVelocity)() {
  if (!leap_hand__srv__detail__leap_velocity__rosidl_typesupport_introspection_c__LeapVelocity_service_type_support_handle.typesupport_identifier) {
    leap_hand__srv__detail__leap_velocity__rosidl_typesupport_introspection_c__LeapVelocity_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)leap_hand__srv__detail__leap_velocity__rosidl_typesupport_introspection_c__LeapVelocity_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, leap_hand, srv, LeapVelocity_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, leap_hand, srv, LeapVelocity_Response)()->data;
  }

  return &leap_hand__srv__detail__leap_velocity__rosidl_typesupport_introspection_c__LeapVelocity_service_type_support_handle;
}
