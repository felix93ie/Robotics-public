#!/bin/bash
echo "Starting PX4 SITL with Gazebo Harmonic (Forest world)..."

# Kill any lingering background simulators
pkill -9 -f px4 2>/dev/null || true
pkill -9 -f gz 2>/dev/null || true
pkill -9 -f ruby 2>/dev/null || true

# Wipe the PX4 EEPROM cache so the battery and parameters fully reset on every launch
rm -rf /Users/eduardofelix/scout_bot_mac/PX4-Autopilot/build/px4_sitl_default/rootfs

# M2-specific fixes
export GZ_IP=127.0.0.1

# Force runtime linker to use Pixi's Qt5/Protobuf instead of Homebrew's
PIXI_PREFIX=/Users/eduardofelix/scout_bot_mac/.pixi/envs/default
export DYLD_LIBRARY_PATH=${PIXI_PREFIX}/lib:$DYLD_LIBRARY_PATH

# Custom Baylands World with custom terrain
export PX4_GZ_WORLD=baylands_custom

# Append custom world and meshes path to resource path so Gazebo finds them
export GZ_SIM_RESOURCE_PATH="/Users/eduardofelix/scout_bot_mac/ros_ws/src/scout_bot/worlds:${GZ_SIM_RESOURCE_PATH}"

# Prevent CMake from mixing Homebrew libraries with Pixi libraries
export CMAKE_PREFIX_PATH=${PIXI_PREFIX}:$CMAKE_PREFIX_PATH

# Get the macOS SDK path (needed for OpenGL gl.h headers on newer macOS)
MACOS_SYSROOT=$(xcrun --show-sdk-path)

# Launch PX4 SITL
cd /Users/eduardofelix/scout_bot_mac/PX4-Autopilot
pixi run make px4_sitl gz_x500_depth \
  CMAKE_ARGS="-DCMAKE_FIND_FRAMEWORK=LAST -DCMAKE_SYSTEM_IGNORE_PATH=/opt/homebrew -DCMAKE_IGNORE_PATH=/opt/homebrew -DCMAKE_OSX_SYSROOT=${MACOS_SYSROOT} -DQt5_DIR=${PIXI_PREFIX}/lib/cmake/Qt5 -DProtobuf_LIBRARY=${PIXI_PREFIX}/lib/libprotobuf.dylib -DProtobuf_INCLUDE_DIR=${PIXI_PREFIX}/include -DProtobuf_PROTOC_EXECUTABLE=${PIXI_PREFIX}/bin/protoc"
