How to use

First install ROS2 Humble on Ubuntu 22.04

sudo apt-get install ros-humble-desktop

make a ROS2 workspace (directory can be changed as preferenced)

mkdir ros2_ws

cd ros2_ws

mkdir src

cd src

clone this repository

cd ~/ros2_ws

colcon build --packages-select duo_image_publisher

source ~/ros2_ws/install/setup.bash

run the camera publishers with:

ros2 launch duo_image_publisher dual_cameras.launch.py

run the synchronized image taker with:

ros2 run duo_image_publisher stereo_sync_node

The left right images should save in a stereo_pairs folder in your home directory.
