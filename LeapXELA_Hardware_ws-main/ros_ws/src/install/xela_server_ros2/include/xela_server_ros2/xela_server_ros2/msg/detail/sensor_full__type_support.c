// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from xela_server_ros2:msg/SensorFull.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "xela_server_ros2/msg/detail/sensor_full__rosidl_typesupport_introspection_c.h"
#include "xela_server_ros2/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "xela_server_ros2/msg/detail/sensor_full__functions.h"
#include "xela_server_ros2/msg/detail/sensor_full__struct.h"


// Include directives for member types
// Member `model`
#include "rosidl_runtime_c/string_functions.h"
// Member `taxels`
#include "xela_server_ros2/msg/taxel.h"
// Member `taxels`
#include "xela_server_ros2/msg/detail/taxel__rosidl_typesupport_introspection_c.h"
// Member `forces`
#include "xela_server_ros2/msg/forces.h"
// Member `forces`
#include "xela_server_ros2/msg/detail/forces__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void xela_server_ros2__msg__SensorFull__rosidl_typesupport_introspection_c__SensorFull_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  xela_server_ros2__msg__SensorFull__init(message_memory);
}

void xela_server_ros2__msg__SensorFull__rosidl_typesupport_introspection_c__SensorFull_fini_function(void * message_memory)
{
  xela_server_ros2__msg__SensorFull__fini(message_memory);
}

size_t xela_server_ros2__msg__SensorFull__rosidl_typesupport_introspection_c__size_function__SensorFull__taxels(
  const void * untyped_member)
{
  const xela_server_ros2__msg__Taxel__Sequence * member =
    (const xela_server_ros2__msg__Taxel__Sequence *)(untyped_member);
  return member->size;
}

const void * xela_server_ros2__msg__SensorFull__rosidl_typesupport_introspection_c__get_const_function__SensorFull__taxels(
  const void * untyped_member, size_t index)
{
  const xela_server_ros2__msg__Taxel__Sequence * member =
    (const xela_server_ros2__msg__Taxel__Sequence *)(untyped_member);
  return &member->data[index];
}

void * xela_server_ros2__msg__SensorFull__rosidl_typesupport_introspection_c__get_function__SensorFull__taxels(
  void * untyped_member, size_t index)
{
  xela_server_ros2__msg__Taxel__Sequence * member =
    (xela_server_ros2__msg__Taxel__Sequence *)(untyped_member);
  return &member->data[index];
}

void xela_server_ros2__msg__SensorFull__rosidl_typesupport_introspection_c__fetch_function__SensorFull__taxels(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const xela_server_ros2__msg__Taxel * item =
    ((const xela_server_ros2__msg__Taxel *)
    xela_server_ros2__msg__SensorFull__rosidl_typesupport_introspection_c__get_const_function__SensorFull__taxels(untyped_member, index));
  xela_server_ros2__msg__Taxel * value =
    (xela_server_ros2__msg__Taxel *)(untyped_value);
  *value = *item;
}

void xela_server_ros2__msg__SensorFull__rosidl_typesupport_introspection_c__assign_function__SensorFull__taxels(
  void * untyped_member, size_t index, const void * untyped_value)
{
  xela_server_ros2__msg__Taxel * item =
    ((xela_server_ros2__msg__Taxel *)
    xela_server_ros2__msg__SensorFull__rosidl_typesupport_introspection_c__get_function__SensorFull__taxels(untyped_member, index));
  const xela_server_ros2__msg__Taxel * value =
    (const xela_server_ros2__msg__Taxel *)(untyped_value);
  *item = *value;
}

bool xela_server_ros2__msg__SensorFull__rosidl_typesupport_introspection_c__resize_function__SensorFull__taxels(
  void * untyped_member, size_t size)
{
  xela_server_ros2__msg__Taxel__Sequence * member =
    (xela_server_ros2__msg__Taxel__Sequence *)(untyped_member);
  xela_server_ros2__msg__Taxel__Sequence__fini(member);
  return xela_server_ros2__msg__Taxel__Sequence__init(member, size);
}

size_t xela_server_ros2__msg__SensorFull__rosidl_typesupport_introspection_c__size_function__SensorFull__forces(
  const void * untyped_member)
{
  const xela_server_ros2__msg__Forces__Sequence * member =
    (const xela_server_ros2__msg__Forces__Sequence *)(untyped_member);
  return member->size;
}

const void * xela_server_ros2__msg__SensorFull__rosidl_typesupport_introspection_c__get_const_function__SensorFull__forces(
  const void * untyped_member, size_t index)
{
  const xela_server_ros2__msg__Forces__Sequence * member =
    (const xela_server_ros2__msg__Forces__Sequence *)(untyped_member);
  return &member->data[index];
}

void * xela_server_ros2__msg__SensorFull__rosidl_typesupport_introspection_c__get_function__SensorFull__forces(
  void * untyped_member, size_t index)
{
  xela_server_ros2__msg__Forces__Sequence * member =
    (xela_server_ros2__msg__Forces__Sequence *)(untyped_member);
  return &member->data[index];
}

void xela_server_ros2__msg__SensorFull__rosidl_typesupport_introspection_c__fetch_function__SensorFull__forces(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const xela_server_ros2__msg__Forces * item =
    ((const xela_server_ros2__msg__Forces *)
    xela_server_ros2__msg__SensorFull__rosidl_typesupport_introspection_c__get_const_function__SensorFull__forces(untyped_member, index));
  xela_server_ros2__msg__Forces * value =
    (xela_server_ros2__msg__Forces *)(untyped_value);
  *value = *item;
}

