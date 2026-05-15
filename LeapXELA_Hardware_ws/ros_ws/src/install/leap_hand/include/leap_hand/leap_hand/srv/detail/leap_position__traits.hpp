// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from leap_hand:srv/LeapPosition.idl
// generated code does not contain a copyright notice

#ifndef LEAP_HAND__SRV__DETAIL__LEAP_POSITION__TRAITS_HPP_
#define LEAP_HAND__SRV__DETAIL__LEAP_POSITION__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "leap_hand/srv/detail/leap_position__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace leap_hand
{

namespace srv
{

inline void to_flow_style_yaml(
  const LeapPosition_Request & msg,
  std::ostream & out)
{
  (void)msg;
  out << "null";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const LeapPosition_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  (void)msg;
  (void)indentation;
  out << "null\n";
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const LeapPosition_Request & msg, bool use_flow_style = false)
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

}  // namespace leap_hand

namespace rosidl_generator_traits
{

[[deprecated("use leap_hand::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const leap_hand::srv::LeapPosition_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  leap_hand::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use leap_hand::srv::to_yaml() instead")]]
inline std::string to_yaml(const leap_hand::srv::LeapPosition_Request & msg)
{
  return leap_hand::srv::to_yaml(msg);
}

template<>
inline const char * data_type<leap_hand::srv::LeapPosition_Request>()
{
  return "leap_hand::srv::LeapPosition_Request";
}

template<>
inline const char * name<leap_hand::srv::LeapPosition_Request>()
{
  return "leap_hand/srv/LeapPosition_Request";
}

template<>
struct has_fixed_size<leap_hand::srv::LeapPosition_Request>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<leap_hand::srv::LeapPosition_Request>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<leap_hand::srv::LeapPosition_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace leap_hand
{

namespace srv
{

inline void to_flow_style_yaml(
  const LeapPosition_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: position
  {
    if (msg.position.size() == 0) {
      out << "position: []";
    } else {
      out << "position: [";
      size_t pending_items = msg.position.size();
      for (auto item : msg.position) {
        rosidl_generator_traits::value_to_yaml(item, out);
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
  const LeapPosition_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: position
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.position.size() == 0) {
      out << "position: []\n";
    } else {
      out << "position:\n";
      for (auto item : msg.position) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const LeapPosition_Response & msg, bool use_flow_style = false)
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

}  // namespace leap_hand

namespace rosidl_generator_traits
{

[[deprecated("use leap_hand::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const leap_hand::srv::LeapPosition_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  leap_hand::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use leap_hand::srv::to_yaml() instead")]]
inline std::string to_yaml(const leap_hand::srv::LeapPosition_Response & msg)
{
  return leap_hand::srv::to_yaml(msg);
}

template<>
inline const char * data_type<leap_hand::srv::LeapPosition_Response>()
{
  return "leap_hand::srv::LeapPosition_Response";
}

template<>
inline const char * name<leap_hand::srv::LeapPosition_Response>()
{
  return "leap_hand/srv/LeapPosition_Response";
}

template<>
struct has_fixed_size<leap_hand::srv::LeapPosition_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<leap_hand::srv::LeapPosition_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<leap_hand::srv::LeapPosition_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<leap_hand::srv::LeapPosition>()
{
  return "leap_hand::srv::LeapPosition";
}

template<>
inline const char * name<leap_hand::srv::LeapPosition>()
{
  return "leap_hand/srv/LeapPosition";
}

template<>
struct has_fixed_size<leap_hand::srv::LeapPosition>
  : std::integral_constant<
    bool,
    has_fixed_size<leap_hand::srv::LeapPosition_Request>::value &&
    has_fixed_size<leap_hand::srv::LeapPosition_Response>::value
  >
{
};

template<>
struct has_bounded_size<leap_hand::srv::LeapPosition>
  : std::integral_constant<
    bool,
    has_bounded_size<leap_hand::srv::LeapPosition_Request>::value &&
    has_bounded_size<leap_hand::srv::LeapPosition_Response>::value
  >
{
};

template<>
struct is_service<leap_hand::srv::LeapPosition>
  : std::true_type
{
};

template<>
struct is_service_request<leap_hand::srv::LeapPosition_Request>
  : std::true_type
{
};

template<>
struct is_service_response<leap_hand::srv::LeapPosition_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // LEAP_HAND__SRV__DETAIL__LEAP_POSITION__TRAITS_HPP_
