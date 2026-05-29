#!/bin/bash
# ============================================================
# Helper Script to Launch YOLO Object Detection Node
# ============================================================

# Use Pixi to run the ROS 2 node
pixi run bash -c "
  source ros_ws/install/setup.bash
  echo '✅ Starting YOLOv8 Object Detection Node (Stage 3: Vision)...'
  ros2 run scout_bot yolo_node
"
