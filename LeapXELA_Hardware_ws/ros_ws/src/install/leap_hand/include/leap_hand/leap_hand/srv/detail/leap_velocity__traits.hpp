// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from leap_hand:srv/LeapVelocity.idl
// generated code does not contain a copyright notice

#ifndef LEAP_HAND__SRV__DETAIL__LEAP_VELOCITY__TRAITS_HPP_
#define LEAP_HAND__SRV__DETAIL__LEAP_VELOCITY__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "leap_hand/srv/detail/leap_velocity__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace leap_hand
{

namespace srv
{

inline void to_flow_style_yaml(
  const LeapVelocity_Request & msg,
  std::ostream & out)
{
  (void)msg;
  out << "null";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const LeapVelocity_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  (void)msg;
  (void)indentation;
  out << "null\n";
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const LeapVelocity_Request & msg, bool use_flow_style = false)
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
  const leap_hand::srv::LeapVelocity_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  leap_hand::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use leap_hand::srv::to_yaml() instead")]]
inline std::string to_yaml(const leap_hand::srv::LeapVelocity_Request & msg)
{
  return leap_hand::srv::to_yaml(msg);
}

template<>
inline const char * data_type<leap_hand::srv::LeapVelocity_Request>()
{
  return "leap_hand::srv::LeapVelocity_Request";
}

template<>
inline const char * name<leap_hand::srv::LeapVelocity_Request>()
{
  return "leap_hand/srv/LeapVelocity_Request";
}

template<>
struct has_fixed_size<leap_hand::srv::LeapVelocity_Request>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<leap_hand::srv::LeapVelocity_Request>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<leap_hand::srv::LeapVelocity_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace leap_hand
{

namespace srv
{

inline void to_flow_style_yaml(
  const LeapVelocity_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: velocity
  {
    if (msg.velocity.size() == 0) {
      out << "velocity: []";
    } else {
      out << "velocity: [";
      size_t pending_items = msg.velocity.size();
      for (auto item : msg.velocity) {
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
  const LeapVelocity_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: velocity
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.velocity.size() == 0) {
      out << "velocity: []\n";
    } else {
      out << "velocity:\n";
      for (auto item : msg.velocity) {
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

inline std::string to_yaml(const LeapVelocity_Response & msg, bool use_flow_style = false)
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
  const leap_hand::srv::LeapVelocity_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  leap_hand::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use leap_hand::srv::to_yaml() instead")]]
inline std::string to_yaml(const leap_hand::srv::LeapVelocity_Response & msg)
{
  return leap_hand::srv::to_yaml(msg);
}

template<>
inline const char * data_type<leap_hand::srv::LeapVelocity_Response>()
{
  return "leap_hand::srv::LeapVelocity_Response";
}

template<>
inline const char * name<leap_hand::srv::LeapVelocity_Response>()
{
  return "leap_hand/srv/LeapVelocity_Response";
}

template<>
struct has_fixed_size<leap_hand::srv::LeapVelocity_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<leap_hand::srv::LeapVelocity_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<leap_hand::srv::LeapVelocity_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<leap_hand::srv::LeapVelocity>()
{
  return "leap_hand::srv::LeapVelocity";
}

template<>
inline const char * name<leap_hand::srv::LeapVelocity>()
{
  return "leap_hand/srv/LeapVelocity";
}

template<>
struct has_fixed_size<leap_hand::srv::LeapVelocity>
  : std::integral_constant<
    bool,
    has_fixed_size<leap_hand::srv::LeapVelocity_Request>::value &&
    has_fixed_size<leap_hand::srv::LeapVelocity_Response>::value
  >
{
};

template<>
struct has_bounded_size<leap_hand::srv::LeapVelocity>
  : std::integral_constant<
    bool,
    has_bounded_size<leap_hand::srv::LeapVelocity_Request>::value &&
    has_bounded_size<leap_hand::srv::LeapVelocity_Response>::value
  >
{
};

template<>
struct is_service<leap_hand::srv::LeapVelocity>
  : std::true_type
{
};

template<>
struct is_service_request<leap_hand::srv::LeapVelocity_Request>
  : std::true_type
{
};

template<>
struct is_service_response<leap_hand::srv::LeapVelocity_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // LEAP_HAND__SRV__DETAIL__LEAP_VELOCITY__TRAITS_HPP_
