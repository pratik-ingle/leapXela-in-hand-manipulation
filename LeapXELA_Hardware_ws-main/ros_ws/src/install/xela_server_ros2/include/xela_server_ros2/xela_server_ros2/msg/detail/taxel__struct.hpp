// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from xela_server_ros2:msg/Taxel.idl
// generated code does not contain a copyright notice

#ifndef XELA_SERVER_ROS2__MSG__DETAIL__TAXEL__STRUCT_HPP_
#define XELA_SERVER_ROS2__MSG__DETAIL__TAXEL__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__xela_server_ros2__msg__Taxel __attribute__((deprecated))
#else
# define DEPRECATED__xela_server_ros2__msg__Taxel __declspec(deprecated)
#endif

namespace xela_server_ros2
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Taxel_
{
  using Type = Taxel_<ContainerAllocator>;

  explicit Taxel_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->x = 0;
      this->y = 0;
      this->z = 0;
    }
  }

  explicit Taxel_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->x = 0;
      this->y = 0;
      this->z = 0;
    }
  }

  // field types and members
  using _x_type =
    uint16_t;
  _x_type x;
  using _y_type =
    uint16_t;
  _y_type y;
  using _z_type =
    uint16_t;
  _z_type z;

  // setters for named parameter idiom
  Type & set__x(
    const uint16_t & _arg)
  {
    this->x = _arg;
    return *this;
  }
  Type & set__y(
    const uint16_t & _arg)
  {
    this->y = _arg;
    return *this;
  }
  Type & set__z(
    const uint16_t & _arg)
  {
    this->z = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    xela_server_ros2::msg::Taxel_<ContainerAllocator> *;
  using ConstRawPtr =
    const xela_server_ros2::msg::Taxel_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<xela_server_ros2::msg::Taxel_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<xela_server_ros2::msg::Taxel_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      xela_server_ros2::msg::Taxel_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<xela_server_ros2::msg::Taxel_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      xela_server_ros2::msg::Taxel_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<xela_server_ros2::msg::Taxel_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<xela_server_ros2::msg::Taxel_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<xela_server_ros2::msg::Taxel_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__xela_server_ros2__msg__Taxel
    std::shared_ptr<xela_server_ros2::msg::Taxel_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__xela_server_ros2__msg__Taxel
    std::shared_ptr<xela_server_ros2::msg::Taxel_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Taxel_ & other) const
  {
    if (this->x != other.x) {
      return false;
    }
    if (this->y != other.y) {
      return false;
    }
    if (this->z != other.z) {
      return false;
    }
    return true;
  }
  bool operator!=(const Taxel_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Taxel_

// alias to use template instance with default allocator
using Taxel =
  xela_server_ros2::msg::Taxel_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace xela_server_ros2

#endif  // XELA_SERVER_ROS2__MSG__DETAIL__TAXEL__STRUCT_HPP_
