FROM osrf/ros:foxy-desktop

LABEL org.opencontainers.image.authors="blazej135g@gmail.com"
# Update
RUN apt-get update && apt-get upgrade -y && apt-get autoremove -y
# Install dependencies
RUN apt install -y \
    libasio-dev git python3-pip \
    ros-foxy-cv-bridge ros-foxy-camera-calibration-parsers ros-foxy-gazebo-ros-pkgs \
    nano 
RUN pip3 install transformations==v2018.9.5
# Create workspace
RUN mkdir -p /root/tello_ws/src
WORKDIR /root/tello_ws/src
# Clone repositories
RUN git clone https://github.com/clydemcqueen/tello_ros.git
RUN git clone https://github.com/ptrmu/ros2_shared.git
RUN git clone https://github.com/ptrmu/fiducial_vlam.git

WORKDIR /root/tello_ws
# Clone models
WORKDIR /root/.gazebo/
RUN git clone https://github.com/osrf/gazebo_models.git
RUN mv gazebo_models models
# Build
WORKDIR /root/tello_ws
RUN . /opt/ros/foxy/setup.sh && \
    colcon build --symlink-install
# Add sourcing to bashrc
RUN echo "source /opt/ros/foxy/setup.sh" >> ~/.bashrc
RUN echo "source /root/tello_ws/install/setup.bash" >> ~/.bashrc
