# CPLEX CMake module

# =================================================================================================
# Check if path to CPLEX Studio is set
if(NOT CPLEX_STUDIO_DIR)
    message(FATAL_ERROR "Unable to find CPLEX: variable CPLEX_STUDIO_DIR not set.")
endif()


# =================================================================================================
# CPLEX headers and libraries

# Base path for CPLEX
set(CPLEX_DIR "${CPLEX_STUDIO_DIR}/cplex")

# Paths to look for CPLEX libraries
file(GLOB_RECURSE CPLEX_CANDIDATE_LIB_DIR
    LIST_DIRECTORIES true "${CPLEX_DIR}/lib/*")

set(CPLEX_LIB_DIR "${CPLEX_DIR}/lib")
foreach(dir ${CPLEX_CANDIDATE_LIB_DIR})
    #if(IS_DIRECTORY ${dir} AND NOT (${dir} MATCHES "${CPLEX_DIR}/lib[a-zA-Z0-9_/]*mdd[a-zA-Z0-9_/]*"))
    if(IS_DIRECTORY ${dir} AND NOT (${dir} MATCHES "${CPLEX_DIR}/lib[a-zA-Z0-9_/]*mda[a-zA-Z0-9_/]*"))
        list(APPEND CPLEX_LIB_DIR ${dir})
    endif()
endforeach()

# Headers
find_path(CPLEX_INCLUDE_DIR
    NAMES ilcplex/cplex.h
    HINTS ${CPLEX_DIR}
    PATH_SUFFIXES include)

# Libraries
find_library(CPLEX_LIBRARY
    NAMES cplex cplex2010
    HINTS ${CPLEX_LIB_DIR})

find_library(ILOCPLEX_LIBRARY
    NAMES ilocplex
    HINTS ${CPLEX_LIB_DIR})

list(APPEND CPLEX_LIBRARY ${ILOCPLEX_LIBRARY})
list(REVERSE CPLEX_LIBRARY)


# =================================================================================================
# CPLEX Concert API for C++

# Check if C++ language is enabled
if(CXX)

    # Base path for CPLEX
    set(CPLEX_CONCERT_DIR "${CPLEX_STUDIO_DIR}/concert")

    # Paths to look for CPLEX Concert API libraries
    file(GLOB_RECURSE CPLEX_CONCERT_CANDIDATE_LIB_DIR
        LIST_DIRECTORIES true "${CPLEX_CONCERT_DIR}/lib/*")

    set(CPLEX_CONCERT_LIB_DIR "${CPLEX_CONCERT_DIR}/lib")
    foreach(dir ${CPLEX_CONCERT_CANDIDATE_LIB_DIR})
        #if(IS_DIRECTORY ${dir} AND NOT (${dir} MATCHES "${CPLEX_CONCERT_DIR}/lib[a-zA-Z0-9_/]*mdd[a-zA-Z0-9_/]*"))
        if(IS_DIRECTORY ${dir} AND NOT (${dir} MATCHES "${CPLEX_CONCERT_DIR}/lib[a-zA-Z0-9_/]*mda[a-zA-Z0-9_/]*"))
            list(APPEND CPLEX_CONCERT_LIB_DIR ${dir})
        endif()
    endforeach()

    # Headers
    find_path(CPLEX_CXX_INCLUDE_DIR
        NAMES ilconcert/iloenv.h
        HINTS ${CPLEX_CONCERT_DIR}
        PATH_SUFFIXES include)

    list(APPEND CPLEX_INCLUDE_DIR ${CPLEX_CXX_INCLUDE_DIR})

    # Libraries
    find_library(CPLEX_CXX_LIBRARY
        NAMES concert
        HINTS ${CPLEX_CONCERT_LIB_DIR})
    
endif()


# =================================================================================================
# Provides a function intended to be used in Find Modules implementing find_package calls.

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(CPLEX DEFAULT_MSG CPLEX_LIBRARY)
