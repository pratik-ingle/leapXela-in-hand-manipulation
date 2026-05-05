// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from xela_server_ros2:msg/SensorFull.idl
// generated code does not contain a copyright notice

#ifndef XELA_SERVER_ROS2__MSG__DETAIL__SENSOR_FULL__TRAITS_HPP_
#define XELA_SERVER_ROS2__MSG__DETAIL__SENSOR_FULL__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "xela_server_ros2/msg/detail/sensor_full__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'taxels'
#include "xela_server_ros2/msg/detail/taxel__traits.hpp"
// Member 'forces'
#include "xela_server_ros2/msg/detail/forces__traits.hpp"

namespace xela_server_ros2
{

namespace msg
{

inline void to_flow_style_yaml(
  const SensorFull & msg,
  std::ostream & out)
{
  out << "{";
  // member: message
  {
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
    out << ", ";
  }

  // member: time
  {
    out << "time: ";
    rosidl_generator_traits::value_to_yaml(msg.time, out);
    out << ", ";
  }

  // member: model
  {
    out << "model: ";
    rosidl_generator_traits::value_to_yaml(msg.model, out);
    out << ", ";
  }

  // member: sensor_pos
  {
    out << "sensor_pos: ";
    rosidl_generator_traits::value_to_yaml(msg.sensor_pos, out);
    out << ", ";
  }

  // member: taxels
  {
    if (msg.taxels.size() == 0) {
      out << "taxels: []";
    } else {
      out << "taxels: [";
      size_t pending_items = msg.taxels.size();
      for (auto item : msg.taxels) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: forces
  {
    if (msg.forces.size() == 0) {
      out << "forces: []";
    } else {
      out << "forces: [";
      size_t pending_items = msg.forces.size();
      for (auto item : msg.forces) {
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
  const SensorFull & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: message
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
    out << "\n";
  }

  // member: time
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "time: ";
    rosidl_generator_traits::value_to_yaml(msg.time, out);
    out << "\n";
  }

  // member: model
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "model: ";
    rosidl_generator_traits::value_to_yaml(msg.model, out);
    out << "\n";
  }

  // member: sensor_pos
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "sensor_pos: ";
    rosidl_generator_traits::value_to_yaml(msg.sensor_pos, out);
    out << "\n";
  }

  // member: taxels
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.taxels.size() == 0) {
      out << "taxels: []\n";
    } else {
      out << "taxels:\n";
      for (auto item : msg.taxels) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }

  // member: forces
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.forces.size() == 0) {
      out << "forces: []\n";
    } else {
      out << "forces:\n";
      for (auto item : msg.forces) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const SensorFull & msg, bool use_flow_style = false)
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
  const xela_server_ros2::msg::SensorFull & msg,
  std::ostream & out, size_t indentation = 0)
{
  xela_server_ros2::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use xela_server_ros2::msg::to_yaml() instead")]]
inline std::string to_yaml(const xela_server_ros2::msg::SensorFull & msg)
{
  return xela_server_ros2::msg::to_yaml(msg);
}

template<>
inline const char * data_type<xela_server_ros2::msg::SensorFull>()
{
  return "xela_server_ros2::msg::SensorFull";
}

template<>
inline const char * name<xela_server_ros2::msg::SensorFull>()
{
  return "xela_server_ros2/msg/SensorFull";
}

template<>
struct has_fixed_size<xela_server_ros2::msg::SensorFull>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<xela_server_ros2::msg::SensorFull>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<xela_server_ros2::msg::SensorFull>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // XELA_SERVER_ROS2__MSG__DETAIL__SENSOR_FULL__TRAITS_HPP_
