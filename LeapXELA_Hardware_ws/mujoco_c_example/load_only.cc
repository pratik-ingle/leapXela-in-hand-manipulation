#include <mujoco/mujoco.h>

#include <cstdio>

int main(int argc, char** argv) {
  const char* xml = (argc >= 2) ? argv[1] : "";
  if (!xml || !xml[0]) {
    std::fprintf(stderr, "usage: %s /path/to/model.xml\n", argv[0]);
    return 2;
  }

  char err[1024] = {0};
  mjModel* m = mj_loadXML(xml, /*vfs=*/nullptr, err, sizeof(err));
  if (!m) {
    std::fprintf(stderr, "mj_loadXML failed: %s\n", err);
    return 1;
  }

  mjData* d = mj_makeData(m);
  if (!d) {
    std::fprintf(stderr, "mj_makeData failed\n");
    mj_deleteModel(m);
    return 1;
  }

  // Touch a tiny bit of simulation to ensure model/data are valid.
  mj_step(m, d);

  mj_deleteData(d);
  mj_deleteModel(m);
  return 0;
}

