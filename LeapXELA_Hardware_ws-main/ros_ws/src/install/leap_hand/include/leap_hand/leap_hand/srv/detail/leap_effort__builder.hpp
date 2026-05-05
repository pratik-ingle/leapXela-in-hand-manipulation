// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from leap_hand:srv/LeapEffort.idl
// generated code does not contain a copyright notice

#ifndef LEAP_HAND__SRV__DETAIL__LEAP_EFFORT__BUILDER_HPP_
#define LEAP_HAND__SRV__DETAIL__LEAP_EFFORT__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "leap_hand/srv/detail/leap_effort__struct.hpp"
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
auto build<::leap_hand::srv::LeapEffort_Request>()
{
  return ::leap_hand::srv::LeapEffort_Request(rosidl_runtime_cpp::MessageInitialization::ZERO);
}

}  // namespace leap_hand


namespace leap_hand
{

namespace srv
{

namespace builder
{

class Init_LeapEffort_Response_effort
{
public:
  Init_LeapEffort_Response_effort()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::leap_hand::srv::LeapEffort_Response effort(::leap_hand::srv::LeapEffort_Response::_effort_type arg)
  {
    msg_.effort = std::move(arg);
    return std::move(msg_);
  }

private:
  ::leap_hand::srv::LeapEffort_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::leap_hand::srv::LeapEffort_Response>()
{
  return leap_hand::srv::builder::Init_LeapEffort_Response_effort();
}

}  // namespace leap_hand

#endif  // LEAP_HAND__SRV__DETAIL__LEAP_EFFORT__BUILDER_HPP_
