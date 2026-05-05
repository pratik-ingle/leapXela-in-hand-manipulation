// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from leap_hand:srv/LeapEffort.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "leap_hand/srv/detail/leap_effort__rosidl_typesupport_introspection_c.h"
#include "leap_hand/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "leap_hand/srv/detail/leap_effort__functions.h"
#include "leap_hand/srv/detail/leap_effort__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void leap_hand__srv__LeapEffort_Request__rosidl_typesupport_introspection_c__LeapEffort_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  leap_hand__srv__LeapEffort_Request__init(message_memory);
}

void leap_hand__srv__LeapEffort_Request__rosidl_typesupport_introspection_c__LeapEffort_Request_fini_function(void * message_memory)
{
  leap_hand__srv__LeapEffort_Request__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember leap_hand__srv__LeapEffort_Request__rosidl_typesupport_introspection_c__LeapEffort_Request_message_member_array[1] = {
  {
    "structure_needs_at_least_one_member",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(leap_hand__srv__LeapEffort_Request, structure_needs_at_least_one_member),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers leap_hand__srv__LeapEffort_Request__rosidl_typesupport_introspection_c__LeapEffort_Request_message_members = {
  "leap_hand__srv",  // message namespace
  "LeapEffort_Request",  // message name
  1,  // number of fields
  sizeof(leap_hand__srv__LeapEffort_Request),
  leap_hand__srv__LeapEffort_Request__rosidl_typesupport_introspection_c__LeapEffort_Request_message_member_array,  // message members
  leap_hand__srv__LeapEffort_Request__rosidl_typesupport_introspection_c__LeapEffort_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  leap_hand__srv__LeapEffort_Request__rosidl_typesupport_introspection_c__LeapEffort_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t leap_hand__srv__LeapEffort_Request__rosidl_typesupport_introspection_c__LeapEffort_Request_message_type_support_handle = {
  0,
  &leap_hand__srv__LeapEffort_Request__rosidl_typesupport_introspection_c__LeapEffort_Request_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_leap_hand
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, leap_hand, srv, LeapEffort_Request)() {
  if (!leap_hand__srv__LeapEffort_Request__rosidl_typesupport_introspection_c__LeapEffort_Request_message_type_support_handle.typesupport_identifier) {
    leap_hand__srv__LeapEffort_Request__rosidl_typesupport_introspection_c__LeapEffort_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &leap_hand__srv__LeapEffort_Request__rosidl_typesupport_introspection_c__LeapEffort_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "leap_hand/srv/detail/leap_effort__rosidl_typesupport_introspection_c.h"
// already included above
// #include "leap_hand/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "leap_hand/srv/detail/leap_effort__functions.h"
// already included above
// #include "leap_hand/srv/detail/leap_effort__struct.h"


// Include directives for member types
// Member `effort`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void leap_hand__srv__LeapEffort_Response__rosidl_typesupport_introspection_c__LeapEffort_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  leap_hand__srv__LeapEffort_Response__init(message_memory);
}

void leap_hand__srv__LeapEffort_Response__rosidl_typesupport_introspection_c__LeapEffort_Response_fini_function(void * message_memory)
{
  leap_hand__srv__LeapEffort_Response__fini(message_memory);
}

size_t leap_hand__srv__LeapEffort_Response__rosidl_typesupport_introspection_c__size_function__LeapEffort_Response__effort(
  const void * untyped_member)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return member->size;
}

const void * leap_hand__srv__LeapEffort_Response__rosidl_typesupport_introspection_c__get_const_function__LeapEffort_Response__effort(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void * leap_hand__srv__LeapEffort_Response__rosidl_typesupport_introspection_c__get_function__LeapEffort_Response__effort(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void leap_hand__srv__LeapEffort_Response__rosidl_typesupport_introspection_c__fetch_function__LeapEffort_Response__effort(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    leap_hand__srv__LeapEffort_Response__rosidl_typesupport_introspection_c__get_const_function__LeapEffort_Response__effort(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void leap_hand__srv__LeapEffort_Response__rosidl_typesupport_introspection_c__assign_function__LeapEffort_Response__effort(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    leap_hand__srv__LeapEffort_Response__rosidl_typesupport_introspection_c__get_function__LeapEffort_Response__effort(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

bool leap_hand__srv__LeapEffort_Response__rosidl_typesupport_introspection_c__resize_function__LeapEffort_Response__effort(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  rosidl_runtime_c__double__Sequence__fini(member);
  return rosidl_runtime_c__double__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember leap_hand__srv__LeapEffort_Response__rosidl_typesupport_introspection_c__LeapEffort_Response_message_member_array[1] = {
  {
    "effort",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(leap_hand__srv__LeapEffort_Response, effort),  // bytes offset in struct
    NULL,  // default value
    leap_hand__srv__LeapEffort_Response__rosidl_typesupport_introspection_c__size_function__LeapEffort_Response__effort,  // size() function pointer
    leap_hand__srv__LeapEffort_Response__rosidl_typesupport_introspection_c__get_const_function__LeapEffort_Response__effort,  // get_const(index) function pointer
    leap_hand__srv__LeapEffort_Response__rosidl_typesupport_introspection_c__get_function__LeapEffort_Response__effort,  // get(index) function pointer
    leap_hand__srv__LeapEffort_Response__rosidl_typesupport_introspection_c__fetch_function__LeapEffort_Response__effort,  // fetch(index, &value) function pointer
    leap_hand__srv__LeapEffort_Response__rosidl_typesupport_introspection_c__assign_function__LeapEffort_Response__effort,  // assign(index, value) function pointer
    leap_hand__srv__LeapEffort_Response__rosidl_typesupport_introspection_c__resize_function__LeapEffort_Response__effort  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers leap_hand__srv__LeapEffort_Response__rosidl_typesupport_introspection_c__LeapEffort_Response_message_members = {
  "leap_hand__srv",  // message namespace
  "LeapEffort_Response",  // message name
  1,  // number of fields
  sizeof(leap_hand__srv__LeapEffort_Response),
  leap_hand__srv__LeapEffort_Response__rosidl_typesupport_introspection_c__LeapEffort_Response_message_member_array,  // message members
  leap_hand__srv__LeapEffort_Response__rosidl_typesupport_introspection_c__LeapEffort_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  leap_hand__srv__LeapEffort_Response__rosidl_typesupport_introspection_c__LeapEffort_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t leap_hand__srv__LeapEffort_Response__rosidl_typesupport_introspection_c__LeapEffort_Response_message_type_support_handle = {
  0,
  &leap_hand__srv__LeapEffort_Response__rosidl_typesupport_introspection_c__LeapEffort_Response_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_leap_hand
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, leap_hand, srv, LeapEffort_Response)() {
  if (!leap_hand__srv__LeapEffort_Response__rosidl_typesupport_introspection_c__LeapEffort_Response_message_type_support_handle.typesupport_identifier) {
    leap_hand__srv__LeapEffort_Response__rosidl_typesupport_introspection_c__LeapEffort_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &leap_hand__srv__LeapEffort_Response__rosidl_typesupport_introspection_c__LeapEffort_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "leap_hand/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "leap_hand/srv/detail/leap_effort__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers leap_hand__srv__detail__leap_effort__rosidl_typesupport_introspection_c__LeapEffort_service_members = {
  "leap_hand__srv",  // service namespace
  "LeapEffort",  // service name
  // these two fields are initialized below on the first access
  NULL,  // request message
  // leap_hand__srv__detail__leap_effort__rosidl_typesupport_introspection_c__LeapEffort_Request_message_type_support_handle,
  NULL  // response message
  // leap_hand__srv__detail__leap_effort__rosidl_typesupport_introspection_c__LeapEffort_Response_message_type_support_handle
};

static rosidl_service_type_support_t leap_hand__srv__detail__leap_effort__rosidl_typesupport_introspection_c__LeapEffort_service_type_support_handle = {
  0,
  &leap_hand__srv__detail__leap_effort__rosidl_typesupport_introspection_c__LeapEffort_service_members,
  get_service_typesupport_handle_function,
};

// Forward declaration of request/response type support functions
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, leap_hand, srv, LeapEffort_Request)();

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, leap_hand, srv, LeapEffort_Response)();

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_leap_hand
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, leap_hand, srv, LeapEffort)() {
  if (!leap_hand__srv__detail__leap_effort__rosidl_typesupport_introspection_c__LeapEffort_service_type_support_handle.typesupport_identifier) {
    leap_hand__srv__detail__leap_effort__rosidl_typesupport_introspection_c__LeapEffort_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)leap_hand__srv__detail__leap_effort__rosidl_typesupport_introspection_c__LeapEffort_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, leap_hand, srv, LeapEffort_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, leap_hand, srv, LeapEffort_Response)()->data;
  }

  return &leap_hand__srv__detail__leap_effort__rosidl_typesupport_introspection_c__LeapEffort_service_type_support_handle;
}
