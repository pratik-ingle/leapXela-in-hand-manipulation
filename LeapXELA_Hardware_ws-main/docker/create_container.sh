
sudo xhost +local:root


sudo docker run --runtime=nvidia -it --name leap_xela_hardware \
  -v $(pwd)/../../LeapXELA_Hardware_ws:/workspace/LeapXELA_Hardware_ws \
  -v /etc/xela:/etc/xela \
  --cap-add NET_ADMIN \
  --cap-add NET_RAW \
  -e NVIDIA_VISIBLE_DEVICES=all \
  -e NVIDIA_DRIVER_CAPABILITIES=all \
  -e DISPLAY -e LOCAL_USER_ID=$(id -u) -e LOCAL_GID=$(id -g) \
  -e QT_X11_NO_MITSHM=1 -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -e MUJOCO_GL=egl \
  --net=host  --privileged leap_xela_hardware


