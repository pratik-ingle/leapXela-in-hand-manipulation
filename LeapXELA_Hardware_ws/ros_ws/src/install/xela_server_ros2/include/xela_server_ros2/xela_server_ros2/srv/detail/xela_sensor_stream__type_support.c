// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from xela_server_ros2:srv/XelaSensorStream.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "xela_server_ros2/srv/detail/xela_sensor_stream__rosidl_typesupport_introspection_c.h"
#include "xela_server_ros2/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "xela_server_ros2/srv/detail/xela_sensor_stream__functions.h"
#include "xela_server_ros2/srv/detail/xela_sensor_stream__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void xela_server_ros2__srv__XelaSensorStream_Request__rosidl_typesupport_introspection_c__XelaSensorStream_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  xela_server_ros2__srv__XelaSensorStream_Request__init(message_memory);
}

void xela_server_ros2__srv__XelaSensorStream_Request__rosidl_typesupport_introspection_c__XelaSensorStream_Request_fini_function(void * message_memory)
{
  xela_server_ros2__srv__XelaSensorStream_Request__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember xela_server_ros2__srv__XelaSensorStream_Request__rosidl_typesupport_introspection_c__XelaSensorStream_Request_message_member_array[1] = {
  {
    "sensor",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(xela_server_ros2__srv__XelaSensorStream_Request, sensor),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers xela_server_ros2__srv__XelaSensorStream_Request__rosidl_typesupport_introspection_c__XelaSensorStream_Request_message_members = {
  "xela_server_ros2__srv",  // message namespace
  "XelaSensorStream_Request",  // message name
  1,  // number of fields
  sizeof(xela_server_ros2__srv__XelaSensorStream_Request),
  xela_server_ros2__srv__XelaSensorStream_Request__rosidl_typesupport_introspection_c__XelaSensorStream_Request_message_member_array,  // message members
  xela_server_ros2__srv__XelaSensorStream_Request__rosidl_typesupport_introspection_c__XelaSensorStream_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  xela_server_ros2__srv__XelaSensorStream_Request__rosidl_typesupport_introspection_c__XelaSensorStream_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t xela_server_ros2__srv__XelaSensorStream_Request__rosidl_typesupport_introspection_c__XelaSensorStream_Request_message_type_support_handle = {
  0,
  &xela_server_ros2__srv__XelaSensorStream_Request__rosidl_typesupport_introspection_c__XelaSensorStream_Request_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_xela_server_ros2
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, xela_server_ros2, srv, XelaSensorStream_Request)() {
  if (!xela_server_ros2__srv__XelaSensorStream_Request__rosidl_typesupport_introspection_c__XelaSensorStream_Request_message_type_support_handle.typesupport_identifier) {
    xela_server_ros2__srv__XelaSensorStream_Request__rosidl_typesupport_introspection_c__XelaSensorStream_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &xela_server_ros2__srv__XelaSensorStream_Request__rosidl_typesupport_introspection_c__XelaSensorStream_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "xela_server_ros2/srv/detail/xela_sensor_stream__rosidl_typesupport_introspection_c.h"
// already included above
// #include "xela_server_ros2/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "xela_server_ros2/srv/detail/xela_sensor_stream__functions.h"
// already included above
// #include "xela_server_ros2/srv/detail/xela_sensor_stream__struct.h"


// Include directives for member types
// Member `data`
#include "xela_server_ros2/msg/sensor_full.h"
// Member `data`
#include "xela_server_ros2/msg/detail/sensor_full__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void xela_server_ros2__srv__XelaSensorStream_Response__rosidl_typesupport_introspection_c__XelaSensorStream_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  xela_server_ros2__srv__XelaSensorStream_Response__init(message_memory);
}

void xela_server_ros2__srv__XelaSensorStream_Response__rosidl_typesupport_introspection_c__XelaSensorStream_Response_fini_function(void * message_memory)
{
  xela_server_ros2__srv__XelaSensorStream_Response__fini(message_memory);
}

size_t xela_server_ros2__srv__XelaSensorStream_Response__rosidl_typesupport_introspection_c__size_function__XelaSensorStream_Response__data(
  const void * untyped_member)
{
  const xela_server_ros2__msg__SensorFull__Sequence * member =
    (const xela_server_ros2__msg__SensorFull__Sequence *)(untyped_member);
  return member->size;
}

const void * xela_server_ros2__srv__XelaSensorStream_Response__rosidl_typesupport_introspection_c__get_const_function__XelaSensorStream_Response__data(
  const void * untyped_member, size_t index)
{
  const xela_server_ros2__msg__SensorFull__Sequence * member =
    (const xela_server_ros2__msg__SensorFull__Sequence *)(untyped_member);
  return &member->data[index];
}

void * xela_server_ros2__srv__XelaSensorStream_Response__rosidl_typesupport_introspection_c__get_function__XelaSensorStream_Response__data(
  void * untyped_member, size_t index)
{
  xela_server_ros2__msg__SensorFull__Sequence * member =
    (xela_server_ros2__msg__SensorFull__Sequence *)(untyped_member);
  return &member->data[index];
}

void xela_server_ros2__srv__XelaSensorStream_Response__rosidl_typesupport_introspection_c__fetch_function__XelaSensorStream_Response__data(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const xela_server_ros2__msg__SensorFull * item =
    ((const xela_server_ros2__msg__SensorFull *)
    xela_server_ros2__srv__XelaSensorStream_Response__rosidl_typesupport_introspection_c__get_const_function__XelaSensorStream_Response__data(untyped_member, index));
  xela_server_ros2__msg__SensorFull * value =
    (xela_server_ros2__msg__SensorFull *)(untyped_value);
  *value = *item;
}

void xela_server_ros2__srv__XelaSensorStream_Response__rosidl_typesupport_introspection_c__assign_function__XelaSensorStream_Response__data(
  void * untyped_member, size_t index, const void * untyped_value)
{
  xela_server_ros2__msg__SensorFull * item =
    ((xela_server_ros2__msg__SensorFull *)
    xela_server_ros2__srv__XelaSensorStream_Response__rosidl_typesupport_introspection_c__get_function__XelaSensorStream_Response__data(untyped_member, index));
  const xela_server_ros2__msg__SensorFull * value =
    (const xela_server_ros2__msg__SensorFull *)(untyped_value);
  *item = *value;
}

bool xela_server_ros2__srv__XelaSensorStream_Response__rosidl_typesupport_introspection_c__resize_function__XelaSensorStream_Response__data(
  void * untyped_member, size_t size)
{
  xela_server_ros2__msg__SensorFull__Sequence * member =
    (xela_server_ros2__msg__SensorFull__Sequence *)(untyped_member);
  xela_server_ros2__msg__SensorFull__Sequence__fini(member);
  return xela_server_ros2__msg__SensorFull__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember xela_server_ros2__srv__XelaSensorStream_Response__rosidl_typesupport_introspection_c__XelaSensorStream_Response_message_member_array[1] = {
  {
    "data",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(xela_server_ros2__srv__XelaSensorStream_Response, data),  // bytes offset in struct
    NULL,  // default value
    xela_server_ros2__srv__XelaSensorStream_Response__rosidl_typesupport_introspection_c__size_function__XelaSensorStream_Response__data,  // size() function pointer
    xela_server_ros2__srv__XelaSensorStream_Response__rosidl_typesupport_introspection_c__get_const_function__XelaSensorStream_Response__data,  // get_const(index) function pointer
    xela_server_ros2__srv__XelaSensorStream_Response__rosidl_typesupport_introspection_c__get_function__XelaSensorStream_Response__data,  // get(index) function pointer
    xela_server_ros2__srv__XelaSensorStream_Response__rosidl_typesupport_introspection_c__fetch_function__XelaSensorStream_Response__data,  // fetch(index, &value) function pointer
    xela_server_ros2__srv__XelaSensorStream_Response__rosidl_typesupport_introspection_c__assign_function__XelaSensorStream_Response__data,  // assign(index, value) function pointer
    xela_server_ros2__srv__XelaSensorStream_Response__rosidl_typesupport_introspection_c__resize_function__XelaSensorStream_Response__data  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers xela_server_ros2__srv__XelaSensorStream_Response__rosidl_typesupport_introspection_c__XelaSensorStream_Response_message_members = {
  "xela_server_ros2__srv",  // message namespace
  "XelaSensorStream_Response",  // message name
  1,  // number of fields
  sizeof(xela_server_ros2__srv__XelaSensorStream_Response),
  xela_server_ros2__srv__XelaSensorStream_Response__rosidl_typesupport_introspection_c__XelaSensorStream_Response_message_member_array,  // message members
  xela_server_ros2__srv__XelaSensorStream_Response__rosidl_typesupport_introspection_c__XelaSensorStream_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  xela_server_ros2__srv__XelaSensorStream_Response__rosidl_typesupport_introspection_c__XelaSensorStream_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t xela_server_ros2__srv__XelaSensorStream_Response__rosidl_typesupport_introspection_c__XelaSensorStream_Response_message_type_support_handle = {
  0,
  &xela_server_ros2__srv__XelaSensorStream_Response__rosidl_typesupport_introspection_c__XelaSensorStream_Response_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_xela_server_ros2
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, xela_server_ros2, srv, XelaSensorStream_Response)() {
  xela_server_ros2__srv__XelaSensorStream_Response__rosidl_typesupport_introspection_c__XelaSensorStream_Response_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, xela_server_ros2, msg, SensorFull)();
  if (!xela_server_ros2__srv__XelaSensorStream_Response__rosidl_typesupport_introspection_c__XelaSensorStream_Response_message_type_support_handle.typesupport_identifier) {
    xela_server_ros2__srv__XelaSensorStream_Response__rosidl_typesupport_introspection_c__XelaSensorStream_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &xela_server_ros2__srv__XelaSensorStream_Response__rosidl_typesupport_introspection_c__XelaSensorStream_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "xela_server_ros2/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "xela_server_ros2/srv/detail/xela_sensor_stream__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers xela_server_ros2__srv__detail__xela_sensor_stream__rosidl_typesupport_introspection_c__XelaSensorStream_service_members = {
  "xela_server_ros2__srv",  // service namespace
  "XelaSensorStream",  // service name
  // these two fields are initialized below on the first access
  NULL,  // request message
  // xela_server_ros2__srv__detail__xela_sensor_stream__rosidl_typesupport_introspection_c__XelaSensorStream_Request_message_type_support_handle,
  NULL  // response message
  // xela_server_ros2__srv__detail__xela_sensor_stream__rosidl_typesupport_introspection_c__XelaSensorStream_Response_message_type_support_handle
};

static rosidl_service_type_support_t xela_server_ros2__srv__detail__xela_sensor_stream__rosidl_typesupport_introspection_c__XelaSensorStream_service_type_support_handle = {
  0,
  &xela_server_ros2__srv__detail__xela_sensor_stream__rosidl_typesupport_introspection_c__XelaSensorStream_service_members,
  get_service_typesupport_handle_function,
};

// Forward declaration of request/response type support functions
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, xela_server_ros2, srv, XelaSensorStream_Request)();

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, xela_server_ros2, srv, XelaSensorStream_Response)();

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_xela_server_ros2
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, xela_server_ros2, srv, XelaSensorStream)() {
  if (!xela_server_ros2__srv__detail__xela_sensor_stream__rosidl_typesupport_introspection_c__XelaSensorStream_service_type_support_handle.typesupport_identifier) {
    xela_server_ros2__srv__detail__xela_sensor_stream__rosidl_typesupport_introspection_c__XelaSensorStream_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)xela_server_ros2__srv__detail__xela_sensor_stream__rosidl_typesupport_introspection_c__XelaSensorStream_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, xela_server_ros2, srv, XelaSensorStream_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, xela_server_ros2, srv, XelaSensorStream_Response)()->data;
  }

  return &xela_server_ros2__srv__detail__xela_sensor_stream__rosidl_typesupport_introspection_c__XelaSensorStream_service_type_support_handle;
}
