#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};




// Corresponds to xela_server_ros2__srv__XelaSensorStream_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct XelaSensorStream_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub sensor: u8,

}



impl Default for XelaSensorStream_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::XelaSensorStream_Request::default())
  }
}

impl rosidl_runtime_rs::Message for XelaSensorStream_Request {
  type RmwMsg = super::srv::rmw::XelaSensorStream_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        sensor: msg.sensor,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      sensor: msg.sensor,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      sensor: msg.sensor,
    }
  }
}


// Corresponds to xela_server_ros2__srv__XelaSensorStream_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct XelaSensorStream_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub data: Vec<super::msg::SensorFull>,

}



impl Default for XelaSensorStream_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::XelaSensorStream_Response::default())
  }
}

impl rosidl_runtime_rs::Message for XelaSensorStream_Response {
  type RmwMsg = super::srv::rmw::XelaSensorStream_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        data: msg.data
          .into_iter()
          .map(|elem| super::msg::SensorFull::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        data: msg.data
          .iter()
          .map(|elem| super::msg::SensorFull::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      data: msg.data
          .into_iter()
          .map(super::msg::SensorFull::from_rmw_message)
          .collect(),
    }
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


