
import mujoco as mj
import pprint
import json

# [x_min, x_max, y_min, y_max, z_min, z_max]
SLIDER_JOINT_LIMITS = [(-0.0025, 0.0025), (-0.0025, 0.0025), (-0.0025, 0.0025)]


def load_fingertip_magnet_pose():
    with open("fingertip_magnet_pose.json", "r") as f:
        return json.load(f)
    return None

def remove_contact_detection_between_grid_elements_of_sensor(spec,geoms_name):
    for geom_name in geoms_name:
        for other_geom_name in geoms_name:
            if geom_name != other_geom_name:
                spec.add_exclude(bodyname1 = geom_name, bodyname2 = other_geom_name)

def make_visual_geoms_of_the_hand_transparent(spec):
    m = spec.material("black")
    rgba = m.rgba
    rgba[3] = 0.2
    print(spec.material("black").rgba)

def remove_collsions_geom_convering_sensors_except_for_finger(spec):
    for idx in range(3):
        name = f"uspa46_{idx+1}"
        geom = spec.geom(name)
        spec.delete(geom)
    
    for finger in ["if", "mf", "rf"]:
        name = f"{finger}_bs_uspa44"
        geom = spec.geom(name)
        spec.delete(geom)
        name = f"{finger}_px_uspa44"
        geom = spec.geom(name)
        spec.delete(geom)
        name = f"{finger}_md_uspa44"
        geom = spec.geom(name)
        spec.delete(geom)
    
    # thumb
    name = "th_px_uspa44"
    geom = spec.geom(name)
    spec.delete(geom)
    name = "th_ds_uspa44"
    geom = spec.geom(name)
    spec.delete(geom)

    ####thumb fingertips####
    name = "th_ds_tip"
    geom = spec.geom(name)
    spec.delete(geom)
    for idx in range(2,7):
        name = f"th_ds_tip_{idx}"
        geom = spec.geom(name)
        spec.delete(geom)
    ####fingers fingertips####
    for finger in ["if", "mf", "rf"]:
        name = f"{finger}_ds_tip"
        geom = spec.geom(name)
        spec.delete(geom)
        for idx in range(2,7):
            name = f"{finger}_ds_tip_{idx}"
            geom = spec.geom(name)
            spec.delete(geom)

def remove_collision_geoms_of_the_hand(spec):
    for geom in spec.geoms:
        if "collision" in geom.name:
            spec.delete(geom)

def add_sensor_patch_defaults_for_if_mf_rf(spec,sensor_patch_default):

    sensor_patch_default_dict = {}
    sensor_patch_params = {}  # Store pos and euler for each default
    
    # top surface
    locations = [([0.01, -0.035, 0.0145],[0,0,0]),
                ([0.0100, -0.045, 0.0145],[0,0,0]),
                ([0.004, -0.057, 0.0145],[0,0,0.7])]
    for idx,loc in enumerate(locations):
        pos,euler = loc
        ref = spec.add_default(f"fingertip_sensor_top_surface_{idx+1}",sensor_patch_default)
        ref.geom.pos = pos
        # Note: euler cannot be set on geom defaults, will be set when adding geom

        sensor_patch_default_dict[f"fingertip_sensor_top_surface_{idx+1}"] = ref
        sensor_patch_params[f"fingertip_sensor_top_surface_{idx+1}"] = {"pos": pos, "euler": euler}
    
    # left surface
    locations = [([0.007, -0.035, 0.023],[0,-0.9,0]),
                ([0.007, -0.045, 0.023],[0,-0.9,0])]
    for idx,loc in enumerate(locations):
        pos,euler = loc
        ref = spec.add_default(f"fingertip_sensor_left_surface_{idx+1}",sensor_patch_default)
        ref.geom.pos = pos
        # Note: euler cannot be set on geom defaults, will be set when adding geom

        sensor_patch_default_dict[f"fingertip_sensor_left_surface_{idx+1}"] = ref
        sensor_patch_params[f"fingertip_sensor_left_surface_{idx+1}"] = {"pos": pos, "euler": euler}
    
    # right surface
    locations = [([0.007, -0.035, 0.006],[0,0.9,0]),
                ([0.007, -0.045, 0.006],[0,0.9,0])]
    for idx,loc in enumerate(locations):
        pos,euler = loc
        ref = spec.add_default(f"fingertip_sensor_right_surface_{idx+1}",sensor_patch_default)
        ref.geom.pos = pos
        # Note: euler cannot be set on geom defaults, will be set when adding geom

        sensor_patch_default_dict[f"fingertip_sensor_right_surface_{idx+1}"] = ref
        sensor_patch_params[f"fingertip_sensor_right_surface_{idx+1}"] = {"pos": pos, "euler": euler}

    return sensor_patch_default_dict, sensor_patch_params

