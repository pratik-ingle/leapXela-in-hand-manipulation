// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from leap_hand:srv/LeapVelocity.idl
// generated code does not contain a copyright notice

#ifndef LEAP_HAND__SRV__DETAIL__LEAP_VELOCITY__STRUCT_HPP_
#define LEAP_HAND__SRV__DETAIL__LEAP_VELOCITY__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__leap_hand__srv__LeapVelocity_Request __attribute__((deprecated))
#else
# define DEPRECATED__leap_hand__srv__LeapVelocity_Request __declspec(deprecated)
#endif

namespace leap_hand
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct LeapVelocity_Request_
{
  using Type = LeapVelocity_Request_<ContainerAllocator>;

  explicit LeapVelocity_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->structure_needs_at_least_one_member = 0;
    }
  }

  explicit LeapVelocity_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->structure_needs_at_least_one_member = 0;
    }
  }

  // field types and members
  using _structure_needs_at_least_one_member_type =
    uint8_t;
  _structure_needs_at_least_one_member_type structure_needs_at_least_one_member;


  // constant declarations

  // pointer types
  using RawPtr =
    leap_hand::srv::LeapVelocity_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const leap_hand::srv::LeapVelocity_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<leap_hand::srv::LeapVelocity_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<leap_hand::srv::LeapVelocity_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      leap_hand::srv::LeapVelocity_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<leap_hand::srv::LeapVelocity_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      leap_hand::srv::LeapVelocity_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<leap_hand::srv::LeapVelocity_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<leap_hand::srv::LeapVelocity_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<leap_hand::srv::LeapVelocity_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__leap_hand__srv__LeapVelocity_Request
    std::shared_ptr<leap_hand::srv::LeapVelocity_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__leap_hand__srv__LeapVelocity_Request
    std::shared_ptr<leap_hand::srv::LeapVelocity_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const LeapVelocity_Request_ & other) const
  {
    if (this->structure_needs_at_least_one_member != other.structure_needs_at_least_one_member) {
      return false;
    }
    return true;
  }
  bool operator!=(const LeapVelocity_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct LeapVelocity_Request_

// alias to use template instance with default allocator
using LeapVelocity_Request =
  leap_hand::srv::LeapVelocity_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace leap_hand


#ifndef _WIN32
# define DEPRECATED__leap_hand__srv__LeapVelocity_Response __attribute__((deprecated))
#else
# define DEPRECATED__leap_hand__srv__LeapVelocity_Response __declspec(deprecated)
#endif

namespace leap_hand
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct LeapVelocity_Response_
{
  using Type = LeapVelocity_Response_<ContainerAllocator>;

  explicit LeapVelocity_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
  }

  explicit LeapVelocity_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
    (void)_alloc;
  }

  // field types and members
  using _velocity_type =
    std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>>;
  _velocity_type velocity;

  // setters for named parameter idiom
  Type & set__velocity(
    const std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>> & _arg)
  {
    this->velocity = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    leap_hand::srv::LeapVelocity_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const leap_hand::srv::LeapVelocity_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<leap_hand::srv::LeapVelocity_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<leap_hand::srv::LeapVelocity_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      leap_hand::srv::LeapVelocity_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<leap_hand::srv::LeapVelocity_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      leap_hand::srv::LeapVelocity_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<leap_hand::srv::LeapVelocity_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<leap_hand::srv::LeapVelocity_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<leap_hand::srv::LeapVelocity_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__leap_hand__srv__LeapVelocity_Response
    std::shared_ptr<leap_hand::srv::LeapVelocity_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__leap_hand__srv__LeapVelocity_Response
    std::shared_ptr<leap_hand::srv::LeapVelocity_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const LeapVelocity_Response_ & other) const
  {
    if (this->velocity != other.velocity) {
      return false;
    }
    return true;
  }
  bool operator!=(const LeapVelocity_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct LeapVelocity_Response_

// alias to use template instance with default allocator
using LeapVelocity_Response =
  leap_hand::srv::LeapVelocity_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace leap_hand

namespace leap_hand
{

namespace srv
{

struct LeapVelocity
{
  using Request = leap_hand::srv::LeapVelocity_Request;
  using Response = leap_hand::srv::LeapVelocity_Response;
};

}  // namespace srv

}  // namespace leap_hand

#endif  // LEAP_HAND__SRV__DETAIL__LEAP_VELOCITY__STRUCT_HPP_
