#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



#[link(name = "leap_hand__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__leap_hand__srv__LeapVelocity_Request() -> *const std::ffi::c_void;
}

#[link(name = "leap_hand__rosidl_generator_c")]
extern "C" {
    fn leap_hand__srv__LeapVelocity_Request__init(msg: *mut LeapVelocity_Request) -> bool;
    fn leap_hand__srv__LeapVelocity_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<LeapVelocity_Request>, size: usize) -> bool;
    fn leap_hand__srv__LeapVelocity_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<LeapVelocity_Request>);
    fn leap_hand__srv__LeapVelocity_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<LeapVelocity_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<LeapVelocity_Request>) -> bool;
}

// Corresponds to leap_hand__srv__LeapVelocity_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct LeapVelocity_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for LeapVelocity_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !leap_hand__srv__LeapVelocity_Request__init(&mut msg as *mut _) {
        panic!("Call to leap_hand__srv__LeapVelocity_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for LeapVelocity_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { leap_hand__srv__LeapVelocity_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { leap_hand__srv__LeapVelocity_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { leap_hand__srv__LeapVelocity_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for LeapVelocity_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for LeapVelocity_Request where Self: Sized {
  const TYPE_NAME: &'static str = "leap_hand/srv/LeapVelocity_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__leap_hand__srv__LeapVelocity_Request() }
  }
}


#[link(name = "leap_hand__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__leap_hand__srv__LeapVelocity_Response() -> *const std::ffi::c_void;
}

#[link(name = "leap_hand__rosidl_generator_c")]
extern "C" {
    fn leap_hand__srv__LeapVelocity_Response__init(msg: *mut LeapVelocity_Response) -> bool;
    fn leap_hand__srv__LeapVelocity_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<LeapVelocity_Response>, size: usize) -> bool;
    fn leap_hand__srv__LeapVelocity_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<LeapVelocity_Response>);
    fn leap_hand__srv__LeapVelocity_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<LeapVelocity_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<LeapVelocity_Response>) -> bool;
}

// Corresponds to leap_hand__srv__LeapVelocity_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct LeapVelocity_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub velocity: rosidl_runtime_rs::Sequence<f64>,

}



impl Default for LeapVelocity_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !leap_hand__srv__LeapVelocity_Response__init(&mut msg as *mut _) {
        panic!("Call to leap_hand__srv__LeapVelocity_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for LeapVelocity_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { leap_hand__srv__LeapVelocity_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { leap_hand__srv__LeapVelocity_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { leap_hand__srv__LeapVelocity_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for LeapVelocity_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for LeapVelocity_Response where Self: Sized {
  const TYPE_NAME: &'static str = "leap_hand/srv/LeapVelocity_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__leap_hand__srv__LeapVelocity_Response() }
  }
}


#[link(name = "leap_hand__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__leap_hand__srv__LeapPosition_Request() -> *const std::ffi::c_void;
}

#[link(name = "leap_hand__rosidl_generator_c")]
extern "C" {
    fn leap_hand__srv__LeapPosition_Request__init(msg: *mut LeapPosition_Request) -> bool;
    fn leap_hand__srv__LeapPosition_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<LeapPosition_Request>, size: usize) -> bool;
    fn leap_hand__srv__LeapPosition_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<LeapPosition_Request>);
    fn leap_hand__srv__LeapPosition_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<LeapPosition_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<LeapPosition_Request>) -> bool;
}

// Corresponds to leap_hand__srv__LeapPosition_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct LeapPosition_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for LeapPosition_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !leap_hand__srv__LeapPosition_Request__init(&mut msg as *mut _) {
        panic!("Call to leap_hand__srv__LeapPosition_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for LeapPosition_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { leap_hand__srv__LeapPosition_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { leap_hand__srv__LeapPosition_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { leap_hand__srv__LeapPosition_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for LeapPosition_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for LeapPosition_Request where Self: Sized {
  const TYPE_NAME: &'static str = "leap_hand/srv/LeapPosition_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__leap_hand__srv__LeapPosition_Request() }
  }
}


#[link(name = "leap_hand__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__leap_hand__srv__LeapPosition_Response() -> *const std::ffi::c_void;
}

