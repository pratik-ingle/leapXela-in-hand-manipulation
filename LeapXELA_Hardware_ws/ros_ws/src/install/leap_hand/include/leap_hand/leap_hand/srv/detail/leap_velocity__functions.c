// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from leap_hand:srv/LeapVelocity.idl
// generated code does not contain a copyright notice
#include "leap_hand/srv/detail/leap_velocity__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"

bool
leap_hand__srv__LeapVelocity_Request__init(leap_hand__srv__LeapVelocity_Request * msg)
{
  if (!msg) {
    return false;
  }
  // structure_needs_at_least_one_member
  return true;
}

void
leap_hand__srv__LeapVelocity_Request__fini(leap_hand__srv__LeapVelocity_Request * msg)
{
  if (!msg) {
    return;
  }
  // structure_needs_at_least_one_member
}

bool
leap_hand__srv__LeapVelocity_Request__are_equal(const leap_hand__srv__LeapVelocity_Request * lhs, const leap_hand__srv__LeapVelocity_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // structure_needs_at_least_one_member
  if (lhs->structure_needs_at_least_one_member != rhs->structure_needs_at_least_one_member) {
    return false;
  }
  return true;
}

bool
leap_hand__srv__LeapVelocity_Request__copy(
  const leap_hand__srv__LeapVelocity_Request * input,
  leap_hand__srv__LeapVelocity_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // structure_needs_at_least_one_member
  output->structure_needs_at_least_one_member = input->structure_needs_at_least_one_member;
  return true;
}

