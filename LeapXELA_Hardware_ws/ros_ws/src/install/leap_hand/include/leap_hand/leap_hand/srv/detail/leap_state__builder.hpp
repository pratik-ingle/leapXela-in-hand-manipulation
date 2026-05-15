// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from leap_hand:srv/LeapState.idl
// generated code does not contain a copyright notice

#ifndef LEAP_HAND__SRV__DETAIL__LEAP_STATE__BUILDER_HPP_
#define LEAP_HAND__SRV__DETAIL__LEAP_STATE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "leap_hand/srv/detail/leap_state__struct.hpp"
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
auto build<::leap_hand::srv::LeapState_Request>()
{
  return ::leap_hand::srv::LeapState_Request(rosidl_runtime_cpp::MessageInitialization::ZERO);
}

}  // namespace leap_hand


namespace leap_hand
{

namespace srv
{

namespace builder
{

class Init_LeapState_Response_position
{
public:
  explicit Init_LeapState_Response_position(::leap_hand::srv::LeapState_Response & msg)
  : msg_(msg)
  {}
  ::leap_hand::srv::LeapState_Response position(::leap_hand::srv::LeapState_Response::_position_type arg)
  {
    msg_.position = std::move(arg);
    return std::move(msg_);
  }

private:
  ::leap_hand::srv::LeapState_Response msg_;
};

class Init_LeapState_Response_effort
{
public:
  explicit Init_LeapState_Response_effort(::leap_hand::srv::LeapState_Response & msg)
  : msg_(msg)
  {}
  Init_LeapState_Response_position effort(::leap_hand::srv::LeapState_Response::_effort_type arg)
  {
    msg_.effort = std::move(arg);
    return Init_LeapState_Response_position(msg_);
  }

private:
  ::leap_hand::srv::LeapState_Response msg_;
};

class Init_LeapState_Response_velocity
{
public:
  Init_LeapState_Response_velocity()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_LeapState_Response_effort velocity(::leap_hand::srv::LeapState_Response::_velocity_type arg)
  {
    msg_.velocity = std::move(arg);
    return Init_LeapState_Response_effort(msg_);
  }

private:
  ::leap_hand::srv::LeapState_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::leap_hand::srv::LeapState_Response>()
{
  return leap_hand::srv::builder::Init_LeapState_Response_velocity();
}

}  // namespace leap_hand

#endif  // LEAP_HAND__SRV__DETAIL__LEAP_STATE__BUILDER_HPP_
