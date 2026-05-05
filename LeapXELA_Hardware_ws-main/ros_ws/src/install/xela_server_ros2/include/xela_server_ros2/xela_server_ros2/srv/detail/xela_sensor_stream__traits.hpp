// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from xela_server_ros2:srv/XelaSensorStream.idl
// generated code does not contain a copyright notice

#ifndef XELA_SERVER_ROS2__SRV__DETAIL__XELA_SENSOR_STREAM__TRAITS_HPP_
#define XELA_SERVER_ROS2__SRV__DETAIL__XELA_SENSOR_STREAM__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "xela_server_ros2/srv/detail/xela_sensor_stream__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace xela_server_ros2
{

namespace srv
{

inline void to_flow_style_yaml(
  const XelaSensorStream_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: sensor
  {
    out << "sensor: ";
    rosidl_generator_traits::value_to_yaml(msg.sensor, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const XelaSensorStream_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: sensor
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "sensor: ";
    rosidl_generator_traits::value_to_yaml(msg.sensor, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const XelaSensorStream_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace xela_server_ros2

namespace rosidl_generator_traits
{

[[deprecated("use xela_server_ros2::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const xela_server_ros2::srv::XelaSensorStream_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  xela_server_ros2::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use xela_server_ros2::srv::to_yaml() instead")]]
inline std::string to_yaml(const xela_server_ros2::srv::XelaSensorStream_Request & msg)
{
  return xela_server_ros2::srv::to_yaml(msg);
}

template<>
inline const char * data_type<xela_server_ros2::srv::XelaSensorStream_Request>()
{
  return "xela_server_ros2::srv::XelaSensorStream_Request";
}

template<>
inline const char * name<xela_server_ros2::srv::XelaSensorStream_Request>()
{
  return "xela_server_ros2/srv/XelaSensorStream_Request";
}

template<>
struct has_fixed_size<xela_server_ros2::srv::XelaSensorStream_Request>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<xela_server_ros2::srv::XelaSensorStream_Request>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<xela_server_ros2::srv::XelaSensorStream_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'data'
#include "xela_server_ros2/msg/detail/sensor_full__traits.hpp"

namespace xela_server_ros2
{

namespace srv
{

inline void to_flow_style_yaml(
  const XelaSensorStream_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: data
  {
    if (msg.data.size() == 0) {
      out << "data: []";
    } else {
      out << "data: [";
      size_t pending_items = msg.data.size();
      for (auto item : msg.data) {
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
  const XelaSensorStream_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: data
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.data.size() == 0) {
      out << "data: []\n";
    } else {
      out << "data:\n";
      for (auto item : msg.data) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const XelaSensorStream_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace xela_server_ros2

namespace rosidl_generator_traits
{

[[deprecated("use xela_server_ros2::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const xela_server_ros2::srv::XelaSensorStream_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  xela_server_ros2::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use xela_server_ros2::srv::to_yaml() instead")]]
inline std::string to_yaml(const xela_server_ros2::srv::XelaSensorStream_Response & msg)
{
  return xela_server_ros2::srv::to_yaml(msg);
}

template<>
inline const char * data_type<xela_server_ros2::srv::XelaSensorStream_Response>()
{
  return "xela_server_ros2::srv::XelaSensorStream_Response";
}

template<>
inline const char * name<xela_server_ros2::srv::XelaSensorStream_Response>()
{
  return "xela_server_ros2/srv/XelaSensorStream_Response";
}

template<>
struct has_fixed_size<xela_server_ros2::srv::XelaSensorStream_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<xela_server_ros2::srv::XelaSensorStream_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<xela_server_ros2::srv::XelaSensorStream_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<xela_server_ros2::srv::XelaSensorStream>()
{
  return "xela_server_ros2::srv::XelaSensorStream";
}

template<>
inline const char * name<xela_server_ros2::srv::XelaSensorStream>()
{
  return "xela_server_ros2/srv/XelaSensorStream";
}

template<>
struct has_fixed_size<xela_server_ros2::srv::XelaSensorStream>
  : std::integral_constant<
    bool,
    has_fixed_size<xela_server_ros2::srv::XelaSensorStream_Request>::value &&
    has_fixed_size<xela_server_ros2::srv::XelaSensorStream_Response>::value
  >
{
};

template<>
struct has_bounded_size<xela_server_ros2::srv::XelaSensorStream>
  : std::integral_constant<
    bool,
    has_bounded_size<xela_server_ros2::srv::XelaSensorStream_Request>::value &&
    has_bounded_size<xela_server_ros2::srv::XelaSensorStream_Response>::value
  >
{
};

template<>
struct is_service<xela_server_ros2::srv::XelaSensorStream>
  : std::true_type
{
};

template<>
struct is_service_request<xela_server_ros2::srv::XelaSensorStream_Request>
  : std::true_type
{
};

template<>
struct is_service_response<xela_server_ros2::srv::XelaSensorStream_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // XELA_SERVER_ROS2__SRV__DETAIL__XELA_SENSOR_STREAM__TRAITS_HPP_
