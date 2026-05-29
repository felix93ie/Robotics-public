#!/bin/bash
# ============================================================
# Terminal 3: Tactical Mission Coordinator (TMC) Node
# Sequences the drone through the Cavalry Scout mission logic
# ============================================================

# Use Pixi to run the ROS 2 node
pixi run bash -c "
  source ros_ws/install/setup.bash
  echo '✅ Starting TMC Node (Stage 2: Tactical Navigation)...'
  ros2 run scout_bot tmc_node
"
