// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from xela_server_ros2:msg/SensorFull.idl
// generated code does not contain a copyright notice
#include "xela_server_ros2/msg/detail/sensor_full__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `model`
#include "rosidl_runtime_c/string_functions.h"
// Member `taxels`
#include "xela_server_ros2/msg/detail/taxel__functions.h"
// Member `forces`
#include "xela_server_ros2/msg/detail/forces__functions.h"

bool
xela_server_ros2__msg__SensorFull__init(xela_server_ros2__msg__SensorFull * msg)
{
  if (!msg) {
    return false;
  }
  // message
  // time
  // model
  if (!rosidl_runtime_c__String__init(&msg->model)) {
    xela_server_ros2__msg__SensorFull__fini(msg);
    return false;
  }
  // sensor_pos
  // taxels
  if (!xela_server_ros2__msg__Taxel__Sequence__init(&msg->taxels, 0)) {
    xela_server_ros2__msg__SensorFull__fini(msg);
    return false;
  }
  // forces
  if (!xela_server_ros2__msg__Forces__Sequence__init(&msg->forces, 0)) {
    xela_server_ros2__msg__SensorFull__fini(msg);
    return false;
  }
  return true;
}

void
xela_server_ros2__msg__SensorFull__fini(xela_server_ros2__msg__SensorFull * msg)
{
  if (!msg) {
    return;
  }
  // message
  // time
  // model
  rosidl_runtime_c__String__fini(&msg->model);
  // sensor_pos
  // taxels
  xela_server_ros2__msg__Taxel__Sequence__fini(&msg->taxels);
  // forces
  xela_server_ros2__msg__Forces__Sequence__fini(&msg->forces);
}

bool
xela_server_ros2__msg__SensorFull__are_equal(const xela_server_ros2__msg__SensorFull * lhs, const xela_server_ros2__msg__SensorFull * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // message
  if (lhs->message != rhs->message) {
    return false;
  }
  // time
  if (lhs->time != rhs->time) {
    return false;
  }
  // model
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->model), &(rhs->model)))
  {
    return false;
  }
  // sensor_pos
  if (lhs->sensor_pos != rhs->sensor_pos) {
    return false;
  }
  // taxels
  if (!xela_server_ros2__msg__Taxel__Sequence__are_equal(
      &(lhs->taxels), &(rhs->taxels)))
  {
    return false;
  }
  // forces
  if (!xela_server_ros2__msg__Forces__Sequence__are_equal(
      &(lhs->forces), &(rhs->forces)))
  {
    return false;
  }
  return true;
}

bool
xela_server_ros2__msg__SensorFull__copy(
  const xela_server_ros2__msg__SensorFull * input,
  xela_server_ros2__msg__SensorFull * output)
{
  if (!input || !output) {
    return false;
  }
  // message
  output->message = input->message;
  // time
  output->time = input->time;
  // model
  if (!rosidl_runtime_c__String__copy(
      &(input->model), &(output->model)))
  {
    return false;
  }
  // sensor_pos
  output->sensor_pos = input->sensor_pos;
  // taxels
  if (!xela_server_ros2__msg__Taxel__Sequence__copy(
      &(input->taxels), &(output->taxels)))
  {
    return false;
  }
  // forces
  if (!xela_server_ros2__msg__Forces__Sequence__copy(
      &(input->forces), &(output->forces)))
  {
    return false;
  }
  return true;
}

xela_server_ros2__msg__SensorFull *
xela_server_ros2__msg__SensorFull__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  xela_server_ros2__msg__SensorFull * msg = (xela_server_ros2__msg__SensorFull *)allocator.allocate(sizeof(xela_server_ros2__msg__SensorFull), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(xela_server_ros2__msg__SensorFull));
  bool success = xela_server_ros2__msg__SensorFull__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
xela_server_ros2__msg__SensorFull__destroy(xela_server_ros2__msg__SensorFull * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    xela_server_ros2__msg__SensorFull__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
xela_server_ros2__msg__SensorFull__Sequence__init(xela_server_ros2__msg__SensorFull__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  xela_server_ros2__msg__SensorFull * data = NULL;

  if (size) {
    data = (xela_server_ros2__msg__SensorFull *)allocator.zero_allocate(size, sizeof(xela_server_ros2__msg__SensorFull), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = xela_server_ros2__msg__SensorFull__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        xela_server_ros2__msg__SensorFull__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
xela_server_ros2__msg__SensorFull__Sequence__fini(xela_server_ros2__msg__SensorFull__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      xela_server_ros2__msg__SensorFull__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

xela_server_ros2__msg__SensorFull__Sequence *
xela_server_ros2__msg__SensorFull__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  xela_server_ros2__msg__SensorFull__Sequence * array = (xela_server_ros2__msg__SensorFull__Sequence *)allocator.allocate(sizeof(xela_server_ros2__msg__SensorFull__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = xela_server_ros2__msg__SensorFull__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
xela_server_ros2__msg__SensorFull__Sequence__destroy(xela_server_ros2__msg__SensorFull__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    xela_server_ros2__msg__SensorFull__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
xela_server_ros2__msg__SensorFull__Sequence__are_equal(const xela_server_ros2__msg__SensorFull__Sequence * lhs, const xela_server_ros2__msg__SensorFull__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!xela_server_ros2__msg__SensorFull__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
xela_server_ros2__msg__SensorFull__Sequence__copy(
  const xela_server_ros2__msg__SensorFull__Sequence * input,
  xela_server_ros2__msg__SensorFull__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(xela_server_ros2__msg__SensorFull);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    xela_server_ros2__msg__SensorFull * data =
      (xela_server_ros2__msg__SensorFull *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!xela_server_ros2__msg__SensorFull__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          xela_server_ros2__msg__SensorFull__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!xela_server_ros2__msg__SensorFull__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
