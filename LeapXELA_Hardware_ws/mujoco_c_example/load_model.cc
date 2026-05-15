#include <mujoco/mujoco.h>

#include <GLFW/glfw3.h>

#include <cstdio>
#include <cstdlib>

namespace {
// MuJoCo state
mjModel* m = nullptr;
mjData* d = nullptr;

// MuJoCo visualization
mjvCamera cam;
mjvOption opt;
mjvScene scn;
mjrContext con;
}  // namespace

int main(int argc, char * argv[])
{
    char err[1024] = {0};
    m = mj_loadXML(
        "/workspace/LeapXELA_Hardware_ws/mujoco_c_example/mjcf/scene.xml",
        /*vfs=*/nullptr, err, sizeof(err));
    if (!m) {
        printf("Failed to load model: %s\n", err);
        return 1;
    }

    d = mj_makeData(m);
    if (!d) {
        printf("Failed to allocate mjData\n");
        mj_deleteModel(m);
        return 1;
    }

    if (!glfwInit()) {
        printf("Failed to init GLFW\n");
        mj_deleteData(d);
        mj_deleteModel(m);
        return 1;
    }

    GLFWwindow* window = glfwCreateWindow(1200, 900, "MuJoCo Viewer (load_model)", nullptr, nullptr);
    if (!window) {
        printf("Failed to create GLFW window\n");
        glfwTerminate();
        mj_deleteData(d);
        mj_deleteModel(m);
        return 1;
    }

    glfwMakeContextCurrent(window);
    glfwSwapInterval(1);

    mjv_defaultCamera(&cam);
    mjv_defaultOption(&opt);
    mjv_defaultScene(&scn);
    mjr_defaultContext(&con);

    mjv_makeScene(m, &scn, 2000);
    mjr_makeContext(m, &con, mjFONTSCALE_150);

    // Reasonable initial camera.
    cam.azimuth = 0;
    cam.elevation = -50.0;
    cam.distance = 1;

    while (!glfwWindowShouldClose(window)) {
        mj_step(m, d);

        // Get framebuffer size and update viewport.
        mjrRect viewport = {0, 0, 0, 0};
        glfwGetFramebufferSize(window, &viewport.width, &viewport.height);

        // Update scene and render.
        mjv_updateScene(m, d, &opt, /*pert=*/nullptr, &cam, mjCAT_ALL, &scn);
        mjr_render(viewport, &scn, &con);

        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    mjr_freeContext(&con);
    mjv_freeScene(&scn);

    glfwDestroyWindow(window);
    glfwTerminate();

    mj_deleteData(d);
    mj_deleteModel(m);

    return 0;
}