// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from xela_server_ros2:msg/Forces.idl
// generated code does not contain a copyright notice
#include "xela_server_ros2/msg/detail/forces__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
xela_server_ros2__msg__Forces__init(xela_server_ros2__msg__Forces * msg)
{
  if (!msg) {
    return false;
  }
  // x
  // y
  // z
  return true;
}

void
xela_server_ros2__msg__Forces__fini(xela_server_ros2__msg__Forces * msg)
{
  if (!msg) {
    return;
  }
  // x
  // y
  // z
}

bool
xela_server_ros2__msg__Forces__are_equal(const xela_server_ros2__msg__Forces * lhs, const xela_server_ros2__msg__Forces * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // x
  if (lhs->x != rhs->x) {
    return false;
  }
  // y
  if (lhs->y != rhs->y) {
    return false;
  }
  // z
  if (lhs->z != rhs->z) {
    return false;
  }
  return true;
}

bool
xela_server_ros2__msg__Forces__copy(
  const xela_server_ros2__msg__Forces * input,
  xela_server_ros2__msg__Forces * output)
{
  if (!input || !output) {
    return false;
  }
  // x
  output->x = input->x;
  // y
  output->y = input->y;
  // z
  output->z = input->z;
  return true;
}

xela_server_ros2__msg__Forces *
xela_server_ros2__msg__Forces__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  xela_server_ros2__msg__Forces * msg = (xela_server_ros2__msg__Forces *)allocator.allocate(sizeof(xela_server_ros2__msg__Forces), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(xela_server_ros2__msg__Forces));
  bool success = xela_server_ros2__msg__Forces__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
xela_server_ros2__msg__Forces__destroy(xela_server_ros2__msg__Forces * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    xela_server_ros2__msg__Forces__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
xela_server_ros2__msg__Forces__Sequence__init(xela_server_ros2__msg__Forces__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  xela_server_ros2__msg__Forces * data = NULL;

  if (size) {
    data = (xela_server_ros2__msg__Forces *)allocator.zero_allocate(size, sizeof(xela_server_ros2__msg__Forces), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = xela_server_ros2__msg__Forces__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        xela_server_ros2__msg__Forces__fini(&data[i - 1]);
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
xela_server_ros2__msg__Forces__Sequence__fini(xela_server_ros2__msg__Forces__Sequence * array)
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
      xela_server_ros2__msg__Forces__fini(&array->data[i]);
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

xela_server_ros2__msg__Forces__Sequence *
xela_server_ros2__msg__Forces__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  xela_server_ros2__msg__Forces__Sequence * array = (xela_server_ros2__msg__Forces__Sequence *)allocator.allocate(sizeof(xela_server_ros2__msg__Forces__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = xela_server_ros2__msg__Forces__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
xela_server_ros2__msg__Forces__Sequence__destroy(xela_server_ros2__msg__Forces__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    xela_server_ros2__msg__Forces__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
xela_server_ros2__msg__Forces__Sequence__are_equal(const xela_server_ros2__msg__Forces__Sequence * lhs, const xela_server_ros2__msg__Forces__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!xela_server_ros2__msg__Forces__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
xela_server_ros2__msg__Forces__Sequence__copy(
  const xela_server_ros2__msg__Forces__Sequence * input,
  xela_server_ros2__msg__Forces__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(xela_server_ros2__msg__Forces);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    xela_server_ros2__msg__Forces * data =
      (xela_server_ros2__msg__Forces *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!xela_server_ros2__msg__Forces__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          xela_server_ros2__msg__Forces__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!xela_server_ros2__msg__Forces__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
