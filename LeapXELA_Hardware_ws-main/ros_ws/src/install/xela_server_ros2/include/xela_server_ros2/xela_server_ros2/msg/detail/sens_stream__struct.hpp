// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from xela_server_ros2:msg/SensStream.idl
// generated code does not contain a copyright notice

#ifndef XELA_SERVER_ROS2__MSG__DETAIL__SENS_STREAM__STRUCT_HPP_
#define XELA_SERVER_ROS2__MSG__DETAIL__SENS_STREAM__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'sensors'
#include "xela_server_ros2/msg/detail/sensor_full__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__xela_server_ros2__msg__SensStream __attribute__((deprecated))
#else
# define DEPRECATED__xela_server_ros2__msg__SensStream __declspec(deprecated)
#endif

namespace xela_server_ros2
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct SensStream_
{
  using Type = SensStream_<ContainerAllocator>;

  explicit SensStream_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
  }

  explicit SensStream_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
    (void)_alloc;
  }

  // field types and members
  using _sensors_type =
    std::vector<xela_server_ros2::msg::SensorFull_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<xela_server_ros2::msg::SensorFull_<ContainerAllocator>>>;
  _sensors_type sensors;

  // setters for named parameter idiom
  Type & set__sensors(
    const std::vector<xela_server_ros2::msg::SensorFull_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<xela_server_ros2::msg::SensorFull_<ContainerAllocator>>> & _arg)
  {
    this->sensors = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    xela_server_ros2::msg::SensStream_<ContainerAllocator> *;
  using ConstRawPtr =
    const xela_server_ros2::msg::SensStream_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<xela_server_ros2::msg::SensStream_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<xela_server_ros2::msg::SensStream_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      xela_server_ros2::msg::SensStream_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<xela_server_ros2::msg::SensStream_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      xela_server_ros2::msg::SensStream_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<xela_server_ros2::msg::SensStream_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<xela_server_ros2::msg::SensStream_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<xela_server_ros2::msg::SensStream_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__xela_server_ros2__msg__SensStream
    std::shared_ptr<xela_server_ros2::msg::SensStream_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__xela_server_ros2__msg__SensStream
    std::shared_ptr<xela_server_ros2::msg::SensStream_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const SensStream_ & other) const
  {
    if (this->sensors != other.sensors) {
      return false;
    }
    return true;
  }
  bool operator!=(const SensStream_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct SensStream_

// alias to use template instance with default allocator
using SensStream =
  xela_server_ros2::msg::SensStream_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace xela_server_ros2

#endif  // XELA_SERVER_ROS2__MSG__DETAIL__SENS_STREAM__STRUCT_HPP_
