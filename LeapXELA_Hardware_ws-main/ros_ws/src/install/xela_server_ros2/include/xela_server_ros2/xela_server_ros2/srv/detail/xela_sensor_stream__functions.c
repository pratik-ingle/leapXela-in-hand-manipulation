// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from xela_server_ros2:srv/XelaSensorStream.idl
// generated code does not contain a copyright notice
#include "xela_server_ros2/srv/detail/xela_sensor_stream__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"

bool
xela_server_ros2__srv__XelaSensorStream_Request__init(xela_server_ros2__srv__XelaSensorStream_Request * msg)
{
  if (!msg) {
    return false;
  }
  // sensor
  return true;
}

void
xela_server_ros2__srv__XelaSensorStream_Request__fini(xela_server_ros2__srv__XelaSensorStream_Request * msg)
{
  if (!msg) {
    return;
  }
  // sensor
}

bool
xela_server_ros2__srv__XelaSensorStream_Request__are_equal(const xela_server_ros2__srv__XelaSensorStream_Request * lhs, const xela_server_ros2__srv__XelaSensorStream_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // sensor
  if (lhs->sensor != rhs->sensor) {
    return false;
  }
  return true;
}

bool
xela_server_ros2__srv__XelaSensorStream_Request__copy(
  const xela_server_ros2__srv__XelaSensorStream_Request * input,
  xela_server_ros2__srv__XelaSensorStream_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // sensor
  output->sensor = input->sensor;
  return true;
}

