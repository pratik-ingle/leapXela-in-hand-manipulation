import json
import numpy as np
import pprint

LEAP_XELA_ID = np.array(
    [
        [6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 0, 1, 2, 3, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6],
        [6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 4, 5, 6, 7, 8, 6e6, 9, 10, 11, 12, 6e6, 13, 14, 15, 16],
        [6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 17, 18, 19, 20, 21, 22, 6e6, 23, 24, 25, 26, 6e6, 27, 28, 29, 30],
        [6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 31, 32, 33, 34, 35, 36, 6e6, 37, 38, 39, 40, 6e6, 41, 42, 43, 44],
        [6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 45, 46, 47, 48, 49, 6e6, 50, 51, 52, 53, 6e6, 54, 55, 56, 57],
        [6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 58, 59, 60, 61, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6],
        [6e6, 6e6, 62, 63, 64, 65, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6],
        [6e6, 66, 67, 68, 69, 70, 6e6, 71, 72, 73, 74, 6e6, 75, 76, 77, 78, 6e6, 79, 80, 81, 82, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6],
        [83, 84, 85, 86, 87, 88, 6e6, 89, 90, 91, 92, 6e6, 93, 94, 95, 96, 6e6, 97, 98, 99, 100, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6],
        [101, 102, 103, 104, 105, 106, 6e6, 107, 108, 109, 110, 6e6, 111, 112, 113, 114, 6e6, 115, 116, 117, 118, 6e6, 119, 120, 121, 122, 6e6, 6e6, 6e6, 6e6, 6e6],
        [6e6, 123, 124, 125, 126, 127, 6e6, 128, 129, 130, 131, 6e6, 132, 133, 134, 135, 6e6, 136, 137, 138, 139, 6e6, 140, 141, 142, 143, 6e6, 6e6, 6e6, 6e6, 6e6],
        [6e6, 6e6, 144, 145, 146, 147, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 148, 149, 150, 151, 6e6, 6e6, 6e6, 6e6, 6e6],
        [6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 152, 153, 154, 155, 6e6, 6e6, 6e6, 6e6, 6e6],
        [6e6, 6e6, 156, 157, 158, 159, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 160, 161, 162, 163, 6e6, 6e6, 6e6, 6e6, 6e6],
        [6e6, 164, 165, 166, 167, 168, 6e6, 169, 170, 171, 172, 6e6, 173, 174, 175, 176, 6e6, 177, 178, 179, 180, 6e6, 181, 182, 183, 184, 6e6, 6e6, 6e6, 6e6, 6e6],
        [185, 186, 187, 188, 189, 190, 6e6, 191, 192, 193, 194, 6e6, 195, 196, 197, 198, 6e6, 199, 200, 201, 202, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6],
        [203, 204, 205, 206, 207, 208, 6e6, 209, 210, 211, 212, 6e6, 213, 214, 215, 216, 6e6, 217, 218, 219, 220, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6],
        [6e6, 221, 222, 223, 224, 225, 6e6, 226, 227, 228, 229, 6e6, 230, 231, 232, 233, 6e6, 234, 235, 236, 237, 6e6, 238, 239, 240, 241, 6e6, 242, 243, 244, 245],
        [6e6, 6e6, 246, 247, 248, 249, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 250, 251, 252, 253, 6e6, 254, 255, 256, 257],
        [6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 258, 259, 260, 261, 6e6, 262, 263, 264, 265],
        [6e6, 6e6, 266, 267, 268, 269, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 270, 271, 272, 273, 6e6, 274, 275, 276, 277],
        [6e6, 278, 279, 280, 281, 282, 6e6, 283, 284, 285, 286, 6e6, 287, 288, 289, 290, 6e6, 291, 292, 293, 294, 6e6, 295, 296, 297, 298, 6e6, 299, 300, 301, 302],
        [303, 304, 305, 306, 307, 308, 6e6, 309, 310, 311, 312, 6e6, 313, 314, 315, 316, 6e6, 317, 318, 319, 320, 6e6, 321, 322, 323, 324, 6e6, 325, 326, 327, 328],
        [329, 330, 331, 332, 333, 334, 6e6, 335, 336, 337, 338, 6e6, 339, 340, 341, 342, 6e6, 343, 344, 345, 346, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6],
        [6e6, 347, 348, 349, 350, 351, 6e6, 352, 353, 354, 355 , 6e6, 356, 357, 358, 359, 6e6, 360, 361, 362, 363, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6],
        [6e6, 6e6, 364, 365, 366, 367, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6, 6e6],
    ],
    dtype=object,
)

def taxel_location_map_for_image_representation(img):
    row, col = np.where(img != 6e6)
    taxels_loc = {}
    for r, c in zip(row, col):
        taxel = img[r, c]
        taxels_loc[taxel] = (int(r), int(c))
    # pprint.pprint(taxels_loc)
    return taxels_loc