def add_sensor_patch_to_fingertip(spec,fingertip_magnet_pose, finger_name, sensor_default = None):
    contacts_bodies = []
    joints = {}
    link_name = f"{finger_name}_ds"
    joints[link_name] = {}
    
    for idx in range(0,30):
        joints[link_name][str(idx+1)] = {}
        pos,quat = fingertip_magnet_pose[str(idx+1)]["pos"],fingertip_magnet_pose[str(idx+1)]["quat"]
        name = f"{finger_name}_sensor_{idx+1}"
        child = spec.body(f"{finger_name}_ds").add_body(name=name,pos=pos,
            quat=quat)
        child.add_geom(
            name=f"{finger_name}_sensor_{idx+1}",
            size=[0.0025, 0.0025, 0.0025],
            pos=[0,0,0],
            type=mj.mjtGeom.mjGEOM_SPHERE,
            default=sensor_default
        )
        axis_name = "not_set"
        for axis in [[1,0,0],[0,1,0],[0,0,1]]:
            if axis[0] == 1:
                limit = SLIDER_JOINT_LIMITS[0]
                axis_name = "x"
            elif axis[1] == 1:
                limit = SLIDER_JOINT_LIMITS[1]
                axis_name = "y"
            elif axis[2] == 1:
                limit = SLIDER_JOINT_LIMITS[2]
                axis_name = "z"
            else:
                raise ValueError(f"Invalid axis: {axis}")
            joint = child.add_joint(type=mj.mjtJoint.mjJNT_SLIDE,name=name+f"_slide_{axis_name}",axis=axis,range=limit)
            joints[link_name][str(idx+1)][axis_name] = joint.name
        
        contacts_bodies.append(child.name)
    # remove contact detection between grid elements of sensor
    remove_contact_detection_between_grid_elements_of_sensor(spec,contacts_bodies)
    return joints

