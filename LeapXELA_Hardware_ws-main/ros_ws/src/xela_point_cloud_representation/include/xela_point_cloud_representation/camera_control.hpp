#pragma once

#include <GLFW/glfw3.h>
#include <mujoco/mujoco.h>

#include <mutex>

namespace xela_point_cloud_representation
{

// Installs MuJoCo-style GLFW callbacks to control an mjvCamera with mouse drag + scroll.
// Designed to be used with `glfwSetWindowUserPointer(window, this)`.
class CameraControl final
{
public:
  using MoveCameraFn = void (*)(const mjModel *, mjtMouse, mjtNum, mjtNum, const mjvScene *, mjvCamera *);
  using DefaultCameraFn = void (*)(mjvCamera *);

  CameraControl(
    GLFWwindow * window,
    const mjModel * model,
    const mjvScene * scene,
    mjvCamera * camera,
    MoveCameraFn mjv_moveCamera,
    DefaultCameraFn mjv_defaultCamera,
    std::mutex * mj_mutex);

  void install();

private:
  static CameraControl * from(GLFWwindow * window);

  static void cb_mouse_button(GLFWwindow * window, int button, int act, int mods);
  static void cb_mouse_move(GLFWwindow * window, double xpos, double ypos);
  static void cb_scroll(GLFWwindow * window, double xoffset, double yoffset);
  static void cb_keyboard(GLFWwindow * window, int key, int scancode, int act, int mods);

  void on_mouse_button(int button, int act, int mods);
  void on_mouse_move(double xpos, double ypos);
  void on_scroll(double xoffset, double yoffset);
  void on_keyboard(int key, int scancode, int act, int mods);

  GLFWwindow * window_{nullptr};
  const mjModel * model_{nullptr};
  const mjvScene * scene_{nullptr};
  mjvCamera * camera_{nullptr};
  MoveCameraFn mjv_moveCamera_{nullptr};
  DefaultCameraFn mjv_defaultCamera_{nullptr};
  std::mutex * mj_mutex_{nullptr};

  bool button_left_{false};
  bool button_middle_{false};
  bool button_right_{false};
  double lastx_{0.0};
  double lasty_{0.0};
};

}  // namespace xela_point_cloud_representation

