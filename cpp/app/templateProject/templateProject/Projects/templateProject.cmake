include (ExternalProject)

# Add External templateProject
set (templateProject "templateProject")
ExternalProject_Add (
  ${templateProject}

  PREFIX Projects/${templateProject}
  SOURCE_DIR ${PROJECT_SOURCE_DIR}/${templateProject}

  BUILD_ALWAYS   ON
  INSTALL_DIR    ${CMAKE_INSTALL_PREFIX}

  CMAKE_CACHE_ARGS
  -DBUILD_SHARED_LIBS:BOOL=ON
  -DENABLE_STATIC_RUNTIME:BOOL=OFF
  -DBUILD_EXAMPLES:BOOL=ON
  -DCMAKE_BUILD_TYPE:STRING=${CMAKE_BUILD_TYPE}
  -DCMAKE_INSTALL_PREFIX:PATH=<INSTALL_DIR>

  BUILD_COMMAND ${CMAKE_COMMAND} --build <BINARY_DIR>
  )


