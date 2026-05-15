
#https://medium.com/@smart-design-techology/hand-detection-in-3d-space-888433a1c1f3


# ====== Sample Code for Smart Design Technology Blog ======

# Intel Realsense D435 cam has RGB camera with 1920×1080 resolution
# Depth camera is 1280x720
# FOV is limited to 69deg x 42deg (H x V) - the RGB camera FOV

# If you run this on a non-Intel CPU, explore other options for rs.align
    # On the NVIDIA Jetson AGX we build the pyrealsense lib with CUDA

import pyrealsense2 as rs
import mediapipe as mp
import cv2
import numpy as np
import datetime as dt

font = cv2.FONT_HERSHEY_SIMPLEX
org = (20, 100)
fontScale = .5
color = (0,50,255)
thickness = 1

# ====== Realsense ======
realsense_ctx = rs.context()
connected_devices = [] # List of serial numbers for present cameras
for i in range(len(realsense_ctx.devices)):
    detected_camera = realsense_ctx.devices[i].get_info(rs.camera_info.serial_number)
    print(f"{detected_camera}")
    connected_devices.append(detected_camera)
device = connected_devices[0] # In this example we are only using one camera
pipeline = rs.pipeline()
config = rs.config()
background_removed_color = 153 # Grey

# ====== Mediapipe ======
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

# MediaPipe hand landmark indices for fingertips
FINGERTIP_LANDMARKS = (
    ("thumb", 4),
    ("index", 8),
    ("middle", 12),
    ("ring", 16),
    ("pinky", 20),
)


# ====== Enable Streams ======
config.enable_device(device)

# # For worse FPS, but better resolution:
# stream_res_x = 1280
# stream_res_y = 720
# # For better FPS. but worse resolution:
stream_res_x = 640
stream_res_y = 480

stream_fps = 30

config.enable_stream(rs.stream.depth, stream_res_x, stream_res_y, rs.format.z16, stream_fps)
config.enable_stream(rs.stream.color, stream_res_x, stream_res_y, rs.format.bgr8, stream_fps)
profile = pipeline.start(config)

# Intrinsics for the color image (aligned depth uses the same pixel grid)
color_intrinsics = (
    profile.get_stream(rs.stream.color).as_video_stream_profile().get_intrinsics()
)

align_to = rs.stream.color
align = rs.align(align_to)

# ====== Get depth Scale ======
depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()
print(f"\tDepth Scale for Camera SN {device} is: {depth_scale}")

# ====== Set clipping distance ======
clipping_distance_in_meters = 2
clipping_distance = clipping_distance_in_meters / depth_scale
print(f"\tConfiguration Successful for SN {device}")

# ====== Get and process images ====== 
print(f"Starting to capture images on SN: {device}")

name_of_window = "SN: " + str(device)
display_width = 1280
display_height = 960
cv2.namedWindow(name_of_window, cv2.WINDOW_NORMAL)
cv2.resizeWindow(name_of_window, display_width, display_height)

frame_idx = 0
print_mpz_every_n_frames = 15