xela_server_ros2__srv__XelaSensorStream_Request *
xela_server_ros2__srv__XelaSensorStream_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  xela_server_ros2__srv__XelaSensorStream_Request * msg = (xela_server_ros2__srv__XelaSensorStream_Request *)allocator.allocate(sizeof(xela_server_ros2__srv__XelaSensorStream_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(xela_server_ros2__srv__XelaSensorStream_Request));
  bool success = xela_server_ros2__srv__XelaSensorStream_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
xela_server_ros2__srv__XelaSensorStream_Request__destroy(xela_server_ros2__srv__XelaSensorStream_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    xela_server_ros2__srv__XelaSensorStream_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
xela_server_ros2__srv__XelaSensorStream_Request__Sequence__init(xela_server_ros2__srv__XelaSensorStream_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  xela_server_ros2__srv__XelaSensorStream_Request * data = NULL;

  if (size) {
    data = (xela_server_ros2__srv__XelaSensorStream_Request *)allocator.zero_allocate(size, sizeof(xela_server_ros2__srv__XelaSensorStream_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = xela_server_ros2__srv__XelaSensorStream_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        xela_server_ros2__srv__XelaSensorStream_Request__fini(&data[i - 1]);
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
xela_server_ros2__srv__XelaSensorStream_Request__Sequence__fini(xela_server_ros2__srv__XelaSensorStream_Request__Sequence * array)
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
      xela_server_ros2__srv__XelaSensorStream_Request__fini(&array->data[i]);
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

xela_server_ros2__srv__XelaSensorStream_Request__Sequence *
xela_server_ros2__srv__XelaSensorStream_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  xela_server_ros2__srv__XelaSensorStream_Request__Sequence * array = (xela_server_ros2__srv__XelaSensorStream_Request__Sequence *)allocator.allocate(sizeof(xela_server_ros2__srv__XelaSensorStream_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = xela_server_ros2__srv__XelaSensorStream_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
xela_server_ros2__srv__XelaSensorStream_Request__Sequence__destroy(xela_server_ros2__srv__XelaSensorStream_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    xela_server_ros2__srv__XelaSensorStream_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
xela_server_ros2__srv__XelaSensorStream_Request__Sequence__are_equal(const xela_server_ros2__srv__XelaSensorStream_Request__Sequence * lhs, const xela_server_ros2__srv__XelaSensorStream_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!xela_server_ros2__srv__XelaSensorStream_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
xela_server_ros2__srv__XelaSensorStream_Request__Sequence__copy(
  const xela_server_ros2__srv__XelaSensorStream_Request__Sequence * input,
  xela_server_ros2__srv__XelaSensorStream_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(xela_server_ros2__srv__XelaSensorStream_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    xela_server_ros2__srv__XelaSensorStream_Request * data =
      (xela_server_ros2__srv__XelaSensorStream_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!xela_server_ros2__srv__XelaSensorStream_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          xela_server_ros2__srv__XelaSensorStream_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!xela_server_ros2__srv__XelaSensorStream_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `data`
#include "xela_server_ros2/msg/detail/sensor_full__functions.h"

bool
xela_server_ros2__srv__XelaSensorStream_Response__init(xela_server_ros2__srv__XelaSensorStream_Response * msg)
{
  if (!msg) {
    return false;
  }
  // data
  if (!xela_server_ros2__msg__SensorFull__Sequence__init(&msg->data, 0)) {
    xela_server_ros2__srv__XelaSensorStream_Response__fini(msg);
    return false;
  }
  return true;
}

void
xela_server_ros2__srv__XelaSensorStream_Response__fini(xela_server_ros2__srv__XelaSensorStream_Response * msg)
{
  if (!msg) {
    return;
  }
  // data
  xela_server_ros2__msg__SensorFull__Sequence__fini(&msg->data);
}

bool
xela_server_ros2__srv__XelaSensorStream_Response__are_equal(const xela_server_ros2__srv__XelaSensorStream_Response * lhs, const xela_server_ros2__srv__XelaSensorStream_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // data
  if (!xela_server_ros2__msg__SensorFull__Sequence__are_equal(
      &(lhs->data), &(rhs->data)))
  {
    return false;
  }
  return true;
}

bool
xela_server_ros2__srv__XelaSensorStream_Response__copy(
  const xela_server_ros2__srv__XelaSensorStream_Response * input,
  xela_server_ros2__srv__XelaSensorStream_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // data
  if (!xela_server_ros2__msg__SensorFull__Sequence__copy(
      &(input->data), &(output->data)))
  {
    return false;
  }
  return true;
}

xela_server_ros2__srv__XelaSensorStream_Response *
xela_server_ros2__srv__XelaSensorStream_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  xela_server_ros2__srv__XelaSensorStream_Response * msg = (xela_server_ros2__srv__XelaSensorStream_Response *)allocator.allocate(sizeof(xela_server_ros2__srv__XelaSensorStream_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(xela_server_ros2__srv__XelaSensorStream_Response));
  bool success = xela_server_ros2__srv__XelaSensorStream_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
xela_server_ros2__srv__XelaSensorStream_Response__destroy(xela_server_ros2__srv__XelaSensorStream_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    xela_server_ros2__srv__XelaSensorStream_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
xela_server_ros2__srv__XelaSensorStream_Response__Sequence__init(xela_server_ros2__srv__XelaSensorStream_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  xela_server_ros2__srv__XelaSensorStream_Response * data = NULL;

  if (size) {
    data = (xela_server_ros2__srv__XelaSensorStream_Response *)allocator.zero_allocate(size, sizeof(xela_server_ros2__srv__XelaSensorStream_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = xela_server_ros2__srv__XelaSensorStream_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        xela_server_ros2__srv__XelaSensorStream_Response__fini(&data[i - 1]);
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
xela_server_ros2__srv__XelaSensorStream_Response__Sequence__fini(xela_server_ros2__srv__XelaSensorStream_Response__Sequence * array)
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
      xela_server_ros2__srv__XelaSensorStream_Response__fini(&array->data[i]);
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

xela_server_ros2__srv__XelaSensorStream_Response__Sequence *
xela_server_ros2__srv__XelaSensorStream_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  xela_server_ros2__srv__XelaSensorStream_Response__Sequence * array = (xela_server_ros2__srv__XelaSensorStream_Response__Sequence *)allocator.allocate(sizeof(xela_server_ros2__srv__XelaSensorStream_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = xela_server_ros2__srv__XelaSensorStream_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
xela_server_ros2__srv__XelaSensorStream_Response__Sequence__destroy(xela_server_ros2__srv__XelaSensorStream_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    xela_server_ros2__srv__XelaSensorStream_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
xela_server_ros2__srv__XelaSensorStream_Response__Sequence__are_equal(const xela_server_ros2__srv__XelaSensorStream_Response__Sequence * lhs, const xela_server_ros2__srv__XelaSensorStream_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!xela_server_ros2__srv__XelaSensorStream_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
xela_server_ros2__srv__XelaSensorStream_Response__Sequence__copy(
  const xela_server_ros2__srv__XelaSensorStream_Response__Sequence * input,
  xela_server_ros2__srv__XelaSensorStream_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(xela_server_ros2__srv__XelaSensorStream_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    xela_server_ros2__srv__XelaSensorStream_Response * data =
      (xela_server_ros2__srv__XelaSensorStream_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!xela_server_ros2__srv__XelaSensorStream_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          xela_server_ros2__srv__XelaSensorStream_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!xela_server_ros2__srv__XelaSensorStream_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
