# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file LICENSE.rst or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION ${CMAKE_VERSION}) # this file comes with cmake

# If CMAKE_DISABLE_SOURCE_CHANGES is set to true and the source directory is an
# existing directory in our source tree, calling file(MAKE_DIRECTORY) on it
# would cause a fatal error, even though it would be a no-op.
if(NOT EXISTS "/Users/eduardofelix/scout_bot_mac/ros_ws/src/Micro-XRCE-DDS-Agent")
  file(MAKE_DIRECTORY "/Users/eduardofelix/scout_bot_mac/ros_ws/src/Micro-XRCE-DDS-Agent")
endif()
file(MAKE_DIRECTORY
  "/Users/eduardofelix/scout_bot_mac/ros_ws/build/microxrcedds_agent"
  "/Users/eduardofelix/scout_bot_mac/ros_ws/build/microxrcedds_agent/uagent-prefix"
  "/Users/eduardofelix/scout_bot_mac/ros_ws/build/microxrcedds_agent/uagent-prefix/tmp"
  "/Users/eduardofelix/scout_bot_mac/ros_ws/build/microxrcedds_agent/uagent-prefix/src/uagent-stamp"
  "/Users/eduardofelix/scout_bot_mac/ros_ws/build/microxrcedds_agent/uagent-prefix/src"
  "/Users/eduardofelix/scout_bot_mac/ros_ws/build/microxrcedds_agent/uagent-prefix/src/uagent-stamp"
)

set(configSubDirs )
foreach(subDir IN LISTS configSubDirs)
    file(MAKE_DIRECTORY "/Users/eduardofelix/scout_bot_mac/ros_ws/build/microxrcedds_agent/uagent-prefix/src/uagent-stamp/${subDir}")
endforeach()
if(cfgdir)
  file(MAKE_DIRECTORY "/Users/eduardofelix/scout_bot_mac/ros_ws/build/microxrcedds_agent/uagent-prefix/src/uagent-stamp${cfgdir}") # cfgdir has leading slash
endif()
