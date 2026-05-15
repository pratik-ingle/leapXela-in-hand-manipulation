// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from xela_server_ros2:srv/XelaSensorStream.idl
// generated code does not contain a copyright notice

#ifndef XELA_SERVER_ROS2__SRV__DETAIL__XELA_SENSOR_STREAM__STRUCT_HPP_
#define XELA_SERVER_ROS2__SRV__DETAIL__XELA_SENSOR_STREAM__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__xela_server_ros2__srv__XelaSensorStream_Request __attribute__((deprecated))
#else
# define DEPRECATED__xela_server_ros2__srv__XelaSensorStream_Request __declspec(deprecated)
#endif

namespace xela_server_ros2
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct XelaSensorStream_Request_
{
  using Type = XelaSensorStream_Request_<ContainerAllocator>;

  explicit XelaSensorStream_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->sensor = 0;
    }
  }

  explicit XelaSensorStream_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->sensor = 0;
    }
  }

  // field types and members
  using _sensor_type =
    uint8_t;
  _sensor_type sensor;

  // setters for named parameter idiom
  Type & set__sensor(
    const uint8_t & _arg)
  {
    this->sensor = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    xela_server_ros2::srv::XelaSensorStream_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const xela_server_ros2::srv::XelaSensorStream_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<xela_server_ros2::srv::XelaSensorStream_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<xela_server_ros2::srv::XelaSensorStream_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      xela_server_ros2::srv::XelaSensorStream_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<xela_server_ros2::srv::XelaSensorStream_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      xela_server_ros2::srv::XelaSensorStream_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<xela_server_ros2::srv::XelaSensorStream_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<xela_server_ros2::srv::XelaSensorStream_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<xela_server_ros2::srv::XelaSensorStream_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__xela_server_ros2__srv__XelaSensorStream_Request
    std::shared_ptr<xela_server_ros2::srv::XelaSensorStream_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__xela_server_ros2__srv__XelaSensorStream_Request
    std::shared_ptr<xela_server_ros2::srv::XelaSensorStream_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const XelaSensorStream_Request_ & other) const
  {
    if (this->sensor != other.sensor) {
      return false;
    }
    return true;
  }
  bool operator!=(const XelaSensorStream_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct XelaSensorStream_Request_

// alias to use template instance with default allocator
using XelaSensorStream_Request =
  xela_server_ros2::srv::XelaSensorStream_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace xela_server_ros2


// Include directives for member types
// Member 'data'
#include "xela_server_ros2/msg/detail/sensor_full__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__xela_server_ros2__srv__XelaSensorStream_Response __attribute__((deprecated))
#else
# define DEPRECATED__xela_server_ros2__srv__XelaSensorStream_Response __declspec(deprecated)
#endif

namespace xela_server_ros2
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct XelaSensorStream_Response_
{
  using Type = XelaSensorStream_Response_<ContainerAllocator>;

  explicit XelaSensorStream_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
  }

  explicit XelaSensorStream_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
    (void)_alloc;
  }

  // field types and members
  using _data_type =
    std::vector<xela_server_ros2::msg::SensorFull_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<xela_server_ros2::msg::SensorFull_<ContainerAllocator>>>;
  _data_type data;

  // setters for named parameter idiom
  Type & set__data(
    const std::vector<xela_server_ros2::msg::SensorFull_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<xela_server_ros2::msg::SensorFull_<ContainerAllocator>>> & _arg)
  {
    this->data = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    xela_server_ros2::srv::XelaSensorStream_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const xela_server_ros2::srv::XelaSensorStream_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<xela_server_ros2::srv::XelaSensorStream_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<xela_server_ros2::srv::XelaSensorStream_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      xela_server_ros2::srv::XelaSensorStream_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<xela_server_ros2::srv::XelaSensorStream_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      xela_server_ros2::srv::XelaSensorStream_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<xela_server_ros2::srv::XelaSensorStream_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<xela_server_ros2::srv::XelaSensorStream_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<xela_server_ros2::srv::XelaSensorStream_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__xela_server_ros2__srv__XelaSensorStream_Response
    std::shared_ptr<xela_server_ros2::srv::XelaSensorStream_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__xela_server_ros2__srv__XelaSensorStream_Response
    std::shared_ptr<xela_server_ros2::srv::XelaSensorStream_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const XelaSensorStream_Response_ & other) const
  {
    if (this->data != other.data) {
      return false;
    }
    return true;
  }
  bool operator!=(const XelaSensorStream_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct XelaSensorStream_Response_

// alias to use template instance with default allocator
using XelaSensorStream_Response =
  xela_server_ros2::srv::XelaSensorStream_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace xela_server_ros2

namespace xela_server_ros2
{

namespace srv
{

struct XelaSensorStream
{
  using Request = xela_server_ros2::srv::XelaSensorStream_Request;
  using Response = xela_server_ros2::srv::XelaSensorStream_Response;
};

}  // namespace srv

}  // namespace xela_server_ros2

#endif  // XELA_SERVER_ROS2__SRV__DETAIL__XELA_SENSOR_STREAM__STRUCT_HPP_
