# FROM nvidia/cuda:12.6.3-cudnn-devel-ubuntu22.04
FROM nvidia/cuda:12.2.2-cudnn8-devel-ubuntu22.04

RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

RUN apt-get update && apt-get install -y software-properties-common
RUN add-apt-repository universe

RUN apt-get update && apt-get install -y git
RUN apt-get update && apt install -y mesa-utils
# Install EGL libraries for headless MuJoCo rendering
RUN apt-get update && apt-get install -y libegl1-mesa libgl1-mesa-glx libglib2.0-0
RUN apt-get update && apt install -y libfuse2
#
# SAPIEN uses Vulkan for rendering. In containers you often need either:
# - NVIDIA Vulkan ICD from the host (GPU path), or
# - Mesa's lavapipe (CPU Vulkan path) as a fallback.
RUN apt-get update && apt-get install -y \
    libglvnd0 \
    libvulkan1 \
    mesa-vulkan-drivers \
    vulkan-validationlayers \
    && rm -rf /var/lib/apt/lists/*

#### ROS2 Humble ######
ENV ROS_DISTRO=humble

RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
RUN apt update && apt install locales
RUN locale-gen en_US en_US.UTF-8
RUN update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
RUN export LANG=en_US.UTF-8

RUN apt install -y software-properties-common
RUN add-apt-repository universe

RUN apt update && apt install curl -y
RUN apt-get update && apt-get install -y \
    ca-certificates \
    curl \
    gnupg

RUN export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F\" '{print $4}')
RUN apt-get update && apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
 && curl -fsSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
    | gpg --dearmor -o /usr/share/keyrings/ros-archive-keyring.gpg \
 && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
http://packages.ros.org/ros2/ubuntu \
$(lsb_release -cs) main" \
    > /etc/apt/sources.list.d/ros2.list
RUN apt-get update && apt-get install -y ros-${ROS_DISTRO}-desktop

#colcon build
RUN  apt update && apt install -y python3-colcon-common-extensions

#### Environment setup
RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
RUN bash /opt/ros/humble/setup.bash

##### python3.11 ######
RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv \
    && rm -rf /var/lib/apt/lists/*

#### Install dependencies
RUN apt-get install -y python3-pip curl
RUN pip install websocket-client
RUN pip3 install dynamixel-sdk
RUN pip install gradio
RUN pip install h5py
##### Terminator ####
RUN apt-get update && apt-get install -y terminator
##### PyQt5 ######
RUN apt-get update && apt-get install -y libxcb-cursor0
RUN pip install pyqtgraph PySide6

##### realsense ######
# Install RealSense (CUDA-accelerated processing: align, pointcloud, etc.).
# Base image supplies CUDA toolkit; runtime still needs NVIDIA driver + nvidia-container-toolkit (--gpus all).
ENV CUDA_HOME=/usr/local/cuda
ENV PATH=${CUDA_HOME}/bin:${PATH}
ENV LD_LIBRARY_PATH=${CUDA_HOME}/lib64:${LD_LIBRARY_PATH}
RUN \
    apt-get update && apt-get install -y cmake libssl-dev libusb-1.0-0-dev libudev-dev pkg-config libgtk-3-dev \
    &&                                                             \
    apt-get install -y libglfw3-dev libgl1-mesa-dev libglu1-mesa-dev at \
    &&                                                             \
    git clone https://github.com/IntelRealSense/librealsense.git   \
    &&                                                             \
    cd librealsense                                                \
    &&                                                             \
    git checkout -b development                                    \
    &&                                                             \
    mkdir build && cd build                                        \
    &&                                                             \
    cmake .. \
        -DCMAKE_BUILD_TYPE=Release \
        -DBUILD_WITH_CUDA=ON \
        -DBUILD_PYTHON_BINDINGS=ON \
        -DPYTHON_EXECUTABLE=/usr/bin/python3 \
    &&                                                             \
    cmake --build .     -j$(nproc)                                 \
    &&                                                             \
    cmake --install .                                              \
    && cd / && rm -rf /librealsense
ENV PYTHONPATH=$PYTHONPATH:/usr/local/lib
##### Dex-retargeting ######
# matplotlib from pip (NumPy 2 ABI). Apt python3-matplotlib targets system NumPy 1.x and breaks when pip installs NumPy 2 (mediapipe imports matplotlib).
RUN python3 -m pip install --no-cache-dir \
    "numpy>=2.0.0" \
    "matplotlib>=3.8.0" \
    "pytransform3d>=3.5.0" \
    "pin>=3.3.1" \
    "nlopt>=2.8.0" \
    "anytree>=2.12.0" \
    "pyyaml>=6.0.0" \
    "lxml>=5.2.2" \
    "tyro" \
    "tqdm" \
    "opencv-python" \
    "mediapipe==0.10.14" \
    "protobuf<5" \
    "sapien==3.0.0b0" \
    "loguru" \
    "torch"

###### Sapian #####
ARG VULKAN_SDK_VERSION=1.4.341.1
RUN cd /tmp && \
    curl -fSL -o "vulkansdk-linux-x86_64-${VULKAN_SDK_VERSION}.tar.xz" \
    "https://sdk.lunarg.com/sdk/download/${VULKAN_SDK_VERSION}/linux/vulkansdk-linux-x86_64-${VULKAN_SDK_VERSION}.tar.xz" && \
    tar -xJf "vulkansdk-linux-x86_64-${VULKAN_SDK_VERSION}.tar.xz" && \
    rm -f "vulkansdk-linux-x86_64-${VULKAN_SDK_VERSION}.tar.xz"
ENV VULKAN_SDK=/tmp/${VULKAN_SDK_VERSION}/x86_64 \
    LD_LIBRARY_PATH=/tmp/${VULKAN_SDK_VERSION}/x86_64/lib \
    VK_LAYER_PATH=/tmp/${VULKAN_SDK_VERSION}/x86_64/etc/vulkan/explicit_layer.d \
    PATH=/tmp/${VULKAN_SDK_VERSION}/x86_64/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin


# Vulkan & GLVND Support
RUN apt-get update && apt-get install -y vulkan-tools 
######pybullet ######
RUN pip install pybullet
######onshape-to-robot ######
RUN python3 -m pip install --no-cache-dir "uv>=0.5" "uv-build>=0.5"
RUN cd /tmp && \
    git clone https://github.com/Rhoban/onshape-to-robot.git && \
    cd onshape-to-robot && \
    python3 -m pip install --no-cache-dir --no-build-isolation .
####### Mujoco ######
ARG MUJOCO_VERSION=3.8.0
RUN cd /tmp && \
    git clone https://github.com/google-deepmind/mujoco.git && \
    cd mujoco && \
    git checkout "${MUJOCO_VERSION}" && \
    cmake -S . -B build \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=/usr/local && \
    cmake --build build -j"$(nproc)" && \
    cmake --install build
RUN pip install mujoco==${MUJOCO_VERSION}
####### perline noise ######
# https://github.com/salaxieb/perlin_noise
RUN pip install perlin-noise
###### open3d ######
RUN pip install open3d
###### xacro ######
RUN apt-get update && apt-get install -y ros-humble-xacro
##### Joint state publisher ######
RUN apt-get update && apt-get install -y ros-humble-joint-state-publisher-gui
###### WorkDir #######
WORKDIR workspace

###### Shell #######
CMD /bin/bash
