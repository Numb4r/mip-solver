# FICO Xpress CMake module

# =================================================================================================
# Check if path to Gurobi is set

if(NOT XPRESS_DIR)
    if (DEFINED ENV{XPRESSDIR})
        set(XPRESS_DIR "$ENV{XPRESSDIR}")
    endif()
endif()

if (NOT XPRESS_DIR)
    message(FATAL_ERROR "Unable to find FICO Xpress: variable XPRESS_DIR not set.")
endif()


# =================================================================================================
# Headers

# Find path to FICO Xpress headers
find_path(XPRESS_INCLUDE_DIR
    NAMES xprs.h
    HINTS ${XPRESS_DIR}
    PATH_SUFFIXES include)


# =================================================================================================
# Libraries

# Find FICO Xpress libraries
find_library(XPRESS_XPRS_LIBRARY
    NAMES xprs
    HINTS ${XPRESS_DIR}
    PATH_SUFFIXES lib)

find_library(XPRESS_XPRB_LIBRARY
        NAMES xprb
        HINTS ${XPRESS_DIR}
        PATH_SUFFIXES lib)

set(XPRESS_LIBRARY ${XPRESS_XPRB_LIBRARY} ${XPRESS_XPRS_LIBRARY})


# =================================================================================================
# Provides a function intended to be used in Find Modules implementing find_package calls.

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(XPRESS DEFAULT_MSG XPRESS_LIBRARY)
