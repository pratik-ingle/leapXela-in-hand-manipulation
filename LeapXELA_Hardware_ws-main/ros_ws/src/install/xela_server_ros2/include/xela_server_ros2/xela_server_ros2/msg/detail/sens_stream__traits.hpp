// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from xela_server_ros2:msg/SensStream.idl
// generated code does not contain a copyright notice

#ifndef XELA_SERVER_ROS2__MSG__DETAIL__SENS_STREAM__TRAITS_HPP_
#define XELA_SERVER_ROS2__MSG__DETAIL__SENS_STREAM__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "xela_server_ros2/msg/detail/sens_stream__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'sensors'
#include "xela_server_ros2/msg/detail/sensor_full__traits.hpp"

namespace xela_server_ros2
{

namespace msg
{

inline void to_flow_style_yaml(
  const SensStream & msg,
  std::ostream & out)
{
  out << "{";
  // member: sensors
  {
    if (msg.sensors.size() == 0) {
      out << "sensors: []";
    } else {
      out << "sensors: [";
      size_t pending_items = msg.sensors.size();
      for (auto item : msg.sensors) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const SensStream & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: sensors
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.sensors.size() == 0) {
      out << "sensors: []\n";
    } else {
      out << "sensors:\n";
      for (auto item : msg.sensors) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const SensStream & msg, bool use_flow_style = false)
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
  const xela_server_ros2::msg::SensStream & msg,
  std::ostream & out, size_t indentation = 0)
{
  xela_server_ros2::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use xela_server_ros2::msg::to_yaml() instead")]]
inline std::string to_yaml(const xela_server_ros2::msg::SensStream & msg)
{
  return xela_server_ros2::msg::to_yaml(msg);
}

template<>
inline const char * data_type<xela_server_ros2::msg::SensStream>()
{
  return "xela_server_ros2::msg::SensStream";
}

template<>
inline const char * name<xela_server_ros2::msg::SensStream>()
{
  return "xela_server_ros2/msg/SensStream";
}

template<>
struct has_fixed_size<xela_server_ros2::msg::SensStream>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<xela_server_ros2::msg::SensStream>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<xela_server_ros2::msg::SensStream>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // XELA_SERVER_ROS2__MSG__DETAIL__SENS_STREAM__TRAITS_HPP_
