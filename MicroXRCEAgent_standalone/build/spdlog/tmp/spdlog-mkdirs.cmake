# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file LICENSE.rst or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION ${CMAKE_VERSION}) # this file comes with cmake

# If CMAKE_DISABLE_SOURCE_CHANGES is set to true and the source directory is an
# existing directory in our source tree, calling file(MAKE_DIRECTORY) on it
# would cause a fatal error, even though it would be a no-op.
if(NOT EXISTS "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/spdlog/src/spdlog")
  file(MAKE_DIRECTORY "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/spdlog/src/spdlog")
endif()
file(MAKE_DIRECTORY
  "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/spdlog/src/spdlog-build"
  "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/temp_install/spdlog-1.9.2"
  "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/spdlog/tmp"
  "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/spdlog/src/spdlog-stamp"
  "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/spdlog/src"
  "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/spdlog/src/spdlog-stamp"
)

set(configSubDirs )
foreach(subDir IN LISTS configSubDirs)
    file(MAKE_DIRECTORY "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/spdlog/src/spdlog-stamp/${subDir}")
endforeach()
if(cfgdir)
  file(MAKE_DIRECTORY "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/spdlog/src/spdlog-stamp${cfgdir}") # cfgdir has leading slash
endif()
