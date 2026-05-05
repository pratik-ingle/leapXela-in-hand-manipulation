// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from xela_server_ros2:msg/SensStream.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "xela_server_ros2/msg/detail/sens_stream__rosidl_typesupport_introspection_c.h"
#include "xela_server_ros2/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "xela_server_ros2/msg/detail/sens_stream__functions.h"
#include "xela_server_ros2/msg/detail/sens_stream__struct.h"


// Include directives for member types
// Member `sensors`
#include "xela_server_ros2/msg/sensor_full.h"
// Member `sensors`
#include "xela_server_ros2/msg/detail/sensor_full__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void xela_server_ros2__msg__SensStream__rosidl_typesupport_introspection_c__SensStream_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  xela_server_ros2__msg__SensStream__init(message_memory);
}

void xela_server_ros2__msg__SensStream__rosidl_typesupport_introspection_c__SensStream_fini_function(void * message_memory)
{
  xela_server_ros2__msg__SensStream__fini(message_memory);
}

size_t xela_server_ros2__msg__SensStream__rosidl_typesupport_introspection_c__size_function__SensStream__sensors(
  const void * untyped_member)
{
  const xela_server_ros2__msg__SensorFull__Sequence * member =
    (const xela_server_ros2__msg__SensorFull__Sequence *)(untyped_member);
  return member->size;
}

const void * xela_server_ros2__msg__SensStream__rosidl_typesupport_introspection_c__get_const_function__SensStream__sensors(
  const void * untyped_member, size_t index)
{
  const xela_server_ros2__msg__SensorFull__Sequence * member =
    (const xela_server_ros2__msg__SensorFull__Sequence *)(untyped_member);
  return &member->data[index];
}

void * xela_server_ros2__msg__SensStream__rosidl_typesupport_introspection_c__get_function__SensStream__sensors(
  void * untyped_member, size_t index)
{
  xela_server_ros2__msg__SensorFull__Sequence * member =
    (xela_server_ros2__msg__SensorFull__Sequence *)(untyped_member);
  return &member->data[index];
}

void xela_server_ros2__msg__SensStream__rosidl_typesupport_introspection_c__fetch_function__SensStream__sensors(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const xela_server_ros2__msg__SensorFull * item =
    ((const xela_server_ros2__msg__SensorFull *)
    xela_server_ros2__msg__SensStream__rosidl_typesupport_introspection_c__get_const_function__SensStream__sensors(untyped_member, index));
  xela_server_ros2__msg__SensorFull * value =
    (xela_server_ros2__msg__SensorFull *)(untyped_value);
  *value = *item;
}

void xela_server_ros2__msg__SensStream__rosidl_typesupport_introspection_c__assign_function__SensStream__sensors(
  void * untyped_member, size_t index, const void * untyped_value)
{
  xela_server_ros2__msg__SensorFull * item =
    ((xela_server_ros2__msg__SensorFull *)
    xela_server_ros2__msg__SensStream__rosidl_typesupport_introspection_c__get_function__SensStream__sensors(untyped_member, index));
  const xela_server_ros2__msg__SensorFull * value =
    (const xela_server_ros2__msg__SensorFull *)(untyped_value);
  *item = *value;
}

bool xela_server_ros2__msg__SensStream__rosidl_typesupport_introspection_c__resize_function__SensStream__sensors(
  void * untyped_member, size_t size)
{
  xela_server_ros2__msg__SensorFull__Sequence * member =
    (xela_server_ros2__msg__SensorFull__Sequence *)(untyped_member);
  xela_server_ros2__msg__SensorFull__Sequence__fini(member);
  return xela_server_ros2__msg__SensorFull__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember xela_server_ros2__msg__SensStream__rosidl_typesupport_introspection_c__SensStream_message_member_array[1] = {
  {
    "sensors",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(xela_server_ros2__msg__SensStream, sensors),  // bytes offset in struct
    NULL,  // default value
    xela_server_ros2__msg__SensStream__rosidl_typesupport_introspection_c__size_function__SensStream__sensors,  // size() function pointer
    xela_server_ros2__msg__SensStream__rosidl_typesupport_introspection_c__get_const_function__SensStream__sensors,  // get_const(index) function pointer
    xela_server_ros2__msg__SensStream__rosidl_typesupport_introspection_c__get_function__SensStream__sensors,  // get(index) function pointer
    xela_server_ros2__msg__SensStream__rosidl_typesupport_introspection_c__fetch_function__SensStream__sensors,  // fetch(index, &value) function pointer
    xela_server_ros2__msg__SensStream__rosidl_typesupport_introspection_c__assign_function__SensStream__sensors,  // assign(index, value) function pointer
    xela_server_ros2__msg__SensStream__rosidl_typesupport_introspection_c__resize_function__SensStream__sensors  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers xela_server_ros2__msg__SensStream__rosidl_typesupport_introspection_c__SensStream_message_members = {
  "xela_server_ros2__msg",  // message namespace
  "SensStream",  // message name
  1,  // number of fields
  sizeof(xela_server_ros2__msg__SensStream),
  xela_server_ros2__msg__SensStream__rosidl_typesupport_introspection_c__SensStream_message_member_array,  // message members
  xela_server_ros2__msg__SensStream__rosidl_typesupport_introspection_c__SensStream_init_function,  // function to initialize message memory (memory has to be allocated)
  xela_server_ros2__msg__SensStream__rosidl_typesupport_introspection_c__SensStream_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t xela_server_ros2__msg__SensStream__rosidl_typesupport_introspection_c__SensStream_message_type_support_handle = {
  0,
  &xela_server_ros2__msg__SensStream__rosidl_typesupport_introspection_c__SensStream_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_xela_server_ros2
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, xela_server_ros2, msg, SensStream)() {
  xela_server_ros2__msg__SensStream__rosidl_typesupport_introspection_c__SensStream_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, xela_server_ros2, msg, SensorFull)();
  if (!xela_server_ros2__msg__SensStream__rosidl_typesupport_introspection_c__SensStream_message_type_support_handle.typesupport_identifier) {
    xela_server_ros2__msg__SensStream__rosidl_typesupport_introspection_c__SensStream_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &xela_server_ros2__msg__SensStream__rosidl_typesupport_introspection_c__SensStream_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
