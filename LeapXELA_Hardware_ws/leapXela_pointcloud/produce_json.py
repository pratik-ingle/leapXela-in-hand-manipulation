import mujoco as mj
import json


def produce_dict_of_pointcloud_pose(spec):
    pointcloud_dict = {}
    # Navigate to finger
    body = spec.body("finger")
    idx = 0
    for  geom in body.geoms:
        
        if geom.material == "pointcloud_material" and geom.classname.name == "collision":
            idx += 1
            pointcloud_dict[idx] = {
                "pos": geom.pos.tolist(),
                "quat": geom.quat.tolist(),
            }
    print(f"length of pointcloud_dict: {len(pointcloud_dict.keys())}")
    return pointcloud_dict


def write_json(dict, filename):
    with open(filename, "w") as f:
        json.dump(dict, f)



if __name__ == "__main__":
    spec = mj.MjSpec.from_file("robot.xml")
    produce_dict_of_pointcloud_pose(spec)
    write_json(produce_dict_of_pointcloud_pose(spec), "fingertip_magnet_pose.json")