cmake_minimum_required (VERSION 2.6)
project (DataProjection)

# should we use our own math functions?
option (USE_MYMATH 
        "Use tutorial provided math implementation" OFF) 
		
# The version number
set (Tutorial_VERSION_MAJOR 1)
set (Tutorial_VERSION_MINOR 0)

set(CMAKE_SUPPRESS_REGENERATION true)

# pass cmake settings to the source code
configure_file (
  "${PROJECT_SOURCE_DIR}/dataprojection.h.in"
  "${PROJECT_BINARY_DIR}/dataprojection.h"
)
# add the binary tree to the search path for include files
# so that we will find dataprojection.h
include_directories("${PROJECT_BINARY_DIR}")

file(GLOB SOURCES
  reader.h
  reader.cpp
  dataprojection.cpp
)

if(USE_MYMATH)
  include_directories ("${PROJECT_SOURCE_DIR}/MathFunctions")
  add_subdirectory (MathFunctions)
  set (EXTRA_LIBS ${EXTRA_LIBS} MathFunctions)
  
  file(COPY ${PROJECT_SOURCE_DIR}/MathFunctions/MathFunctions.h
        DESTINATION ${PROJECT_BINARY_DIR}/MathFunctions.h)

endif (USE_MYMATH)

# add the executable
add_executable (DataProjection ${SOURCES})

target_link_libraries (DataProjection ${EXTRA_LIBS})

# add the install targets
install (TARGETS DataProjection DESTINATION bin)
install (FILES "${PROJECT_BINARY_DIR}/dataprojection.h"        
         DESTINATION include)