void xela_server_ros2__msg__SensorFull__rosidl_typesupport_introspection_c__assign_function__SensorFull__forces(
  void * untyped_member, size_t index, const void * untyped_value)
{
  xela_server_ros2__msg__Forces * item =
    ((xela_server_ros2__msg__Forces *)
    xela_server_ros2__msg__SensorFull__rosidl_typesupport_introspection_c__get_function__SensorFull__forces(untyped_member, index));
  const xela_server_ros2__msg__Forces * value =
    (const xela_server_ros2__msg__Forces *)(untyped_value);
  *item = *value;
}

bool xela_server_ros2__msg__SensorFull__rosidl_typesupport_introspection_c__resize_function__SensorFull__forces(
  void * untyped_member, size_t size)
{
  xela_server_ros2__msg__Forces__Sequence * member =
    (xela_server_ros2__msg__Forces__Sequence *)(untyped_member);
  xela_server_ros2__msg__Forces__Sequence__fini(member);
  return xela_server_ros2__msg__Forces__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember xela_server_ros2__msg__SensorFull__rosidl_typesupport_introspection_c__SensorFull_message_member_array[6] = {
  {
    "message",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(xela_server_ros2__msg__SensorFull, message),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "time",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(xela_server_ros2__msg__SensorFull, time),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "model",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(xela_server_ros2__msg__SensorFull, model),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "sensor_pos",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(xela_server_ros2__msg__SensorFull, sensor_pos),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "taxels",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(xela_server_ros2__msg__SensorFull, taxels),  // bytes offset in struct
    NULL,  // default value
    xela_server_ros2__msg__SensorFull__rosidl_typesupport_introspection_c__size_function__SensorFull__taxels,  // size() function pointer
    xela_server_ros2__msg__SensorFull__rosidl_typesupport_introspection_c__get_const_function__SensorFull__taxels,  // get_const(index) function pointer
    xela_server_ros2__msg__SensorFull__rosidl_typesupport_introspection_c__get_function__SensorFull__taxels,  // get(index) function pointer
    xela_server_ros2__msg__SensorFull__rosidl_typesupport_introspection_c__fetch_function__SensorFull__taxels,  // fetch(index, &value) function pointer
    xela_server_ros2__msg__SensorFull__rosidl_typesupport_introspection_c__assign_function__SensorFull__taxels,  // assign(index, value) function pointer
    xela_server_ros2__msg__SensorFull__rosidl_typesupport_introspection_c__resize_function__SensorFull__taxels  // resize(index) function pointer
  },
  {
    "forces",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(xela_server_ros2__msg__SensorFull, forces),  // bytes offset in struct
    NULL,  // default value
    xela_server_ros2__msg__SensorFull__rosidl_typesupport_introspection_c__size_function__SensorFull__forces,  // size() function pointer
    xela_server_ros2__msg__SensorFull__rosidl_typesupport_introspection_c__get_const_function__SensorFull__forces,  // get_const(index) function pointer
    xela_server_ros2__msg__SensorFull__rosidl_typesupport_introspection_c__get_function__SensorFull__forces,  // get(index) function pointer
    xela_server_ros2__msg__SensorFull__rosidl_typesupport_introspection_c__fetch_function__SensorFull__forces,  // fetch(index, &value) function pointer
    xela_server_ros2__msg__SensorFull__rosidl_typesupport_introspection_c__assign_function__SensorFull__forces,  // assign(index, value) function pointer
    xela_server_ros2__msg__SensorFull__rosidl_typesupport_introspection_c__resize_function__SensorFull__forces  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers xela_server_ros2__msg__SensorFull__rosidl_typesupport_introspection_c__SensorFull_message_members = {
  "xela_server_ros2__msg",  // message namespace
  "SensorFull",  // message name
  6,  // number of fields
  sizeof(xela_server_ros2__msg__SensorFull),
  xela_server_ros2__msg__SensorFull__rosidl_typesupport_introspection_c__SensorFull_message_member_array,  // message members
  xela_server_ros2__msg__SensorFull__rosidl_typesupport_introspection_c__SensorFull_init_function,  // function to initialize message memory (memory has to be allocated)
  xela_server_ros2__msg__SensorFull__rosidl_typesupport_introspection_c__SensorFull_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t xela_server_ros2__msg__SensorFull__rosidl_typesupport_introspection_c__SensorFull_message_type_support_handle = {
  0,
  &xela_server_ros2__msg__SensorFull__rosidl_typesupport_introspection_c__SensorFull_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_xela_server_ros2
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, xela_server_ros2, msg, SensorFull)() {
  xela_server_ros2__msg__SensorFull__rosidl_typesupport_introspection_c__SensorFull_message_member_array[4].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, xela_server_ros2, msg, Taxel)();
  xela_server_ros2__msg__SensorFull__rosidl_typesupport_introspection_c__SensorFull_message_member_array[5].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, xela_server_ros2, msg, Forces)();
  if (!xela_server_ros2__msg__SensorFull__rosidl_typesupport_introspection_c__SensorFull_message_type_support_handle.typesupport_identifier) {
    xela_server_ros2__msg__SensorFull__rosidl_typesupport_introspection_c__SensorFull_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &xela_server_ros2__msg__SensorFull__rosidl_typesupport_introspection_c__SensorFull_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
