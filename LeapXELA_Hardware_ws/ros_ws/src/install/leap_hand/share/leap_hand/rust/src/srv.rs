#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};




// Corresponds to leap_hand__srv__LeapVelocity_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct LeapVelocity_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for LeapVelocity_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::LeapVelocity_Request::default())
  }
}

impl rosidl_runtime_rs::Message for LeapVelocity_Request {
  type RmwMsg = super::srv::rmw::LeapVelocity_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
    }
  }
}


// Corresponds to leap_hand__srv__LeapVelocity_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct LeapVelocity_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub velocity: Vec<f64>,

}



impl Default for LeapVelocity_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::LeapVelocity_Response::default())
  }
}

impl rosidl_runtime_rs::Message for LeapVelocity_Response {
  type RmwMsg = super::srv::rmw::LeapVelocity_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        velocity: msg.velocity.into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        velocity: msg.velocity.as_slice().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      velocity: msg.velocity
          .into_iter()
          .collect(),
    }
  }
}


// Corresponds to leap_hand__srv__LeapPosition_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct LeapPosition_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for LeapPosition_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::LeapPosition_Request::default())
  }
}

impl rosidl_runtime_rs::Message for LeapPosition_Request {
  type RmwMsg = super::srv::rmw::LeapPosition_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
    }
  }
}


// Corresponds to leap_hand__srv__LeapPosition_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct LeapPosition_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub position: Vec<f64>,

}



impl Default for LeapPosition_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::LeapPosition_Response::default())
  }
}

impl rosidl_runtime_rs::Message for LeapPosition_Response {
  type RmwMsg = super::srv::rmw::LeapPosition_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        position: msg.position.into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        position: msg.position.as_slice().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      position: msg.position
          .into_iter()
          .collect(),
    }
  }
}


// Corresponds to leap_hand__srv__LeapEffort_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct LeapEffort_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for LeapEffort_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::LeapEffort_Request::default())
  }
}

impl rosidl_runtime_rs::Message for LeapEffort_Request {
  type RmwMsg = super::srv::rmw::LeapEffort_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
    }
  }
}


// Corresponds to leap_hand__srv__LeapEffort_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct LeapEffort_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub effort: Vec<f64>,

}



impl Default for LeapEffort_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::LeapEffort_Response::default())
  }
}

impl rosidl_runtime_rs::Message for LeapEffort_Response {
  type RmwMsg = super::srv::rmw::LeapEffort_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        effort: msg.effort.into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        effort: msg.effort.as_slice().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      effort: msg.effort
          .into_iter()
          .collect(),
    }
  }
}


// Corresponds to leap_hand__srv__LeapState_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct LeapState_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for LeapState_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::LeapState_Request::default())
  }
}

impl rosidl_runtime_rs::Message for LeapState_Request {
  type RmwMsg = super::srv::rmw::LeapState_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
    }
  }
}


// Corresponds to leap_hand__srv__LeapState_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct LeapState_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub velocity: Vec<f64>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub effort: Vec<f64>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub position: Vec<f64>,

}



impl Default for LeapState_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::LeapState_Response::default())
  }
}

impl rosidl_runtime_rs::Message for LeapState_Response {
  type RmwMsg = super::srv::rmw::LeapState_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        velocity: msg.velocity.into(),
        effort: msg.effort.into(),
        position: msg.position.into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        velocity: msg.velocity.as_slice().into(),
        effort: msg.effort.as_slice().into(),
        position: msg.position.as_slice().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      velocity: msg.velocity
          .into_iter()
          .collect(),
      effort: msg.effort
          .into_iter()
          .collect(),
      position: msg.position
          .into_iter()
          .collect(),
    }
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


