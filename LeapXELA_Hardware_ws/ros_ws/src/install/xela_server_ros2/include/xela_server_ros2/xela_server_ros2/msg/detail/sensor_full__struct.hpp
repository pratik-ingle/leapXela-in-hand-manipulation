// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from xela_server_ros2:msg/SensorFull.idl
// generated code does not contain a copyright notice

#ifndef XELA_SERVER_ROS2__MSG__DETAIL__SENSOR_FULL__STRUCT_HPP_
#define XELA_SERVER_ROS2__MSG__DETAIL__SENSOR_FULL__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'taxels'
#include "xela_server_ros2/msg/detail/taxel__struct.hpp"
// Member 'forces'
#include "xela_server_ros2/msg/detail/forces__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__xela_server_ros2__msg__SensorFull __attribute__((deprecated))
#else
# define DEPRECATED__xela_server_ros2__msg__SensorFull __declspec(deprecated)
#endif

namespace xela_server_ros2
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct SensorFull_
{
  using Type = SensorFull_<ContainerAllocator>;

  explicit SensorFull_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->message = 0ul;
      this->time = 0.0;
      this->model = "";
      this->sensor_pos = 0;
    }
  }

  explicit SensorFull_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : model(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->message = 0ul;
      this->time = 0.0;
      this->model = "";
      this->sensor_pos = 0;
    }
  }

  // field types and members
  using _message_type =
    uint32_t;
  _message_type message;
  using _time_type =
    double;
  _time_type time;
  using _model_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _model_type model;
  using _sensor_pos_type =
    uint8_t;
  _sensor_pos_type sensor_pos;
  using _taxels_type =
    std::vector<xela_server_ros2::msg::Taxel_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<xela_server_ros2::msg::Taxel_<ContainerAllocator>>>;
  _taxels_type taxels;
  using _forces_type =
    std::vector<xela_server_ros2::msg::Forces_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<xela_server_ros2::msg::Forces_<ContainerAllocator>>>;
  _forces_type forces;

  // setters for named parameter idiom
  Type & set__message(
    const uint32_t & _arg)
  {
    this->message = _arg;
    return *this;
  }
  Type & set__time(
    const double & _arg)
  {
    this->time = _arg;
    return *this;
  }
  Type & set__model(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->model = _arg;
    return *this;
  }
  Type & set__sensor_pos(
    const uint8_t & _arg)
  {
    this->sensor_pos = _arg;
    return *this;
  }
  Type & set__taxels(
    const std::vector<xela_server_ros2::msg::Taxel_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<xela_server_ros2::msg::Taxel_<ContainerAllocator>>> & _arg)
  {
    this->taxels = _arg;
    return *this;
  }
  Type & set__forces(
    const std::vector<xela_server_ros2::msg::Forces_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<xela_server_ros2::msg::Forces_<ContainerAllocator>>> & _arg)
  {
    this->forces = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    xela_server_ros2::msg::SensorFull_<ContainerAllocator> *;
  using ConstRawPtr =
    const xela_server_ros2::msg::SensorFull_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<xela_server_ros2::msg::SensorFull_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<xela_server_ros2::msg::SensorFull_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      xela_server_ros2::msg::SensorFull_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<xela_server_ros2::msg::SensorFull_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      xela_server_ros2::msg::SensorFull_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<xela_server_ros2::msg::SensorFull_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<xela_server_ros2::msg::SensorFull_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<xela_server_ros2::msg::SensorFull_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__xela_server_ros2__msg__SensorFull
    std::shared_ptr<xela_server_ros2::msg::SensorFull_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__xela_server_ros2__msg__SensorFull
    std::shared_ptr<xela_server_ros2::msg::SensorFull_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const SensorFull_ & other) const
  {
    if (this->message != other.message) {
      return false;
    }
    if (this->time != other.time) {
      return false;
    }
    if (this->model != other.model) {
      return false;
    }
    if (this->sensor_pos != other.sensor_pos) {
      return false;
    }
    if (this->taxels != other.taxels) {
      return false;
    }
    if (this->forces != other.forces) {
      return false;
    }
    return true;
  }
  bool operator!=(const SensorFull_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct SensorFull_

// alias to use template instance with default allocator
using SensorFull =
  xela_server_ros2::msg::SensorFull_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace xela_server_ros2

#endif  // XELA_SERVER_ROS2__MSG__DETAIL__SENSOR_FULL__STRUCT_HPP_
