content_st = """
include (ExternalProject)

# Add External project
set (thisProject "external_{{ module_name }}")
ExternalProject_Add (
  ${thisProject}

  PREFIX Projects/${thisProject}


  GIT_REPOSITORY https://github.com/taglib/taglib
  GIT_TAG        v1.11.1
  GIT_SHALLOW    ON

  BUILD_ALWAYS   ON
  INSTALL_DIR    ${CMAKE_INSTALL_PREFIX}

  CMAKE_CACHE_ARGS
  -DBUILD_SHARED_LIBS:BOOL=ON
  -DENABLE_STATIC_RUNTIME:BOOL=OFF
  -DBUILD_EXAMPLES:BOOL=ON
  -DCMAKE_BUILD_TYPE:STRING=${CMAKE_BUILD_TYPE}
  -DCMAKE_INSTALL_PREFIX:PATH=<INSTALL_DIR>
  -DCMAKE_TOOLCHAIN_FILE:FILE=${CMAKE_TOOLCHAIN_FILE}

  BUILD_COMMAND ${CMAKE_COMMAND} --build <BINARY_DIR>
  )
"""