#[link(name = "leap_hand__rosidl_generator_c")]
extern "C" {
    fn leap_hand__srv__LeapPosition_Response__init(msg: *mut LeapPosition_Response) -> bool;
    fn leap_hand__srv__LeapPosition_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<LeapPosition_Response>, size: usize) -> bool;
    fn leap_hand__srv__LeapPosition_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<LeapPosition_Response>);
    fn leap_hand__srv__LeapPosition_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<LeapPosition_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<LeapPosition_Response>) -> bool;
}

// Corresponds to leap_hand__srv__LeapPosition_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct LeapPosition_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub position: rosidl_runtime_rs::Sequence<f64>,

}



impl Default for LeapPosition_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !leap_hand__srv__LeapPosition_Response__init(&mut msg as *mut _) {
        panic!("Call to leap_hand__srv__LeapPosition_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for LeapPosition_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { leap_hand__srv__LeapPosition_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { leap_hand__srv__LeapPosition_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { leap_hand__srv__LeapPosition_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for LeapPosition_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for LeapPosition_Response where Self: Sized {
  const TYPE_NAME: &'static str = "leap_hand/srv/LeapPosition_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__leap_hand__srv__LeapPosition_Response() }
  }
}


#[link(name = "leap_hand__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__leap_hand__srv__LeapEffort_Request() -> *const std::ffi::c_void;
}

#[link(name = "leap_hand__rosidl_generator_c")]
extern "C" {
    fn leap_hand__srv__LeapEffort_Request__init(msg: *mut LeapEffort_Request) -> bool;
    fn leap_hand__srv__LeapEffort_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<LeapEffort_Request>, size: usize) -> bool;
    fn leap_hand__srv__LeapEffort_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<LeapEffort_Request>);
    fn leap_hand__srv__LeapEffort_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<LeapEffort_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<LeapEffort_Request>) -> bool;
}

// Corresponds to leap_hand__srv__LeapEffort_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct LeapEffort_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for LeapEffort_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !leap_hand__srv__LeapEffort_Request__init(&mut msg as *mut _) {
        panic!("Call to leap_hand__srv__LeapEffort_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for LeapEffort_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { leap_hand__srv__LeapEffort_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { leap_hand__srv__LeapEffort_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { leap_hand__srv__LeapEffort_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for LeapEffort_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for LeapEffort_Request where Self: Sized {
  const TYPE_NAME: &'static str = "leap_hand/srv/LeapEffort_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__leap_hand__srv__LeapEffort_Request() }
  }
}


#[link(name = "leap_hand__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__leap_hand__srv__LeapEffort_Response() -> *const std::ffi::c_void;
}

#[link(name = "leap_hand__rosidl_generator_c")]
extern "C" {
    fn leap_hand__srv__LeapEffort_Response__init(msg: *mut LeapEffort_Response) -> bool;
    fn leap_hand__srv__LeapEffort_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<LeapEffort_Response>, size: usize) -> bool;
    fn leap_hand__srv__LeapEffort_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<LeapEffort_Response>);
    fn leap_hand__srv__LeapEffort_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<LeapEffort_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<LeapEffort_Response>) -> bool;
}

// Corresponds to leap_hand__srv__LeapEffort_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct LeapEffort_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub effort: rosidl_runtime_rs::Sequence<f64>,

}



impl Default for LeapEffort_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !leap_hand__srv__LeapEffort_Response__init(&mut msg as *mut _) {
        panic!("Call to leap_hand__srv__LeapEffort_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for LeapEffort_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { leap_hand__srv__LeapEffort_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { leap_hand__srv__LeapEffort_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { leap_hand__srv__LeapEffort_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for LeapEffort_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for LeapEffort_Response where Self: Sized {
  const TYPE_NAME: &'static str = "leap_hand/srv/LeapEffort_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__leap_hand__srv__LeapEffort_Response() }
  }
}


#[link(name = "leap_hand__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__leap_hand__srv__LeapState_Request() -> *const std::ffi::c_void;
}