while True:
    start_time = dt.datetime.today().timestamp()

    # Get and align frames
    frames = pipeline.wait_for_frames()
    aligned_frames = align.process(frames)
    aligned_depth_frame = aligned_frames.get_depth_frame()
    color_frame = aligned_frames.get_color_frame()
    
    if not aligned_depth_frame or not color_frame:
        continue

    # Process images
    depth_image = np.asanyarray(aligned_depth_frame.get_data())
    depth_image_flipped = cv2.flip(depth_image,1)
    color_image = np.asanyarray(color_frame.get_data())

    depth_image_3d = np.dstack((depth_image,depth_image,depth_image)) #Depth image is 1 channel, while color image is 3
    background_removed = np.where((depth_image_3d > clipping_distance) | (depth_image_3d <= 0), background_removed_color, color_image)

    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

    images = cv2.flip(background_removed,1)
    color_image = cv2.flip(color_image,1)
    color_images_rgb = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)

    # Process hands
    results = hands.process(color_images_rgb)
    if results.multi_hand_landmarks:
        number_of_hands = len(results.multi_hand_landmarks)
        i=0
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(images, handLms, mpHands.HAND_CONNECTIONS)
            org2 = (20, org[1]+(20*(i+1)))
            hand_side_classification_list = results.multi_handedness[i]
            hand_side = hand_side_classification_list.classification[0].label

            # Fingertip positions + depth overlaid on the OpenCV image
            img_h, img_w = images.shape[:2]
            tip_circle_color = (0, 255, 255) if hand_side == "Right" else (0, 255, 0)
            tip_font_scale = 0.42
            for tip_name, lm_idx in FINGERTIP_LANDMARKS:
                lm = handLms.landmark[lm_idx]
                px = int(lm.x * img_w)
                py = int(lm.y * img_h)
                px = min(max(px, 0), img_w - 1)
                py = min(max(py, 0), img_h - 1)
                depth_m = depth_image_flipped[py, px] * depth_scale
                mp_z = lm.z
                # Map flipped display pixels back to camera/aligned-depth coordinates
                u_cam = float((img_w - 1) - px)
                v_cam = float(py)
                if depth_m > 0:
                    xyz = rs.rs2_deproject_pixel_to_point(
                        color_intrinsics, [u_cam, v_cam], depth_m
                    )
                    xyz_label = f"cam XYZ(m): {xyz[0]:.3f} {xyz[1]:.3f} {xyz[2]:.3f}"
                else:
                    xyz_label = "cam XYZ(m): -- (no depth)"

                cv2.circle(images, (px, py), 6, tip_circle_color, 2, cv2.LINE_AA)
                # mp_z: MediaPipe relative depth (same scale as normalized x); not meters
                label1 = (
                    f"{hand_side[0]}:{tip_name} ({px},{py}) "
                    f"RS:{depth_m:.2f}m MPz:{mp_z:.3f}"
                )
                tx, ty = px + 8, py - 6
                if ty < 16:
                    ty = py + 20
                if tx + 380 > img_w:
                    tx = max(4, px - 360)
                for lbl, dy in ((label1, 0), (xyz_label, 16)):
                    y_draw = ty + dy
                    if y_draw >= img_h - 2:
                        continue
                    cv2.putText(
                        images,
                        lbl,
                        (tx + 1, y_draw + 1),
                        font,
                        tip_font_scale,
                        (0, 0, 0),
                        2,
                        cv2.LINE_AA,
                    )
                    cv2.putText(
                        images,
                        lbl,
                        (tx, y_draw),
                        font,
                        tip_font_scale,
                        (255, 255, 255),
                        1,
                        cv2.LINE_AA,
                    )

            if frame_idx % print_mpz_every_n_frames == 0:
                mpz_parts = [
                    f"{tn}={handLms.landmark[idx].z:.4f}"
                    for tn, idx in FINGERTIP_LANDMARKS
                ]
                print(f"{hand_side} hand MediaPipe z (relative): " + ", ".join(mpz_parts))

            middle_finger_knuckle = results.multi_hand_landmarks[i].landmark[9]
            x = int(middle_finger_knuckle.x*len(depth_image_flipped[0]))
            y = int(middle_finger_knuckle.y*len(depth_image_flipped))
            if x >= len(depth_image_flipped[0]):
                x = len(depth_image_flipped[0]) - 1
            if y >= len(depth_image_flipped):
                y = len(depth_image_flipped) - 1
            mfk_distance = depth_image_flipped[y,x] * depth_scale # meters
            mfk_distance_feet = mfk_distance * 3.281 # feet
            images = cv2.putText(images, f"{hand_side} Hand Distance: {mfk_distance_feet:0.3} feet ({mfk_distance:0.3} m) away", org2, font, fontScale, color, thickness, cv2.LINE_AA)
            
            i+=1
        images = cv2.putText(images, f"Hands: {number_of_hands}", org, font, fontScale, color, thickness, cv2.LINE_AA)
    else:
        images = cv2.putText(images,"No Hands", org, font, fontScale, color, thickness, cv2.LINE_AA)


    # Display FPS
    time_diff = dt.datetime.today().timestamp() - start_time
    fps = int(1 / time_diff)
    org3 = (20, org[1] + 60)
    images = cv2.putText(images, f"FPS: {fps}", org3, font, fontScale, color, thickness, cv2.LINE_AA)

    # Display images
    cv2.imshow(name_of_window, images)
    key = cv2.waitKey(1)
    # Press esc or 'q' to close the image window
    if key & 0xFF == ord('q') or key == 27:
        print(f"User pressed break key for SN: {device}")
        break

    frame_idx += 1

print(f"Application Closing")
pipeline.stop()
print(f"Application Closed.")