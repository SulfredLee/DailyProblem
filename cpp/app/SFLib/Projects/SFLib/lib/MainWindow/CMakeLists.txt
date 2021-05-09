set(targetName "MainWindow")
get_filename_component(folderName ${CMAKE_CURRENT_SOURCE_DIR} NAME)
string(REPLACE " " "_" folderName ${folderName})

# Handle QT libraries
file(GLOB ${folderName}_src "${CMAKE_CURRENT_SOURCE_DIR}/*.cpp")
file(GLOB ${folderName}_hdr "${CMAKE_CURRENT_SOURCE_DIR}/*.h")
file(GLOB ${folderName}_ui "${CMAKE_CURRENT_SOURCE_DIR}/*.ui")
# set(${folderName}_rcc ${CMAKE_CURRENT_SOURCE_DIR}/resource.qrc)
qt5_wrap_cpp(${folderName}_hdr_moc ${${folderName}_hdr})
# qt5_wrap_ui (${folderName}_ui_moc  ${${folderName}_src} ${${folderName}_ui})
qt5_wrap_ui (${folderName}_ui_moc  ${${folderName}_ui})
# qt5_add_resources(${folderName}_rcc_moc ${${folderName}_rcc})

# handle other resource
# file(GLOB PlayerEngine_inc
#   "${PROJECT_SOURCE_DIR}/BackEnd/PlayerEngine/*.h")
# file(GLOB PlayerEngine_src
#   "${PROJECT_SOURCE_DIR}/BackEnd/PlayerEngine/*.cpp")

include_directories(
  ${QT_INCLUDE_DIR}
  ${QT_INCLUDE_DIR}/QtWidgets
  ${CMAKE_CURRENT_SOURCE_DIR}
  ${PROJECT_BINARY_DIR}/lib/${folderName}
  # ${libpcap_INCLUDE_DIR}
  # ${PROJECT_SOURCE_DIR}/BackEnd/PlayerEngine
  )

if (UNIX)
  # handle library files for installation
  file(GLOB libqt_libFile "${QT_LIBRARY_DIR}/*so*")
else ()
endif ()

message(STATUS "qt include: " ${QT_INCLUDE_DIR})
message(STATUS "binary folder: " ${PROJECT_BINARY_DIR}/${folderName})
message(STATUS "cmake current dir: " ${CMAKE_CURRENT_SOURCE_DIR})
message(STATUS "source file: " ${${folderName}_ui_moc})
add_library(
  ${targetName}
  ${${folderName}_src}
  ${${folderName}_hdr}
  ${${folderName}_hdr_moc}
  ${${folderName}_ui_moc}
  # ${${folderName}_rcc_moc}
  # ${PlayerEngine_src}
  )

target_link_libraries(
  ${targetName}
  ${Qt5Widgets_LIBRARIES}
  )

# Creates a folder "libraries" and adds target project (*.vcproj) under it
set_property(TARGET ${targetName} PROPERTY FOLDER "libraries")

# Adds logic to INSTALL.vcproj to copy *.lib to destination directory
install (TARGETS ${targetName} DESTINATION lib)
install (FILES ${${folderName}_hdr_proxy} DESTINATION include)
install (FILES ${libqt_libFile} DESTINATION lib)
