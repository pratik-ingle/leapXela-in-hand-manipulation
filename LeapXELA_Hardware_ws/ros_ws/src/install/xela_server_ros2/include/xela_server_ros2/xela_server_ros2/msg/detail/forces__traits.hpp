// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from xela_server_ros2:msg/Forces.idl
// generated code does not contain a copyright notice

#ifndef XELA_SERVER_ROS2__MSG__DETAIL__FORCES__TRAITS_HPP_
#define XELA_SERVER_ROS2__MSG__DETAIL__FORCES__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "xela_server_ros2/msg/detail/forces__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace xela_server_ros2
{

namespace msg
{

inline void to_flow_style_yaml(
  const Forces & msg,
  std::ostream & out)
{
  out << "{";
  // member: x
  {
    out << "x: ";
    rosidl_generator_traits::value_to_yaml(msg.x, out);
    out << ", ";
  }

  // member: y
  {
    out << "y: ";
    rosidl_generator_traits::value_to_yaml(msg.y, out);
    out << ", ";
  }

  // member: z
  {
    out << "z: ";
    rosidl_generator_traits::value_to_yaml(msg.z, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Forces & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: x
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "x: ";
    rosidl_generator_traits::value_to_yaml(msg.x, out);
    out << "\n";
  }

  // member: y
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "y: ";
    rosidl_generator_traits::value_to_yaml(msg.y, out);
    out << "\n";
  }

  // member: z
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "z: ";
    rosidl_generator_traits::value_to_yaml(msg.z, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Forces & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace xela_server_ros2

namespace rosidl_generator_traits
{

[[deprecated("use xela_server_ros2::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const xela_server_ros2::msg::Forces & msg,
  std::ostream & out, size_t indentation = 0)
{
  xela_server_ros2::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use xela_server_ros2::msg::to_yaml() instead")]]
inline std::string to_yaml(const xela_server_ros2::msg::Forces & msg)
{
  return xela_server_ros2::msg::to_yaml(msg);
}

template<>
inline const char * data_type<xela_server_ros2::msg::Forces>()
{
  return "xela_server_ros2::msg::Forces";
}

template<>
inline const char * name<xela_server_ros2::msg::Forces>()
{
  return "xela_server_ros2/msg/Forces";
}

template<>
struct has_fixed_size<xela_server_ros2::msg::Forces>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<xela_server_ros2::msg::Forces>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<xela_server_ros2::msg::Forces>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // XELA_SERVER_ROS2__MSG__DETAIL__FORCES__TRAITS_HPP_