################### Thumb ##########################

def get_th_hardware_taxel_map(map_dict):
    th_taxel_map = map_dict["TH"]

    # Thumb Finger Tip  is 1D array
    tip = th_taxel_map["tip"]
    fingertip_map = tip["1"]+tip["2"]+tip["3"] +tip["4"]+tip["5"] +tip["6"]
    
    # Thumb distal is 2D array
    ds = th_taxel_map["second"]
    ds_map = [
        ds["1"],
        ds["2"],
        ds["3"],
        ds["4"],
    ]

    # Thumb proximal is 2D array
    px = th_taxel_map["third"]
    px_map = [
        px["1"],
        px["2"],
        px["3"],
        px["4"],
    ]
    return fingertip_map, ds_map, px_map


def get_th_sim_taxel_map():
    # Thumb Finger Tip  is 1D array
    fingertip_map = [
        f"th_sensor_{i}" for i in range(1, 31)
    ]
    ds_map = []
    # Thumb distal is 2D array
    for i in range(4):
        row = []
        for j in range(3, -1, -1):
            row.append(f"th_ds_4_4_sensor_patch_{i}_{j}")
        ds_map.append(row)
    px_map = []
    # Thumb proximal is 2D array
    for i in range(4):
        row = []
        for j in range(3, -1, -1):
            row.append(f"th_px_4_4_sensor_patch_{i}_{j}")
        px_map.append(row)
    return fingertip_map, ds_map, px_map


################## Fingers ##########################

def get_finger_hardware_taxel_map(finger_name, map_dict):
    # finger_name is "IF", "MF", "RF"
    finger_taxel_map = map_dict[finger_name]

    # Finger Tip  is 1D array
    tip = finger_taxel_map["tip"]
    fingertip_map = tip["1"]+tip["2"]+tip["3"] +tip["4"]+tip["5"] +tip["6"]
    
    # Finger distal is 2D array
    ds = finger_taxel_map["second"]
    ds_map = [
        ds["1"],
        ds["2"],
        ds["3"],
        ds["4"],
    ]

    # Finger middle is 2D array
    md = finger_taxel_map["third"]
    md_map = [
        md["1"],
        md["2"],
        md["3"],
        md["4"],
    ]
    # Finger bs is 2D array
    bs = finger_taxel_map["fourth"]
    bs_map = [
        bs["1"],
        bs["2"],
        bs["3"],
        bs["4"],
    ]
    return fingertip_map, ds_map, md_map, bs_map

def get_finger_sim_taxel_map(finger_name):
    finger_name = finger_name.lower()
    # Finger Tip  is 1D array
    fingertip_map = [
        f"{finger_name}_sensor_{i}" for i in range(1, 31)
    ]
    
    # distal is 2D array
    ds_map = []
    for i in range(4):
        row = []
        for j in range(3, -1, -1):
            row.append(f"{finger_name}_ds_4_4_sensor_patch_{i}_{j}")
        ds_map.append(row)

    # middle is 2D array
    md_map = []
    for i in range(4):
        row = []
        for j in range(3, -1, -1):
            row.append(f"{finger_name}_md_4_4_sensor_patch_{i}_{j}")
        md_map.append(row)

    # bs is 2D array
    bs_map = []
    for i in range(4):
        row = []
        for j in range(3, -1, -1):
            row.append(f"{finger_name}_bs_4_4_sensor_patch_{i}_{j}")
        bs_map.append(row)
    
    return fingertip_map, ds_map, md_map, bs_map

############## Palm ##########################
def get_palm_sim_taxel_map(map_dict):

    # palm left sensors are 2d arrays
    up_left_map = []
    for i in range(6):
        row = []
        for j in range(3, -1, -1):
            row.append(f"palm_up_left_ds_4_4_sensor_patch_{i}_{j}")
        up_left_map.append(row)
    
    down_left_map = []
    for i in range(6):
        row = []
        for j in range(3, -1, -1):
            row.append(f"palm_down_left_ds_4_4_sensor_patch_{i}_{j}")
        down_left_map.append(row)

    # palm right sensor
    up_right_map = []
    for i in range(5, -1, -1):
        for j in range(3):
            row.append(f"palm_up_right_ds_4_4_sensor_patch_{i}_{j}")
        up_right_map.append(row)
    
    return up_left_map, down_left_map, up_right_map

