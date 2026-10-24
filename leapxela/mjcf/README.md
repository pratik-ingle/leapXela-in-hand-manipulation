# LeapXELA MuJoCo models

Upstream author of `leapXela_base_model.xml`, `robot.urdf` and the `assets/`
mesh set: **Mohammad <mohammad200h@hotmail.com>** (exported with
onshape-to-robot; see `config.json` for the CAD document URL).

## Live inputs

Only three files here feed the current flex-taxel pipeline:

| file | read by |
|---|---|
| `leapXela_base_model.xml` | `hand_builder.load_base_model(mode != "touchgrid")` — the hand the flex skin is built onto |
| `robot_touch_sensor_array_binary_touchgrid_generated.xml` | `hand_builder.load_base_model(mode == "touchgrid")` |
| `joint_config.json` | `action_trajectory.py` — per-joint limits and the hardware motor-ID order |

`assets/` must stay a sibling of the XMLs: `leapXela_base_model.xml` declares
`meshdir="./assets/"`, and `reorientation_cube*.xml` reach their meshes as
`./meshes/*.obj` resolved through that same `meshdir`.

## Everything else

The remaining XMLs are outputs or inputs of abandoned sensor approaches kept for
reference — raycast (`leapXela_touch_sensor_made_of_rays.xml`), site-array
(`robot_touch_sensor_array_*.xml`), MJX simplification (`*_mjx*.xml`), and the
bubble sensor. Their generators live in `leapxela/legacy/`. `textures/` is used
only by `legacy/simplify_model_for_mjx.py`.

`hand_builder.py` writes its generated model, scene and heatmaps to
`data/leapxela_generated/`, not back into this directory.
