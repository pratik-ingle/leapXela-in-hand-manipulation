#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



#[link(name = "xela_server_ros2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__xela_server_ros2__srv__XelaSensorStream_Request() -> *const std::ffi::c_void;
}

#[link(name = "xela_server_ros2__rosidl_generator_c")]
extern "C" {
    fn xela_server_ros2__srv__XelaSensorStream_Request__init(msg: *mut XelaSensorStream_Request) -> bool;
    fn xela_server_ros2__srv__XelaSensorStream_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<XelaSensorStream_Request>, size: usize) -> bool;
    fn xela_server_ros2__srv__XelaSensorStream_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<XelaSensorStream_Request>);
    fn xela_server_ros2__srv__XelaSensorStream_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<XelaSensorStream_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<XelaSensorStream_Request>) -> bool;
}

// Corresponds to xela_server_ros2__srv__XelaSensorStream_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct XelaSensorStream_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub sensor: u8,

}



impl Default for XelaSensorStream_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !xela_server_ros2__srv__XelaSensorStream_Request__init(&mut msg as *mut _) {
        panic!("Call to xela_server_ros2__srv__XelaSensorStream_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for XelaSensorStream_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { xela_server_ros2__srv__XelaSensorStream_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { xela_server_ros2__srv__XelaSensorStream_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { xela_server_ros2__srv__XelaSensorStream_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for XelaSensorStream_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for XelaSensorStream_Request where Self: Sized {
  const TYPE_NAME: &'static str = "xela_server_ros2/srv/XelaSensorStream_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__xela_server_ros2__srv__XelaSensorStream_Request() }
  }
}


#[link(name = "xela_server_ros2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__xela_server_ros2__srv__XelaSensorStream_Response() -> *const std::ffi::c_void;
}

#[link(name = "xela_server_ros2__rosidl_generator_c")]
extern "C" {
    fn xela_server_ros2__srv__XelaSensorStream_Response__init(msg: *mut XelaSensorStream_Response) -> bool;
    fn xela_server_ros2__srv__XelaSensorStream_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<XelaSensorStream_Response>, size: usize) -> bool;
    fn xela_server_ros2__srv__XelaSensorStream_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<XelaSensorStream_Response>);
    fn xela_server_ros2__srv__XelaSensorStream_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<XelaSensorStream_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<XelaSensorStream_Response>) -> bool;
}

// Corresponds to xela_server_ros2__srv__XelaSensorStream_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct XelaSensorStream_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub data: rosidl_runtime_rs::Sequence<super::super::msg::rmw::SensorFull>,

}



impl Default for XelaSensorStream_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !xela_server_ros2__srv__XelaSensorStream_Response__init(&mut msg as *mut _) {
        panic!("Call to xela_server_ros2__srv__XelaSensorStream_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for XelaSensorStream_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { xela_server_ros2__srv__XelaSensorStream_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { xela_server_ros2__srv__XelaSensorStream_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { xela_server_ros2__srv__XelaSensorStream_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for XelaSensorStream_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for XelaSensorStream_Response where Self: Sized {
  const TYPE_NAME: &'static str = "xela_server_ros2/srv/XelaSensorStream_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__xela_server_ros2__srv__XelaSensorStream_Response() }
  }
}






#[link(name = "xela_server_ros2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__xela_server_ros2__srv__XelaSensorStream() -> *const std::ffi::c_void;
}

// Corresponds to xela_server_ros2__srv__XelaSensorStream
#[allow(missing_docs, non_camel_case_types)]
pub struct XelaSensorStream;

impl rosidl_runtime_rs::Service for XelaSensorStream {
    type Request = XelaSensorStream_Request;
    type Response = XelaSensorStream_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__xela_server_ros2__srv__XelaSensorStream() }
    }
}


