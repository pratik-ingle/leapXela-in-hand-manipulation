#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



// Corresponds to xela_server_ros2__msg__SensorFull

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
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
    pub model: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub sensor_pos: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub taxels: Vec<super::msg::Taxel>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub forces: Vec<super::msg::Forces>,

}



impl Default for SensorFull {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::SensorFull::default())
  }
}

impl rosidl_runtime_rs::Message for SensorFull {
  type RmwMsg = super::msg::rmw::SensorFull;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        message: msg.message,
        time: msg.time,
        model: msg.model.as_str().into(),
        sensor_pos: msg.sensor_pos,
        taxels: msg.taxels
          .into_iter()
          .map(|elem| super::msg::Taxel::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
        forces: msg.forces
          .into_iter()
          .map(|elem| super::msg::Forces::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      message: msg.message,
      time: msg.time,
        model: msg.model.as_str().into(),
      sensor_pos: msg.sensor_pos,
        taxels: msg.taxels
          .iter()
          .map(|elem| super::msg::Taxel::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
        forces: msg.forces
          .iter()
          .map(|elem| super::msg::Forces::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      message: msg.message,
      time: msg.time,
      model: msg.model.to_string(),
      sensor_pos: msg.sensor_pos,
      taxels: msg.taxels
          .into_iter()
          .map(super::msg::Taxel::from_rmw_message)
          .collect(),
      forces: msg.forces
          .into_iter()
          .map(super::msg::Forces::from_rmw_message)
          .collect(),
    }
  }
}


// Corresponds to xela_server_ros2__msg__SensStream

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SensStream {

    // This member is not documented.
    #[allow(missing_docs)]
    pub sensors: Vec<super::msg::SensorFull>,

}



impl Default for SensStream {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::SensStream::default())
  }
}

impl rosidl_runtime_rs::Message for SensStream {
  type RmwMsg = super::msg::rmw::SensStream;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        sensors: msg.sensors
          .into_iter()
          .map(|elem| super::msg::SensorFull::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        sensors: msg.sensors
          .iter()
          .map(|elem| super::msg::SensorFull::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      sensors: msg.sensors
          .into_iter()
          .map(super::msg::SensorFull::from_rmw_message)
          .collect(),
    }
  }
}


// Corresponds to xela_server_ros2__msg__Taxel

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::Taxel::default())
  }
}

impl rosidl_runtime_rs::Message for Taxel {
  type RmwMsg = super::msg::rmw::Taxel;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        x: msg.x,
        y: msg.y,
        z: msg.z,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      x: msg.x,
      y: msg.y,
      z: msg.z,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      x: msg.x,
      y: msg.y,
      z: msg.z,
    }
  }
}


// Corresponds to xela_server_ros2__msg__Forces

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::Forces::default())
  }
}

impl rosidl_runtime_rs::Message for Forces {
  type RmwMsg = super::msg::rmw::Forces;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        x: msg.x,
        y: msg.y,
        z: msg.z,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      x: msg.x,
      y: msg.y,
      z: msg.z,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      x: msg.x,
      y: msg.y,
      z: msg.z,
    }
  }
}


