#!/bin/bash
# ============================================================
# Helper Script to Bridge Gazebo Camera Topic to ROS 2
# ============================================================

WORLD_NAME="${PX4_GZ_WORLD:-baylands_custom}"
MODEL_NAME="x500_depth_0"

# M2-specific fixes
export GZ_IP=127.0.0.1

# RGB camera:
GZ_RGB_TOPIC="/world/${WORLD_NAME}/model/${MODEL_NAME}/link/camera_link/sensor/IMX214/image"
ROS_RGB_TOPIC="/camera/image_raw"

# Depth camera:
GZ_DEPTH_TOPIC="/world/${WORLD_NAME}/model/${MODEL_NAME}/link/camera_link/sensor/StereoOV7251/depth_camera"
ROS_DEPTH_TOPIC="/camera/depth/image_raw"

echo "✅ Starting ros_gz_bridge..."
echo "   Bridging RGB Gazebo Topic:   $GZ_RGB_TOPIC"
echo "   To ROS 2 Topic:              $ROS_RGB_TOPIC"
echo "   Bridging Depth Gazebo Topic: $GZ_DEPTH_TOPIC"
echo "   To ROS 2 Topic:              $ROS_DEPTH_TOPIC"
echo ""

# Run the parameter bridge using Pixi
pixi run ros2 run ros_gz_bridge parameter_bridge \
  "$GZ_RGB_TOPIC@sensor_msgs/msg/Image[gz.msgs.Image" \
  "$GZ_DEPTH_TOPIC@sensor_msgs/msg/Image[gz.msgs.Image" \
  --ros-args \
  -r "$GZ_RGB_TOPIC:=$ROS_RGB_TOPIC" \
  -r "$GZ_DEPTH_TOPIC:=$ROS_DEPTH_TOPIC"
