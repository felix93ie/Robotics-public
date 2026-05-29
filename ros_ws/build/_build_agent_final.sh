#!/bin/bash
# Final MicroXRCEAgent build — run after FastDDS is installed to dds_deps_install/
set -e

DEPS='/Users/eduardofelix/scout_bot_mac/ros_ws/build/dds_deps_install'
PIXI_PREFIX='/Users/eduardofelix/scout_bot_mac/.pixi/envs/default'
AGENT_SRC='/Users/eduardofelix/scout_bot_mac/ros_ws/src/Micro-XRCE-DDS-Agent'
AGENT_BUILD='/Users/eduardofelix/scout_bot_mac/ros_ws/build/microxrcedds_agent'
AGENT_INSTALL='/Users/eduardofelix/scout_bot_mac/ros_ws/install/microxrcedds_agent'

ulimit -n 4096

echo "=== Building MicroXRCEAgent v2.4.2 with system FastDDS ==="
rm -rf "$AGENT_BUILD"
mkdir -p "$AGENT_BUILD" "$AGENT_INSTALL"

cmake -S "$AGENT_SRC" -B "$AGENT_BUILD" \
  -DUAGENT_SUPERBUILD=OFF \
  -DUAGENT_USE_SYSTEM_FASTCDR=ON \
  -DUAGENT_USE_SYSTEM_FASTDDS=ON \
  -DUAGENT_USE_SYSTEM_LOGGER=OFF \
  -DUAGENT_FAST_PROFILE=ON \
  -DUAGENT_CED_PROFILE=ON \
  -DUAGENT_DISCOVERY_PROFILE=ON \
  -DUAGENT_P2P_PROFILE=OFF \
  -DUAGENT_LOGGER_PROFILE=OFF \
  -DUAGENT_SOCKETCAN_PROFILE=OFF \
  -DUAGENT_BUILD_EXECUTABLE=ON \
  -DUAGENT_BUILD_TESTS=OFF \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX="$AGENT_INSTALL" \
  -DCMAKE_PREFIX_PATH="$DEPS:$PIXI_PREFIX" \
  -DCMAKE_IGNORE_PATH="$PIXI_PREFIX/lib/cmake/fastcdr;$PIXI_PREFIX/share/fastrtps" \
  -Dfastcdr_DIR="$DEPS/lib/cmake/fastcdr" \
  -Dfastrtps_DIR="$DEPS/share/fastrtps/cmake" \
  2>&1

echo "Configure exit: $?"
cmake --build "$AGENT_BUILD" --target install -j6 2>&1
EXIT=$?
echo "=== Agent build exit: $EXIT ==="
[ $EXIT -eq 0 ] && find "$AGENT_INSTALL" -name 'MicroXRCEAgent'
