# Install script for directory: /Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory/src

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/temp_install/foonathan_memory")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set path to fallback-tool for dependency-resolution.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/usr/bin/objdump")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY FILES "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory-build/src/libfoonathan_memory-0.7.3.a")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libfoonathan_memory-0.7.3.a" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libfoonathan_memory-0.7.3.a")
    execute_process(COMMAND "/usr/bin/ranlib" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libfoonathan_memory-0.7.3.a")
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/foonathan_memory/foonathan/memory" TYPE FILE FILES "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory-build/src/config_impl.hpp")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/foonathan_memory/foonathan/memory/detail" TYPE FILE FILES "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory-build/src/container_node_sizes_impl.hpp")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/foonathan_memory/foonathan/memory" TYPE FILE FILES
    "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory/include/foonathan/memory/aligned_allocator.hpp"
    "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory/include/foonathan/memory/allocator_storage.hpp"
    "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory/include/foonathan/memory/allocator_traits.hpp"
    "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory/include/foonathan/memory/config.hpp"
    "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory/include/foonathan/memory/container.hpp"
    "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory/include/foonathan/memory/debugging.hpp"
    "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory/include/foonathan/memory/default_allocator.hpp"
    "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory/include/foonathan/memory/deleter.hpp"
    "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory/include/foonathan/memory/error.hpp"
    "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory/include/foonathan/memory/fallback_allocator.hpp"
    "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory/include/foonathan/memory/malloc_allocator.hpp"
    "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory/include/foonathan/memory/heap_allocator.hpp"
    "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory/include/foonathan/memory/iteration_allocator.hpp"
    "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory/include/foonathan/memory/joint_allocator.hpp"
    "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory/include/foonathan/memory/memory_arena.hpp"
    "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory/include/foonathan/memory/memory_pool.hpp"
    "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory/include/foonathan/memory/memory_pool_collection.hpp"
    "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory/include/foonathan/memory/memory_pool_type.hpp"
    "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory/include/foonathan/memory/memory_resource_adapter.hpp"
    "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory/include/foonathan/memory/memory_stack.hpp"
    "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory/include/foonathan/memory/namespace_alias.hpp"
    "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory/include/foonathan/memory/new_allocator.hpp"
    "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory/include/foonathan/memory/segregator.hpp"
    "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory/include/foonathan/memory/smart_ptr.hpp"
    "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory/include/foonathan/memory/static_allocator.hpp"
    "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory/include/foonathan/memory/std_allocator.hpp"
    "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory/include/foonathan/memory/temporary_allocator.hpp"
    "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory/include/foonathan/memory/threading.hpp"
    "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory/include/foonathan/memory/tracking.hpp"
    "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory/include/foonathan/memory/virtual_memory.hpp"
    "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory-build/src/container_node_sizes_impl.hpp"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/foonathan_memory/foonathan/memory/detail" TYPE FILE FILES
    "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory/include/foonathan/memory/detail/align.hpp"
    "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory/include/foonathan/memory/detail/assert.hpp"
    "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory/include/foonathan/memory/detail/container_node_sizes.hpp"
    "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory/include/foonathan/memory/detail/debug_helpers.hpp"
    "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory/include/foonathan/memory/detail/ebo_storage.hpp"
    "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory/include/foonathan/memory/detail/free_list.hpp"
    "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory/include/foonathan/memory/detail/free_list_array.hpp"
    "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory/include/foonathan/memory/detail/ilog2.hpp"
    "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory/include/foonathan/memory/detail/lowlevel_allocator.hpp"
    "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory/include/foonathan/memory/detail/memory_stack.hpp"
    "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory/include/foonathan/memory/detail/small_free_list.hpp"
    "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory/include/foonathan/memory/detail/utility.hpp"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/foonathan_memory/cmake" TYPE FILE FILES "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory-build/src/cmake/foonathan_memory-config-version.cmake")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
if(CMAKE_INSTALL_LOCAL_ONLY)
  file(WRITE "/Users/eduardofelix/scout_bot_mac/MicroXRCEAgent_standalone/build/foonathan_memory/src/foonathan_memory-build/src/install_local_manifest.txt"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
endif()
