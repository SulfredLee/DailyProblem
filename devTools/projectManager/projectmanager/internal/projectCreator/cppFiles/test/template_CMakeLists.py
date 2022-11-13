content_st = """
set(targetName "{{ project_name }}_Test")
get_filename_component(folderName ${CMAKE_CURRENT_SOURCE_DIR} NAME)
string(REPLACE " " "_" folderName ${folderName})

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-deprecated-declarations")

file(GLOB ${folderName}_inc
  "${CMAKE_CURRENT_SOURCE_DIR}/*.h")
file(GLOB ${folderName}_src
  "${CMAKE_CURRENT_SOURCE_DIR}/*.cpp")

include_directories(
  ${CMAKE_CURRENT_SOURCE_DIR}
  ${GTEST_INCLUDE_DIRS}
  )
  # ${PROJECT_SOURCE_DIR}/../ProjectB/lib/PrintHelper
  # ${PROJECT_SOURCE_DIR}/lib/utility
  # ${libpng_INCLUDE_DIR}
  # ${libbmp_INCLUDE_DIR})

add_executable(${targetName} ${${folderName}_src})

target_link_libraries(
  ${targetName}
  PRIVATE GTest::gmock GTest::gtest GTest::gmock_main GTest::gtest_main
  )
# target_link_libraries(
#   ${targetName}
#   ${CMAKE_INSTALL_PREFIX}/lib/libPrintHelper.so
#   ${CMAKE_THREAD_LIBS_INIT}
#   utility
#   ${libpng_LIBRARY_DIR}/libpng16.so
#   ${libbmp_LIBRARY_DIR}/libbmp.so
#   )

# Creates a folder "executables" and adds target
# project (*.vcproj) under it
set_property(TARGET ${targetName} PROPERTY FOLDER "executables")

# Adds logic to INSTALL.vcproj to copy *.exe to destination directory
install (TARGETS ${targetName} DESTINATION bin)
"""
