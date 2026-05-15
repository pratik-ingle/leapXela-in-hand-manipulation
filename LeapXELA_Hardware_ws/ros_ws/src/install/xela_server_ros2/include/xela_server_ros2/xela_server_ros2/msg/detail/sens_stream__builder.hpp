// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from xela_server_ros2:msg/SensStream.idl
// generated code does not contain a copyright notice

#ifndef XELA_SERVER_ROS2__MSG__DETAIL__SENS_STREAM__BUILDER_HPP_
#define XELA_SERVER_ROS2__MSG__DETAIL__SENS_STREAM__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "xela_server_ros2/msg/detail/sens_stream__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace xela_server_ros2
{

namespace msg
{

namespace builder
{

class Init_SensStream_sensors
{
public:
  Init_SensStream_sensors()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::xela_server_ros2::msg::SensStream sensors(::xela_server_ros2::msg::SensStream::_sensors_type arg)
  {
    msg_.sensors = std::move(arg);
    return std::move(msg_);
  }

private:
  ::xela_server_ros2::msg::SensStream msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::xela_server_ros2::msg::SensStream>()
{
  return xela_server_ros2::msg::builder::Init_SensStream_sensors();
}

}  // namespace xela_server_ros2

#endif  // XELA_SERVER_ROS2__MSG__DETAIL__SENS_STREAM__BUILDER_HPP_
