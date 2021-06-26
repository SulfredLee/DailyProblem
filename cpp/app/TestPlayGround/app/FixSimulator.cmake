include (ExternalProject)

# Add External FixSimulator
set (thisProject "FixSimulator")
ExternalProject_Add (
  ${thisProject}

  PREFIX Projects/${thisProject}

  SOURCE_DIR ${CMAKE_CURRENT_LIST_DIR}/${thisProject}

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

