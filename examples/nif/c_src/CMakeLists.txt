cmake_minimum_required(VERSION 3.20)
project(example_nif LANGUAGES C)

# Use only the explicitly selected installation's public NIF headers.
file(TO_CMAKE_PATH "$ENV{OTP_PREFIX}" otp_prefix)
if(NOT IS_ABSOLUTE "${otp_prefix}" OR
   NOT EXISTS "${otp_prefix}/usr/include/erl_nif.h")
  message(FATAL_ERROR "Set OTP_PREFIX to an installed OTP distribution with usr/include/erl_nif.h")
endif()

add_library(example_nif MODULE example_nif.c)
target_include_directories(example_nif PRIVATE "${otp_prefix}/usr/include")
target_compile_features(example_nif PRIVATE c_std_99)
# Keep the same priv path with single- and multi-configuration generators.
set_target_properties(example_nif PROPERTIES
  PREFIX ""
  LIBRARY_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/../priv/$<0:>"
  RUNTIME_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/../priv/$<0:>")
if(WIN32)
  set_target_properties(example_nif PROPERTIES SUFFIX ".dll")
else()
  set_target_properties(example_nif PROPERTIES SUFFIX ".so")
endif()
if(APPLE)
  target_link_options(example_nif PRIVATE "LINKER:-undefined,dynamic_lookup")
endif()
