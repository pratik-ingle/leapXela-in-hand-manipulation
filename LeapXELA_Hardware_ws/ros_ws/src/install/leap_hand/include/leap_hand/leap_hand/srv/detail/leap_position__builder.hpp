// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from leap_hand:srv/LeapPosition.idl
// generated code does not contain a copyright notice

#ifndef LEAP_HAND__SRV__DETAIL__LEAP_POSITION__BUILDER_HPP_
#define LEAP_HAND__SRV__DETAIL__LEAP_POSITION__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "leap_hand/srv/detail/leap_position__struct.hpp"
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
auto build<::leap_hand::srv::LeapPosition_Request>()
{
  return ::leap_hand::srv::LeapPosition_Request(rosidl_runtime_cpp::MessageInitialization::ZERO);
}

}  // namespace leap_hand


namespace leap_hand
{

namespace srv
{

namespace builder
{

class Init_LeapPosition_Response_position
{
public:
  Init_LeapPosition_Response_position()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::leap_hand::srv::LeapPosition_Response position(::leap_hand::srv::LeapPosition_Response::_position_type arg)
  {
    msg_.position = std::move(arg);
    return std::move(msg_);
  }

private:
  ::leap_hand::srv::LeapPosition_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::leap_hand::srv::LeapPosition_Response>()
{
  return leap_hand::srv::builder::Init_LeapPosition_Response_position();
}

}  // namespace leap_hand

#endif  // LEAP_HAND__SRV__DETAIL__LEAP_POSITION__BUILDER_HPP_