def add_uspa44(spec, site_name,link_name,sensor_default):
    contacts_bodies = []
    joints = {}
    joints[site_name] = {}

    site_x0_y0 = spec.site(site_name)
    sites_parent_body = site_x0_y0.parent
    x,y,z = site_x0_y0.pos
    if link_name == "bs":
        y += 0.0025
        euler=[1.57,0,0]    
    elif link_name == "px":
        z -= 0.0025
        euler=[0,0,0] 
    elif link_name == "md":
        y -= 0.0025
        euler=[-1.57,0,-1.57] 
    elif link_name == "th_px":
        y -= 0.0025
        euler=[0,-1.57,0] 
    elif link_name == "th_ds":
        x += 0.0025
        euler=[0,1.57,2*1.57] 

    
    offset = 0.0025*2
    for j in range(4):
        for i in range(4):
            loc = str(i)+"_"+str(j)
            joints[site_name][loc] = {}
            pos = None
            if link_name in ["bs", "md"]:
                pos = [x - offset * i, y, z - offset * j]
            elif link_name =="px":
                pos = [x - offset * j , y - offset * i, z ]
            elif link_name == "th_px":
                pos = [x  , y - offset * i, z - offset * j]       
            elif link_name == "th_ds":
                pos = [x  , y + offset * i, z - offset * j]

            name = f"{site_name}_sensor_patch_{i}_{j}"
            child = sites_parent_body.add_body(name=name,pos=pos,euler=euler)
            child.add_geom(
                name=f"{site_name}_sensor_patch_{i}_{j}",
                type=mj.mjtGeom.mjGEOM_SPHERE,
                size=[0.0025, 0.0025, 0.0025],
                pos=[0,0,0],
                default=sensor_default
            )
            axis_name = "not_set"
            for axis in [[1,0,0],[0,1,0],[0,0,1]]:
                if axis[0] == 1:
                    limit = SLIDER_JOINT_LIMITS[0]
                    axis_name = "x"
                elif axis[1] == 1:
                    limit = SLIDER_JOINT_LIMITS[1]
                    axis_name = "y"
                elif axis[2] == 1:
                    limit = SLIDER_JOINT_LIMITS[2]
                    axis_name = "z"
                else:
                    raise ValueError(f"Invalid axis: {axis}")
                joint = child.add_joint(type=mj.mjtJoint.mjJNT_SLIDE,name=name+f"_slide_{axis_name}",axis=axis,range=limit)
                joints[site_name][loc][axis_name] = joint.name
            contacts_bodies.append(child.name)
    # remove contact detection between grid elements of sensor
    remove_contact_detection_between_grid_elements_of_sensor(spec,contacts_bodies)

    return joints

def add_uspa46(spec, site_name,sensor_default):
    link_name = site_name
    contacts_bodies = []
    joints = {}
    joints[link_name] = {}

    site_x0_y0 = spec.site(site_name)
    sites_parent_body = site_x0_y0.parent
    x,y,z = site_x0_y0.pos

    x_offset = 0.004*2
    z_offset = 0.0035*2
    y += 0.0025

    size=[0.0025, 0.0025, 0.0035]
    contacts_bodies = []
    for j in range(4):
        for i in range(6):
            loc = str(i)+"_"+str(j)
            joints[link_name][loc] = {}
            name = f"{site_name}_sensor_patch_{i}_{j}"
            child = sites_parent_body.add_body(name=name,pos=[x - x_offset * i, y , z - z_offset * j],euler=[1.57,0,0])
            child.add_geom(
                name=f"{site_name}_sensor_patch_{i}_{j}",
                type=mj.mjtGeom.mjGEOM_SPHERE,
                size = size,
                pos=[0,0,0],
                default=sensor_default
            )
            axis_name = "not_set"
            for axis in [[1,0,0],[0,1,0],[0,0,1]]:
                if axis[0] == 1:
                    limit = SLIDER_JOINT_LIMITS[0]
                    axis_name = "x"
                elif axis[1] == 1:
                    limit = SLIDER_JOINT_LIMITS[1]
                    axis_name = "y"
                elif axis[2] == 1:
                    limit = SLIDER_JOINT_LIMITS[2]
                    axis_name = "z"
                else:
                    raise ValueError(f"Invalid axis: {axis}")
                joint = child.add_joint(type=mj.mjtJoint.mjJNT_SLIDE,name=name+f"_slide_{axis_name}",axis=axis,range=limit)
                joints[link_name][loc][axis_name] = joint.name
            contacts_bodies.append(child.name)
    # remove contact detection between grid elements of sensor
    remove_contact_detection_between_grid_elements_of_sensor(spec,contacts_bodies)

    return joints

def write_xml_model(spec):
  xml = spec.to_xml()
  
  with open("leapXela_touch_point_cloud.xml", "w") as f:
    f.write(xml)

