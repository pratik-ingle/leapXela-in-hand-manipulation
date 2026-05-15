#include <xela_point_cloud_representation/camera_control.hpp>

#include <algorithm>

namespace xela_point_cloud_representation
{

CameraControl::CameraControl(
  GLFWwindow * window,
  const mjModel * model,
  const mjvScene * scene,
  mjvCamera * camera,
  MoveCameraFn mjv_moveCamera,
  DefaultCameraFn mjv_defaultCamera,
  std::mutex * mj_mutex)
: window_(window),
  model_(model),
  scene_(scene),
  camera_(camera),
  mjv_moveCamera_(mjv_moveCamera),
  mjv_defaultCamera_(mjv_defaultCamera),
  mj_mutex_(mj_mutex)
{
}

void CameraControl::install()
{
  if (!window_) {
    return;
  }
  glfwSetWindowUserPointer(window_, this);
  glfwSetMouseButtonCallback(window_, &CameraControl::cb_mouse_button);
  glfwSetCursorPosCallback(window_, &CameraControl::cb_mouse_move);
  glfwSetScrollCallback(window_, &CameraControl::cb_scroll);
  glfwSetKeyCallback(window_, &CameraControl::cb_keyboard);
}

CameraControl * CameraControl::from(GLFWwindow * window)
{
  return window ? static_cast<CameraControl *>(glfwGetWindowUserPointer(window)) : nullptr;
}

void CameraControl::cb_mouse_button(GLFWwindow * window, int button, int act, int mods)
{
  if (auto * self = from(window)) {
    self->on_mouse_button(button, act, mods);
  }
}

void CameraControl::cb_mouse_move(GLFWwindow * window, double xpos, double ypos)
{
  if (auto * self = from(window)) {
    self->on_mouse_move(xpos, ypos);
  }
}

void CameraControl::cb_scroll(GLFWwindow * window, double xoffset, double yoffset)
{
  if (auto * self = from(window)) {
    self->on_scroll(xoffset, yoffset);
  }
}

void CameraControl::cb_keyboard(GLFWwindow * window, int key, int scancode, int act, int mods)
{
  if (auto * self = from(window)) {
    self->on_keyboard(key, scancode, act, mods);
  }
}

void CameraControl::on_mouse_button(int /*button*/, int /*act*/, int /*mods*/)
{
  if (!window_) {
    return;
  }

  button_left_ = (glfwGetMouseButton(window_, GLFW_MOUSE_BUTTON_LEFT) == GLFW_PRESS);
  button_middle_ = (glfwGetMouseButton(window_, GLFW_MOUSE_BUTTON_MIDDLE) == GLFW_PRESS);
  button_right_ = (glfwGetMouseButton(window_, GLFW_MOUSE_BUTTON_RIGHT) == GLFW_PRESS);

  glfwGetCursorPos(window_, &lastx_, &lasty_);
}

void CameraControl::on_mouse_move(double xpos, double ypos)
{
  if (!model_ || !scene_ || !camera_ || !mjv_moveCamera_) {
    return;
  }

  if (!button_left_ && !button_middle_ && !button_right_) {
    return;
  }

  const double dx = xpos - lastx_;
  const double dy = ypos - lasty_;
  lastx_ = xpos;
  lasty_ = ypos;

  int width = 0;
  int height = 0;
  glfwGetWindowSize(window_, &width, &height);
  height = std::max(1, height);

  const bool mod_shift =
    (glfwGetKey(window_, GLFW_KEY_LEFT_SHIFT) == GLFW_PRESS) ||
    (glfwGetKey(window_, GLFW_KEY_RIGHT_SHIFT) == GLFW_PRESS);

  mjtMouse action;
  if (button_right_) {
    action = mod_shift ? mjMOUSE_MOVE_H : mjMOUSE_MOVE_V;
  } else if (button_left_) {
    action = mod_shift ? mjMOUSE_ROTATE_H : mjMOUSE_ROTATE_V;
  } else {
    action = mjMOUSE_ZOOM;
  }

  if (mj_mutex_) {
    std::lock_guard<std::mutex> lk(*mj_mutex_);
    mjv_moveCamera_(model_, action, dx / height, dy / height, scene_, camera_);
  } else {
    mjv_moveCamera_(model_, action, dx / height, dy / height, scene_, camera_);
  }
}

void CameraControl::on_scroll(double /*xoffset*/, double yoffset)
{
  if (!model_ || !scene_ || !camera_ || !mjv_moveCamera_) {
    return;
  }

  if (mj_mutex_) {
    std::lock_guard<std::mutex> lk(*mj_mutex_);
    mjv_moveCamera_(model_, mjMOUSE_ZOOM, 0.0, -0.05 * yoffset, scene_, camera_);
  } else {
    mjv_moveCamera_(model_, mjMOUSE_ZOOM, 0.0, -0.05 * yoffset, scene_, camera_);
  }
}

void CameraControl::on_keyboard(int key, int /*scancode*/, int act, int /*mods*/)
{
  if (act != GLFW_PRESS) {
    return;
  }

  // Backspace: reset camera to MuJoCo defaults (and keep USER camera mode).
  if (key == GLFW_KEY_BACKSPACE && mjv_defaultCamera_ && camera_) {
    if (mj_mutex_) {
      std::lock_guard<std::mutex> lk(*mj_mutex_);
      mjv_defaultCamera_(camera_);
      camera_->type = mjCAMERA_FREE;
    } else {
      mjv_defaultCamera_(camera_);
      camera_->type = mjCAMERA_FREE;
    }
  }
}

}  // namespace xela_point_cloud_representation

