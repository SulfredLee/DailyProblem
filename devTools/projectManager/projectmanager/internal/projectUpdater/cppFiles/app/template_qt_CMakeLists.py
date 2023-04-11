content_st = """
set(targetName "{{ app_name }}")
get_filename_component(folderName ${CMAKE_CURRENT_SOURCE_DIR} NAME)
string(REPLACE " " "_" folderName ${folderName})

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-deprecated-declarations")

file(GLOB ${folderName}_inc
  "${CMAKE_CURRENT_SOURCE_DIR}/*.h")
file(GLOB ${folderName}_src
  "${CMAKE_CURRENT_SOURCE_DIR}/*.cpp")

include_directories(
  ${CMAKE_CURRENT_SOURCE_DIR}
  ${PROJECT_SOURCE_DIR}/internal/{{ app_name }}_frontend
  ${QT_INCLUDE_DIR}/QtWidgets
  )
  # ${PROJECT_SOURCE_DIR}/../ProjectB/lib/PrintHelper
  # ${PROJECT_SOURCE_DIR}/lib/utility
  # ${libpng_INCLUDE_DIR}
  # ${libbmp_INCLUDE_DIR})

add_executable(${targetName} ${${folderName}_src})

target_link_libraries(
  ${targetName}
  ${Qt5Core_LIBRARIES}
  ${Qt5Core_QTMAIN_LIBRARIES}
  ${Qt5Gui_LIBRARIES}
  ${Qt5Widgets_LIBRARIES}
  {{ app_name }}_frontend
  )
#   ${CMAKE_INSTALL_PREFIX}/lib/libPrintHelper.so
#   ${CMAKE_THREAD_LIBS_INIT}
#   utility
#   ${libpng_LIBRARY_DIR}/libpng16.so
#   ${libbmp_LIBRARY_DIR}/libbmp.so)

# Creates a folder "executables" and adds target
# project (*.vcproj) under it
set_property(TARGET ${targetName} PROPERTY FOLDER "executables")

# Adds logic to INSTALL.vcproj to copy *.exe to destination directory
install (TARGETS ${targetName} DESTINATION bin)
"""
