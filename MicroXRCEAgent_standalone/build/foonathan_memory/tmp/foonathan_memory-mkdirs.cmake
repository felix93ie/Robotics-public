# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file LICENSE.rst or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION ${CMAKE_VERSION}) # this file comes with cmake

# If CMAKE_DISABLE_SOURCE_CHANGES is set to true and the source directory is an
# existing directory in our source tree, calling file(MAKE_DIRECTORY) on it
# would cause a fatal error, even though it would be a no-op.
if(NOT EXISTS "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory")
  file(MAKE_DIRECTORY "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory")
endif()
file(MAKE_DIRECTORY
  "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory-build"
  "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/temp_install/foonathan_memory"
  "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/tmp"
  "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory-stamp"
  "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src"
  "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory-stamp"
)

set(configSubDirs )
foreach(subDir IN LISTS configSubDirs)
    file(MAKE_DIRECTORY "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory-stamp/${subDir}")
endforeach()
if(cfgdir)
  file(MAKE_DIRECTORY "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory-stamp${cfgdir}") # cfgdir has leading slash
endif()
