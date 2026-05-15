// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from leap_hand:srv/LeapVelocity.idl
// generated code does not contain a copyright notice

#ifndef LEAP_HAND__SRV__DETAIL__LEAP_VELOCITY__BUILDER_HPP_
#define LEAP_HAND__SRV__DETAIL__LEAP_VELOCITY__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "leap_hand/srv/detail/leap_velocity__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace leap_hand
{

namespace srv
{


}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::leap_hand::srv::LeapVelocity_Request>()
{
  return ::leap_hand::srv::LeapVelocity_Request(rosidl_runtime_cpp::MessageInitialization::ZERO);
}

}  // namespace leap_hand


namespace leap_hand
{

namespace srv
{

namespace builder
{

class Init_LeapVelocity_Response_velocity
{
public:
  Init_LeapVelocity_Response_velocity()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::leap_hand::srv::LeapVelocity_Response velocity(::leap_hand::srv::LeapVelocity_Response::_velocity_type arg)
  {
    msg_.velocity = std::move(arg);
    return std::move(msg_);
  }

private:
  ::leap_hand::srv::LeapVelocity_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::leap_hand::srv::LeapVelocity_Response>()
{
  return leap_hand::srv::builder::Init_LeapVelocity_Response_velocity();
}

}  // namespace leap_hand

#endif  // LEAP_HAND__SRV__DETAIL__LEAP_VELOCITY__BUILDER_HPP_