leap_hand__srv__LeapVelocity_Request *
leap_hand__srv__LeapVelocity_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  leap_hand__srv__LeapVelocity_Request * msg = (leap_hand__srv__LeapVelocity_Request *)allocator.allocate(sizeof(leap_hand__srv__LeapVelocity_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(leap_hand__srv__LeapVelocity_Request));
  bool success = leap_hand__srv__LeapVelocity_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
leap_hand__srv__LeapVelocity_Request__destroy(leap_hand__srv__LeapVelocity_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    leap_hand__srv__LeapVelocity_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
leap_hand__srv__LeapVelocity_Request__Sequence__init(leap_hand__srv__LeapVelocity_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  leap_hand__srv__LeapVelocity_Request * data = NULL;

  if (size) {
    data = (leap_hand__srv__LeapVelocity_Request *)allocator.zero_allocate(size, sizeof(leap_hand__srv__LeapVelocity_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = leap_hand__srv__LeapVelocity_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        leap_hand__srv__LeapVelocity_Request__fini(&data[i - 1]);
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
leap_hand__srv__LeapVelocity_Request__Sequence__fini(leap_hand__srv__LeapVelocity_Request__Sequence * array)
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
      leap_hand__srv__LeapVelocity_Request__fini(&array->data[i]);
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

leap_hand__srv__LeapVelocity_Request__Sequence *
leap_hand__srv__LeapVelocity_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  leap_hand__srv__LeapVelocity_Request__Sequence * array = (leap_hand__srv__LeapVelocity_Request__Sequence *)allocator.allocate(sizeof(leap_hand__srv__LeapVelocity_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = leap_hand__srv__LeapVelocity_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
leap_hand__srv__LeapVelocity_Request__Sequence__destroy(leap_hand__srv__LeapVelocity_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    leap_hand__srv__LeapVelocity_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
leap_hand__srv__LeapVelocity_Request__Sequence__are_equal(const leap_hand__srv__LeapVelocity_Request__Sequence * lhs, const leap_hand__srv__LeapVelocity_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!leap_hand__srv__LeapVelocity_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
leap_hand__srv__LeapVelocity_Request__Sequence__copy(
  const leap_hand__srv__LeapVelocity_Request__Sequence * input,
  leap_hand__srv__LeapVelocity_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(leap_hand__srv__LeapVelocity_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    leap_hand__srv__LeapVelocity_Request * data =
      (leap_hand__srv__LeapVelocity_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!leap_hand__srv__LeapVelocity_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          leap_hand__srv__LeapVelocity_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!leap_hand__srv__LeapVelocity_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `velocity`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

bool
leap_hand__srv__LeapVelocity_Response__init(leap_hand__srv__LeapVelocity_Response * msg)
{
  if (!msg) {
    return false;
  }
  // velocity
  if (!rosidl_runtime_c__double__Sequence__init(&msg->velocity, 0)) {
    leap_hand__srv__LeapVelocity_Response__fini(msg);
    return false;
  }
  return true;
}

void
leap_hand__srv__LeapVelocity_Response__fini(leap_hand__srv__LeapVelocity_Response * msg)
{
  if (!msg) {
    return;
  }
  // velocity
  rosidl_runtime_c__double__Sequence__fini(&msg->velocity);
}

bool
leap_hand__srv__LeapVelocity_Response__are_equal(const leap_hand__srv__LeapVelocity_Response * lhs, const leap_hand__srv__LeapVelocity_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // velocity
  if (!rosidl_runtime_c__double__Sequence__are_equal(
      &(lhs->velocity), &(rhs->velocity)))
  {
    return false;
  }
  return true;
}

bool
leap_hand__srv__LeapVelocity_Response__copy(
  const leap_hand__srv__LeapVelocity_Response * input,
  leap_hand__srv__LeapVelocity_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // velocity
  if (!rosidl_runtime_c__double__Sequence__copy(
      &(input->velocity), &(output->velocity)))
  {
    return false;
  }
  return true;
}

leap_hand__srv__LeapVelocity_Response *
leap_hand__srv__LeapVelocity_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  leap_hand__srv__LeapVelocity_Response * msg = (leap_hand__srv__LeapVelocity_Response *)allocator.allocate(sizeof(leap_hand__srv__LeapVelocity_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(leap_hand__srv__LeapVelocity_Response));
  bool success = leap_hand__srv__LeapVelocity_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
leap_hand__srv__LeapVelocity_Response__destroy(leap_hand__srv__LeapVelocity_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    leap_hand__srv__LeapVelocity_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
leap_hand__srv__LeapVelocity_Response__Sequence__init(leap_hand__srv__LeapVelocity_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  leap_hand__srv__LeapVelocity_Response * data = NULL;

  if (size) {
    data = (leap_hand__srv__LeapVelocity_Response *)allocator.zero_allocate(size, sizeof(leap_hand__srv__LeapVelocity_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = leap_hand__srv__LeapVelocity_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        leap_hand__srv__LeapVelocity_Response__fini(&data[i - 1]);
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
leap_hand__srv__LeapVelocity_Response__Sequence__fini(leap_hand__srv__LeapVelocity_Response__Sequence * array)
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
      leap_hand__srv__LeapVelocity_Response__fini(&array->data[i]);
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

leap_hand__srv__LeapVelocity_Response__Sequence *
leap_hand__srv__LeapVelocity_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  leap_hand__srv__LeapVelocity_Response__Sequence * array = (leap_hand__srv__LeapVelocity_Response__Sequence *)allocator.allocate(sizeof(leap_hand__srv__LeapVelocity_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = leap_hand__srv__LeapVelocity_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
leap_hand__srv__LeapVelocity_Response__Sequence__destroy(leap_hand__srv__LeapVelocity_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    leap_hand__srv__LeapVelocity_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
leap_hand__srv__LeapVelocity_Response__Sequence__are_equal(const leap_hand__srv__LeapVelocity_Response__Sequence * lhs, const leap_hand__srv__LeapVelocity_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!leap_hand__srv__LeapVelocity_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
leap_hand__srv__LeapVelocity_Response__Sequence__copy(
  const leap_hand__srv__LeapVelocity_Response__Sequence * input,
  leap_hand__srv__LeapVelocity_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(leap_hand__srv__LeapVelocity_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    leap_hand__srv__LeapVelocity_Response * data =
      (leap_hand__srv__LeapVelocity_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!leap_hand__srv__LeapVelocity_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          leap_hand__srv__LeapVelocity_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!leap_hand__srv__LeapVelocity_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