#[link(name = "leap_hand__rosidl_generator_c")]
extern "C" {
    fn leap_hand__srv__LeapState_Request__init(msg: *mut LeapState_Request) -> bool;
    fn leap_hand__srv__LeapState_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<LeapState_Request>, size: usize) -> bool;
    fn leap_hand__srv__LeapState_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<LeapState_Request>);
    fn leap_hand__srv__LeapState_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<LeapState_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<LeapState_Request>) -> bool;
}

// Corresponds to leap_hand__srv__LeapState_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct LeapState_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for LeapState_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !leap_hand__srv__LeapState_Request__init(&mut msg as *mut _) {
        panic!("Call to leap_hand__srv__LeapState_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for LeapState_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { leap_hand__srv__LeapState_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { leap_hand__srv__LeapState_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { leap_hand__srv__LeapState_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for LeapState_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for LeapState_Request where Self: Sized {
  const TYPE_NAME: &'static str = "leap_hand/srv/LeapState_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__leap_hand__srv__LeapState_Request() }
  }
}


#[link(name = "leap_hand__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__leap_hand__srv__LeapState_Response() -> *const std::ffi::c_void;
}

#[link(name = "leap_hand__rosidl_generator_c")]
extern "C" {
    fn leap_hand__srv__LeapState_Response__init(msg: *mut LeapState_Response) -> bool;
    fn leap_hand__srv__LeapState_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<LeapState_Response>, size: usize) -> bool;
    fn leap_hand__srv__LeapState_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<LeapState_Response>);
    fn leap_hand__srv__LeapState_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<LeapState_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<LeapState_Response>) -> bool;
}

// Corresponds to leap_hand__srv__LeapState_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct LeapState_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub velocity: rosidl_runtime_rs::Sequence<f64>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub effort: rosidl_runtime_rs::Sequence<f64>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub position: rosidl_runtime_rs::Sequence<f64>,

}



impl Default for LeapState_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !leap_hand__srv__LeapState_Response__init(&mut msg as *mut _) {
        panic!("Call to leap_hand__srv__LeapState_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for LeapState_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { leap_hand__srv__LeapState_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { leap_hand__srv__LeapState_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { leap_hand__srv__LeapState_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for LeapState_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for LeapState_Response where Self: Sized {
  const TYPE_NAME: &'static str = "leap_hand/srv/LeapState_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__leap_hand__srv__LeapState_Response() }
  }
}






#[link(name = "leap_hand__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__leap_hand__srv__LeapVelocity() -> *const std::ffi::c_void;
}

// Corresponds to leap_hand__srv__LeapVelocity
#[allow(missing_docs, non_camel_case_types)]
pub struct LeapVelocity;

impl rosidl_runtime_rs::Service for LeapVelocity {
    type Request = LeapVelocity_Request;
    type Response = LeapVelocity_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__leap_hand__srv__LeapVelocity() }
    }
}




#[link(name = "leap_hand__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__leap_hand__srv__LeapPosition() -> *const std::ffi::c_void;
}

// Corresponds to leap_hand__srv__LeapPosition
#[allow(missing_docs, non_camel_case_types)]
pub struct LeapPosition;

impl rosidl_runtime_rs::Service for LeapPosition {
    type Request = LeapPosition_Request;
    type Response = LeapPosition_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__leap_hand__srv__LeapPosition() }
    }
}




#[link(name = "leap_hand__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__leap_hand__srv__LeapEffort() -> *const std::ffi::c_void;
}

// Corresponds to leap_hand__srv__LeapEffort
#[allow(missing_docs, non_camel_case_types)]
pub struct LeapEffort;

impl rosidl_runtime_rs::Service for LeapEffort {
    type Request = LeapEffort_Request;
    type Response = LeapEffort_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__leap_hand__srv__LeapEffort() }
    }
}




#[link(name = "leap_hand__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__leap_hand__srv__LeapState() -> *const std::ffi::c_void;
}

// Corresponds to leap_hand__srv__LeapState
#[allow(missing_docs, non_camel_case_types)]
pub struct LeapState;

impl rosidl_runtime_rs::Service for LeapState {
    type Request = LeapState_Request;
    type Response = LeapState_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__leap_hand__srv__LeapState() }
    }
}


