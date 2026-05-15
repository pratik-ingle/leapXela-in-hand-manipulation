// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from xela_server_ros2:msg/SensorFull.idl
// generated code does not contain a copyright notice

#ifndef XELA_SERVER_ROS2__MSG__DETAIL__SENSOR_FULL__BUILDER_HPP_
#define XELA_SERVER_ROS2__MSG__DETAIL__SENSOR_FULL__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "xela_server_ros2/msg/detail/sensor_full__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace xela_server_ros2
{

namespace msg
{

namespace builder
{

class Init_SensorFull_forces
{
public:
  explicit Init_SensorFull_forces(::xela_server_ros2::msg::SensorFull & msg)
  : msg_(msg)
  {}
  ::xela_server_ros2::msg::SensorFull forces(::xela_server_ros2::msg::SensorFull::_forces_type arg)
  {
    msg_.forces = std::move(arg);
    return std::move(msg_);
  }

private:
  ::xela_server_ros2::msg::SensorFull msg_;
};

class Init_SensorFull_taxels
{
public:
  explicit Init_SensorFull_taxels(::xela_server_ros2::msg::SensorFull & msg)
  : msg_(msg)
  {}
  Init_SensorFull_forces taxels(::xela_server_ros2::msg::SensorFull::_taxels_type arg)
  {
    msg_.taxels = std::move(arg);
    return Init_SensorFull_forces(msg_);
  }

private:
  ::xela_server_ros2::msg::SensorFull msg_;
};

class Init_SensorFull_sensor_pos
{
public:
  explicit Init_SensorFull_sensor_pos(::xela_server_ros2::msg::SensorFull & msg)
  : msg_(msg)
  {}
  Init_SensorFull_taxels sensor_pos(::xela_server_ros2::msg::SensorFull::_sensor_pos_type arg)
  {
    msg_.sensor_pos = std::move(arg);
    return Init_SensorFull_taxels(msg_);
  }

private:
  ::xela_server_ros2::msg::SensorFull msg_;
};

class Init_SensorFull_model
{
public:
  explicit Init_SensorFull_model(::xela_server_ros2::msg::SensorFull & msg)
  : msg_(msg)
  {}
  Init_SensorFull_sensor_pos model(::xela_server_ros2::msg::SensorFull::_model_type arg)
  {
    msg_.model = std::move(arg);
    return Init_SensorFull_sensor_pos(msg_);
  }

private:
  ::xela_server_ros2::msg::SensorFull msg_;
};

class Init_SensorFull_time
{
public:
  explicit Init_SensorFull_time(::xela_server_ros2::msg::SensorFull & msg)
  : msg_(msg)
  {}
  Init_SensorFull_model time(::xela_server_ros2::msg::SensorFull::_time_type arg)
  {
    msg_.time = std::move(arg);
    return Init_SensorFull_model(msg_);
  }

private:
  ::xela_server_ros2::msg::SensorFull msg_;
};

class Init_SensorFull_message
{
public:
  Init_SensorFull_message()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_SensorFull_time message(::xela_server_ros2::msg::SensorFull::_message_type arg)
  {
    msg_.message = std::move(arg);
    return Init_SensorFull_time(msg_);
  }

private:
  ::xela_server_ros2::msg::SensorFull msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::xela_server_ros2::msg::SensorFull>()
{
  return xela_server_ros2::msg::builder::Init_SensorFull_message();
}

}  // namespace xela_server_ros2

#endif  // XELA_SERVER_ROS2__MSG__DETAIL__SENSOR_FULL__BUILDER_HPP_