def get_palm_hardware_taxel_map(map_dict):
    up_right = map_dict["Palm"]["up_right"]
    up_right_map = [
        up_right["1"],
        up_right["2"],
        up_right["3"],
        up_right["4"],
        up_right["5"],
        up_right["6"],
    ]

    up_left = map_dict["Palm"]["up_left"]
    up_left_map = [
        up_left["1"],
        up_left["2"],
        up_left["3"],
        up_left["4"],
        up_left["5"],
        up_left["6"],
    ]

    down_left = map_dict["Palm"]["down_left"]
    down_left_map = [
        down_left["1"],
        down_left["2"],
        down_left["3"],
        down_left["4"],
        down_left["5"],
        down_left["6"],
    ]
    return up_left_map, down_left_map, up_right_map


def get_flatten_hand(map_dict):
      ### Flaten all arrays and concatenate them ###
    # TH
    th_tip_hw,  th_ds_hw, th_px_hw = get_th_hardware_taxel_map(map_dict)
    th_tip_sim, th_ds_sim, th_px_sim = get_th_sim_taxel_map()

    th_ds_hw_flat = [item for sublist in th_ds_hw for item in sublist]
    th_px_hw_flat = [item for sublist in th_px_hw for item in sublist]
    th_hw_flat = th_tip_hw + th_ds_hw_flat + th_px_hw_flat

    th_ds_sim_flat = [item for sublist in th_ds_sim for item in sublist]
    th_px_sim_flat = [item for sublist in th_px_sim for item in sublist]
    th_sim_flat = th_tip_sim + th_ds_sim_flat + th_px_sim_flat

    # Fingers
    finger_hw_flat = []
    finger_sim_flat = []
    for finger_name in ["IF", "MF", "RF"]:
        tip_hw, ds_hw, md_hw, bs_hw = get_finger_hardware_taxel_map(finger_name, map_dict)
        tip_sim, ds_sim, md_sim, bs_sim = get_finger_sim_taxel_map(finger_name)

        ds_hw_flat = [item for sublist in ds_hw for item in sublist]
        md_hw_flat = [item for sublist in md_hw for item in sublist]
        bs_hw_flat = [item for sublist in bs_hw for item in sublist]
        hw_flat = tip_hw + ds_hw_flat + md_hw_flat + bs_hw_flat

        ds_sim_flat = [item for sublist in ds_sim for item in sublist]
        md_sim_flat = [item for sublist in md_sim for item in sublist]
        bs_sim_flat = [item for sublist in bs_sim for item in sublist]
        sim_flat = tip_sim + ds_sim_flat + md_sim_flat + bs_sim_flat

        finger_hw_flat += hw_flat
        finger_sim_flat += sim_flat
    
    # Palm
    up_left_hw, down_left_hw, up_right_hw = get_palm_hardware_taxel_map(map_dict)
    up_left_sim, down_left_sim, up_right_sim = get_palm_sim_taxel_map(map_dict)

    up_left_hw_flat = [item for sublist in up_left_hw for item in sublist]
    down_left_hw_flat = [item for sublist in down_left_hw for item in sublist]
    up_right_hw_flat = [item for sublist in up_right_hw for item in sublist]

    up_left_sim_flat = [item for sublist in up_left_sim for item in sublist]
    down_left_sim_flat = [item for sublist in down_left_sim for item in sublist]
    up_right_sim_flat = [item for sublist in up_right_sim for item in sublist]

    palm_hw_flat = up_left_hw_flat + down_left_hw_flat + up_right_hw_flat
    palm_sim_flat = up_left_sim_flat + down_left_sim_flat + up_right_sim_flat


    hand_hw_flat = th_hw_flat + finger_hw_flat + palm_hw_flat
    hand_sim_flat = th_sim_flat + finger_sim_flat + palm_sim_flat

    return hand_hw_flat, hand_sim_flat

def get_sorted_1D_hand_taxels_map(hand_hw_flat, hand_sim_flat):
    map = {}
    for i in range(len(hand_hw_flat)):
        map[hand_hw_flat[i]] = hand_sim_flat[i]
    return map

def sorted_1D_hand_taxel_name(map, hand_hw_flat):
    sorted_sim = []

    for i in range(368):
        sorted_sim.append(map[i])
    return sorted_sim

if __name__ == "__main__":
    map_dict = {}
    with open("leap_sensor_taxel_map.json", "r") as f:
        map_dict = json.load(f)

    ########### Creating One Flat Array for the whole hand ##########
    hand_hw_flat, hand_sim_flat = get_flatten_hand(map_dict)

    map_ = get_sorted_1D_hand_taxels_map(hand_hw_flat, hand_sim_flat)

    sorted_sim = sorted_1D_hand_taxel_name(map_, hand_hw_flat)
    
    print("########## Sorted Sim ##########")
    print("\n")
    print(sorted_sim)
    print("\n")

    ##################################################################
 
    print("\n")
    print(LEAP_XELA_ID.shape)
    print("\n")
    taxel_location_map_for_image_representation(LEAP_XELA_ID)