content_st = """
set(targetName "{{ module_name }}")
get_filename_component(folderName ${CMAKE_CURRENT_SOURCE_DIR} NAME)
string(REPLACE " " "_" folderName ${folderName})

file(GLOB ${folderName}_inc
  "${CMAKE_CURRENT_SOURCE_DIR}/*.h")
file(GLOB ${folderName}_src
  "${CMAKE_CURRENT_SOURCE_DIR}/*.cpp")

include_directories(
  ${CMAKE_CURRENT_SOURCE_DIR}
  # ${PROJECT_SOURCE_DIR}/internal/utility
  # ${Boost_INCLUDE_DIR}
  )

# state that this project is a library
add_library(${targetName} STATIC ${${folderName}_src}) # static library

if (UNIX)
  #   target_link_libraries(
  #     ${targetName}
  #     ${CMAKE_THREAD_LIBS_INIT}
  #     )
else ()
endif ()

# Creates a folder "libraries" and adds target project (*.vcproj) under it
set_property(TARGET ${targetName} PROPERTY FOLDER "libraries")

# Adds logic to INSTALL.vcproj to copy *.a to destination directory
install (TARGETS ${targetName} DESTINATION internal)
install (FILES ${${folderName}_inc} DESTINATION include)
"""
