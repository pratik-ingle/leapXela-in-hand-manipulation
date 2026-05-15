// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from xela_server_ros2:msg/Taxel.idl
// generated code does not contain a copyright notice

#ifndef XELA_SERVER_ROS2__MSG__DETAIL__TAXEL__BUILDER_HPP_
#define XELA_SERVER_ROS2__MSG__DETAIL__TAXEL__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "xela_server_ros2/msg/detail/taxel__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace xela_server_ros2
{

namespace msg
{

namespace builder
{

class Init_Taxel_z
{
public:
  explicit Init_Taxel_z(::xela_server_ros2::msg::Taxel & msg)
  : msg_(msg)
  {}
  ::xela_server_ros2::msg::Taxel z(::xela_server_ros2::msg::Taxel::_z_type arg)
  {
    msg_.z = std::move(arg);
    return std::move(msg_);
  }

private:
  ::xela_server_ros2::msg::Taxel msg_;
};

class Init_Taxel_y
{
public:
  explicit Init_Taxel_y(::xela_server_ros2::msg::Taxel & msg)
  : msg_(msg)
  {}
  Init_Taxel_z y(::xela_server_ros2::msg::Taxel::_y_type arg)
  {
    msg_.y = std::move(arg);
    return Init_Taxel_z(msg_);
  }

private:
  ::xela_server_ros2::msg::Taxel msg_;
};

class Init_Taxel_x
{
public:
  Init_Taxel_x()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Taxel_y x(::xela_server_ros2::msg::Taxel::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_Taxel_y(msg_);
  }

private:
  ::xela_server_ros2::msg::Taxel msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::xela_server_ros2::msg::Taxel>()
{
  return xela_server_ros2::msg::builder::Init_Taxel_x();
}

}  // namespace xela_server_ros2

#endif  // XELA_SERVER_ROS2__MSG__DETAIL__TAXEL__BUILDER_HPP_