def write_scene_xml(spec):
    template = f"""
    <mujoco model="scene_touch_point_cloud">
        <include file="leapXela_touch_point_cloud.xml"/>
        <statistic extent=".6" />
        <visual>
            <headlight diffuse="0.6 0.6 0.6" ambient="0.3 0.3 0.3" specular="0 0 0" />
            <rgba haze="0.15 0.25 0.35 1" />
            <global azimuth="180" elevation="-50"/>
        </visual>

        <asset>
            <texture type="skybox" builtin="gradient" rgb1="0.3 0.5 0.7" rgb2="0 0 0" width="512"
                height="3072" />
            <texture type="2d" name="groundplane" builtin="checker" mark="edge" rgb1="0.2 0.3 0.4"
                rgb2="0.1 0.2 0.3"
                markrgb="0.8 0.8 0.8" width="300" height="300" />
            <material name="groundplane" texture="groundplane" texuniform="true" texrepeat="5 5"
                reflectance="0.2" />
        </asset>

        <worldbody>
            <light pos="0 0 3.5" dir="0 0 -1" directional="true" />
            <geom name="floor" size="0 0 0.05" pos="0 0 0" type="plane" material="groundplane" />
        </worldbody>

    </mujoco>
    """
    with open("scene_touch_point_cloud.xml", "w") as f:
        f.write(template)

def wrtie_sensor_joints_to_json(joints):
    with open("sensor_joints.json", "w") as f:
        json.dump(joints, f)

if __name__ == "__main__":
    spec = mj.MjSpec.from_file("leapXela_base_model.xml")
    fingertip_magnet_pose = load_fingertip_magnet_pose()
    site_names = ["if_bs_uspa44", "mf_bs_uspa44" ,"rf_bs_uspa44",
                  "if_md_uspa44", "mf_md_uspa44" ,"rf_md_uspa44",
                  "if_px_uspa44", "mf_px_uspa44" ,"rf_px_uspa44",
                  
     ]
    th_site_names = ["th_px_uspa44","th_ds_uspa44"]
    palm_site_names = ["uspa46_1", "uspa46_2" ,"uspa46_3"]

    collision_default = spec.geom("if_ds_collision_1").classname
    

    # add sensor_patch to collision default
    sensor_patch_default = spec.add_default("sensor_patch",collision_default)
    sensor_patch_default.geom.size=[0.005, 0.005, 0.005]
    sensor_patch_default.geom.rgba=[1, 0, 0, 1]
    sensor_patch_default.geom.group=2

    make_visual_geoms_of_the_hand_transparent(spec)

    remove_collsions_geom_convering_sensors_except_for_finger(spec)
    remove_collision_geoms_of_the_hand(spec)

    joints = {}
 
    # add sensor_patch to finger links
    for site_name in site_names:
        if "bs" in site_name:
            joints[site_name] = add_uspa44(spec, site_name,"bs",sensor_patch_default)[site_name]
        elif "md" in site_name:
            joints[site_name] = add_uspa44(spec, site_name,"md",sensor_patch_default)[site_name]
        elif "px" in site_name:
            joints[site_name] = add_uspa44(spec, site_name,"px",sensor_patch_default)[site_name]
    sensor_patch_default_dict, sensor_patch_params = add_sensor_patch_defaults_for_if_mf_rf(spec,sensor_patch_default)
    for finger in ["if", "mf", "rf","th"]:
        joints[f"{finger}_ds"] = add_sensor_patch_to_fingertip(spec,fingertip_magnet_pose,finger,sensor_patch_default)[f"{finger}_ds"]
    # add sensor_patch to thumb links
    for site_name in th_site_names:
        if "th_ds" in site_name:
            joints[site_name] = add_uspa44(spec, site_name,"th_ds",sensor_patch_default)[site_name]
        elif "th_px" in site_name:
            joints[site_name] = add_uspa44(spec, site_name,"th_px",sensor_patch_default)[site_name]
   
    
    # add sensor_patch to palm
    for site_name in palm_site_names:
        joints[site_name] = add_uspa46(spec, site_name,sensor_patch_default)[site_name]
    # print(joints.keys())
    # pprint.pprint(joints["if_bs_uspa44"])
    wrtie_sensor_joints_to_json(joints)
    write_xml_model(spec)
    write_scene_xml(spec)