#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "xela_server_ros2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__xela_server_ros2__msg__SensorFull() -> *const std::ffi::c_void;
}

#[link(name = "xela_server_ros2__rosidl_generator_c")]
extern "C" {
    fn xela_server_ros2__msg__SensorFull__init(msg: *mut SensorFull) -> bool;
    fn xela_server_ros2__msg__SensorFull__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SensorFull>, size: usize) -> bool;
    fn xela_server_ros2__msg__SensorFull__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SensorFull>);
    fn xela_server_ros2__msg__SensorFull__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SensorFull>, out_seq: *mut rosidl_runtime_rs::Sequence<SensorFull>) -> bool;
}

// Corresponds to xela_server_ros2__msg__SensorFull
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SensorFull {

    // This member is not documented.
    #[allow(missing_docs)]
    pub message: u32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub time: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub model: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub sensor_pos: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub taxels: rosidl_runtime_rs::Sequence<super::super::msg::rmw::Taxel>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub forces: rosidl_runtime_rs::Sequence<super::super::msg::rmw::Forces>,

}



impl Default for SensorFull {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !xela_server_ros2__msg__SensorFull__init(&mut msg as *mut _) {
        panic!("Call to xela_server_ros2__msg__SensorFull__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SensorFull {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { xela_server_ros2__msg__SensorFull__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { xela_server_ros2__msg__SensorFull__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { xela_server_ros2__msg__SensorFull__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SensorFull {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SensorFull where Self: Sized {
  const TYPE_NAME: &'static str = "xela_server_ros2/msg/SensorFull";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__xela_server_ros2__msg__SensorFull() }
  }
}


#[link(name = "xela_server_ros2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__xela_server_ros2__msg__SensStream() -> *const std::ffi::c_void;
}

#[link(name = "xela_server_ros2__rosidl_generator_c")]
extern "C" {
    fn xela_server_ros2__msg__SensStream__init(msg: *mut SensStream) -> bool;
    fn xela_server_ros2__msg__SensStream__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SensStream>, size: usize) -> bool;
    fn xela_server_ros2__msg__SensStream__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SensStream>);
    fn xela_server_ros2__msg__SensStream__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SensStream>, out_seq: *mut rosidl_runtime_rs::Sequence<SensStream>) -> bool;
}

// Corresponds to xela_server_ros2__msg__SensStream
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SensStream {

    // This member is not documented.
    #[allow(missing_docs)]
    pub sensors: rosidl_runtime_rs::Sequence<super::super::msg::rmw::SensorFull>,

}



impl Default for SensStream {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !xela_server_ros2__msg__SensStream__init(&mut msg as *mut _) {
        panic!("Call to xela_server_ros2__msg__SensStream__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SensStream {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { xela_server_ros2__msg__SensStream__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { xela_server_ros2__msg__SensStream__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { xela_server_ros2__msg__SensStream__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SensStream {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SensStream where Self: Sized {
  const TYPE_NAME: &'static str = "xela_server_ros2/msg/SensStream";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__xela_server_ros2__msg__SensStream() }
  }
}


#[link(name = "xela_server_ros2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__xela_server_ros2__msg__Taxel() -> *const std::ffi::c_void;
}

#[link(name = "xela_server_ros2__rosidl_generator_c")]
extern "C" {
    fn xela_server_ros2__msg__Taxel__init(msg: *mut Taxel) -> bool;
    fn xela_server_ros2__msg__Taxel__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Taxel>, size: usize) -> bool;
    fn xela_server_ros2__msg__Taxel__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Taxel>);
    fn xela_server_ros2__msg__Taxel__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Taxel>, out_seq: *mut rosidl_runtime_rs::Sequence<Taxel>) -> bool;
}

// Corresponds to xela_server_ros2__msg__Taxel
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Taxel {

    // This member is not documented.
    #[allow(missing_docs)]
    pub x: u16,


    // This member is not documented.
    #[allow(missing_docs)]
    pub y: u16,


    // This member is not documented.
    #[allow(missing_docs)]
    pub z: u16,

}



impl Default for Taxel {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !xela_server_ros2__msg__Taxel__init(&mut msg as *mut _) {
        panic!("Call to xela_server_ros2__msg__Taxel__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Taxel {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { xela_server_ros2__msg__Taxel__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { xela_server_ros2__msg__Taxel__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { xela_server_ros2__msg__Taxel__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Taxel {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Taxel where Self: Sized {
  const TYPE_NAME: &'static str = "xela_server_ros2/msg/Taxel";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__xela_server_ros2__msg__Taxel() }
  }
}


#[link(name = "xela_server_ros2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__xela_server_ros2__msg__Forces() -> *const std::ffi::c_void;
}

#[link(name = "xela_server_ros2__rosidl_generator_c")]
extern "C" {
    fn xela_server_ros2__msg__Forces__init(msg: *mut Forces) -> bool;
    fn xela_server_ros2__msg__Forces__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Forces>, size: usize) -> bool;
    fn xela_server_ros2__msg__Forces__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Forces>);
    fn xela_server_ros2__msg__Forces__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Forces>, out_seq: *mut rosidl_runtime_rs::Sequence<Forces>) -> bool;
}

// Corresponds to xela_server_ros2__msg__Forces
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Forces {

    // This member is not documented.
    #[allow(missing_docs)]
    pub x: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub y: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub z: f32,

}



impl Default for Forces {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !xela_server_ros2__msg__Forces__init(&mut msg as *mut _) {
        panic!("Call to xela_server_ros2__msg__Forces__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Forces {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { xela_server_ros2__msg__Forces__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { xela_server_ros2__msg__Forces__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { xela_server_ros2__msg__Forces__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Forces {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Forces where Self: Sized {
  const TYPE_NAME: &'static str = "xela_server_ros2/msg/Forces";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__xela_server_ros2__msg__Forces() }
  }
}


