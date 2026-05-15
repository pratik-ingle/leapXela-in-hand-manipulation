// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from xela_server_ros2:srv/XelaSensorStream.idl
// generated code does not contain a copyright notice

#ifndef XELA_SERVER_ROS2__SRV__DETAIL__XELA_SENSOR_STREAM__BUILDER_HPP_
#define XELA_SERVER_ROS2__SRV__DETAIL__XELA_SENSOR_STREAM__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "xela_server_ros2/srv/detail/xela_sensor_stream__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace xela_server_ros2
{

namespace srv
{

namespace builder
{

class Init_XelaSensorStream_Request_sensor
{
public:
  Init_XelaSensorStream_Request_sensor()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::xela_server_ros2::srv::XelaSensorStream_Request sensor(::xela_server_ros2::srv::XelaSensorStream_Request::_sensor_type arg)
  {
    msg_.sensor = std::move(arg);
    return std::move(msg_);
  }

private:
  ::xela_server_ros2::srv::XelaSensorStream_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::xela_server_ros2::srv::XelaSensorStream_Request>()
{
  return xela_server_ros2::srv::builder::Init_XelaSensorStream_Request_sensor();
}

}  // namespace xela_server_ros2


namespace xela_server_ros2
{

namespace srv
{

namespace builder
{

class Init_XelaSensorStream_Response_data
{
public:
  Init_XelaSensorStream_Response_data()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::xela_server_ros2::srv::XelaSensorStream_Response data(::xela_server_ros2::srv::XelaSensorStream_Response::_data_type arg)
  {
    msg_.data = std::move(arg);
    return std::move(msg_);
  }

private:
  ::xela_server_ros2::srv::XelaSensorStream_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::xela_server_ros2::srv::XelaSensorStream_Response>()
{
  return xela_server_ros2::srv::builder::Init_XelaSensorStream_Response_data();
}

}  // namespace xela_server_ros2

#endif  // XELA_SERVER_ROS2__SRV__DETAIL__XELA_SENSOR_STREAM__BUILDER_HPP_
