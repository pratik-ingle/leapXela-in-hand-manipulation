// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from xela_server_ros2:msg/SensorFull.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "xela_server_ros2/msg/detail/sensor_full__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace xela_server_ros2
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void SensorFull_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) xela_server_ros2::msg::SensorFull(_init);
}

void SensorFull_fini_function(void * message_memory)
{
  auto typed_message = static_cast<xela_server_ros2::msg::SensorFull *>(message_memory);
  typed_message->~SensorFull();
}

size_t size_function__SensorFull__taxels(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<xela_server_ros2::msg::Taxel> *>(untyped_member);
  return member->size();
}

const void * get_const_function__SensorFull__taxels(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<xela_server_ros2::msg::Taxel> *>(untyped_member);
  return &member[index];
}

void * get_function__SensorFull__taxels(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<xela_server_ros2::msg::Taxel> *>(untyped_member);
  return &member[index];
}

void fetch_function__SensorFull__taxels(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const xela_server_ros2::msg::Taxel *>(
    get_const_function__SensorFull__taxels(untyped_member, index));
  auto & value = *reinterpret_cast<xela_server_ros2::msg::Taxel *>(untyped_value);
  value = item;
}

void assign_function__SensorFull__taxels(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<xela_server_ros2::msg::Taxel *>(
    get_function__SensorFull__taxels(untyped_member, index));
  const auto & value = *reinterpret_cast<const xela_server_ros2::msg::Taxel *>(untyped_value);
  item = value;
}

void resize_function__SensorFull__taxels(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<xela_server_ros2::msg::Taxel> *>(untyped_member);
  member->resize(size);
}

size_t size_function__SensorFull__forces(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<xela_server_ros2::msg::Forces> *>(untyped_member);
  return member->size();
}

const void * get_const_function__SensorFull__forces(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<xela_server_ros2::msg::Forces> *>(untyped_member);
  return &member[index];
}

void * get_function__SensorFull__forces(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<xela_server_ros2::msg::Forces> *>(untyped_member);
  return &member[index];
}

void fetch_function__SensorFull__forces(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const xela_server_ros2::msg::Forces *>(
    get_const_function__SensorFull__forces(untyped_member, index));
  auto & value = *reinterpret_cast<xela_server_ros2::msg::Forces *>(untyped_value);
  value = item;
}

void assign_function__SensorFull__forces(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<xela_server_ros2::msg::Forces *>(
    get_function__SensorFull__forces(untyped_member, index));
  const auto & value = *reinterpret_cast<const xela_server_ros2::msg::Forces *>(untyped_value);
  item = value;
}

void resize_function__SensorFull__forces(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<xela_server_ros2::msg::Forces> *>(untyped_member);
  member->resize(size);
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember SensorFull_message_member_array[6] = {
  {
    "message",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_UINT32,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(xela_server_ros2::msg::SensorFull, message),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "time",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(xela_server_ros2::msg::SensorFull, time),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "model",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(xela_server_ros2::msg::SensorFull, model),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "sensor_pos",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(xela_server_ros2::msg::SensorFull, sensor_pos),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "taxels",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<xela_server_ros2::msg::Taxel>(),  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(xela_server_ros2::msg::SensorFull, taxels),  // bytes offset in struct
    nullptr,  // default value
    size_function__SensorFull__taxels,  // size() function pointer
    get_const_function__SensorFull__taxels,  // get_const(index) function pointer
    get_function__SensorFull__taxels,  // get(index) function pointer
    fetch_function__SensorFull__taxels,  // fetch(index, &value) function pointer
    assign_function__SensorFull__taxels,  // assign(index, value) function pointer
    resize_function__SensorFull__taxels  // resize(index) function pointer
  },
  {
    "forces",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<xela_server_ros2::msg::Forces>(),  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(xela_server_ros2::msg::SensorFull, forces),  // bytes offset in struct
    nullptr,  // default value
    size_function__SensorFull__forces,  // size() function pointer
    get_const_function__SensorFull__forces,  // get_const(index) function pointer
    get_function__SensorFull__forces,  // get(index) function pointer
    fetch_function__SensorFull__forces,  // fetch(index, &value) function pointer
    assign_function__SensorFull__forces,  // assign(index, value) function pointer
    resize_function__SensorFull__forces  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers SensorFull_message_members = {
  "xela_server_ros2::msg",  // message namespace
  "SensorFull",  // message name
  6,  // number of fields
  sizeof(xela_server_ros2::msg::SensorFull),
  SensorFull_message_member_array,  // message members
  SensorFull_init_function,  // function to initialize message memory (memory has to be allocated)
  SensorFull_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t SensorFull_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &SensorFull_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace xela_server_ros2


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<xela_server_ros2::msg::SensorFull>()
{
  return &::xela_server_ros2::msg::rosidl_typesupport_introspection_cpp::SensorFull_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, xela_server_ros2, msg, SensorFull)() {
  return &::xela_server_ros2::msg::rosidl_typesupport_introspection_cpp::SensorFull_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
