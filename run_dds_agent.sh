#!/bin/bash
# ============================================================
# Terminal 2: Micro-XRCE-DDS Agent  (v2.4.3 standalone build)
# Bridges PX4 SITL (uXRCE-DDS client on UDP:8888) → DDS domain
# Run AFTER Terminal 1 (PX4 SITL) is up
# ============================================================

AGENT_BUILD="/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build"
AGENT_BIN="$AGENT_BUILD/MicroXRCEAgent"

if [ ! -f "$AGENT_BIN" ]; then
    echo "❌ ERROR: MicroXRCEAgent binary not found at $AGENT_BIN"
    exit 1
fi

# Standalone build libs — agent links against its own fastcdr/fastrtps
export DYLD_LIBRARY_PATH="\
$AGENT_BUILD:\
$AGENT_BUILD/fastcdr/src/fastcdr-build/src/cpp:\
$AGENT_BUILD/fastdds/src/fastdds-build/src/cpp:\
$AGENT_BUILD/temp_install/fastrtps-2.14/lib:\
$DYLD_LIBRARY_PATH"

echo "✅ Starting MicroXRCEAgent v2.4.3 on UDP port 8888..."
echo "   Waiting for PX4 SITL XRCE client connection..."
echo ""
"$AGENT_BIN" udp4 -p 8888
