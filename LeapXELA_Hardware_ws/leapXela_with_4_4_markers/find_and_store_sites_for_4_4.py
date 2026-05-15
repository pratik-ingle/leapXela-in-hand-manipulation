import mujoco as mj
import json

map = {

    "leap_hand_xela_back_cover":"palm",

    "p4_unified":"rf_bs",
    "p4_unified_2":"mf_bs",
    "p4_unified_3":"if_bs",

    "p3_unified":"rf_px",
    "p3_unified_2":"mf_px",
    "p3_unified_3":"if_px",

    "p2_unified":"rf_md",
    "p2_unified_2":"mf_md",
    "p2_unified_3":"if_md",

    "finger":"if_ds",
    "finger_2":"mf_ds",
    "finger_3":"rf_ds",

    "thp2_unified":"th_mp",
    "clipper":"th_bs",
    "thp1_unified":"th_px",
    "thfingertip_unified":"th_ds",

}

def find_and_store_sites_for_4_4_on_if(spec):
    sites = {}
    idx = 1
    for geom in spec.geoms:
        if geom.material == "4_4_origin_material" and geom.classname.name == "collision":
         
            sites[f"4_4_{idx}_base_frame"] = {
                "pos": geom.pos.tolist(),
                "quat": geom.quat.tolist(),
                "parent": map[geom.parent.name],
                
            }
            idx += 1
    return sites



def write_sites(sites):
    with open("4_4_sites.json", "w") as f:
        json.dump(sites, f)
    



if __name__ == "__main__":
       spec = mj.MjSpec.from_file("robot.xml")
       sites = find_and_store_sites_for_4_4_on_if(spec)
       write_sites(sites)
    
    
