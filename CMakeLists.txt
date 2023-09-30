cmake_minimum_required(VERSION 3.13)


# =================================================================================================
# Project info

project(mip-solver-prediction
        VERSION "0.0.1"
        DESCRIPTION "Prediction of computational runtime for solving MIP problems"
        HOMEPAGE_URL "https://github.com/andremaravilha/mip-solver-prediction")


# =================================================================================================
# C++ standard and other settings

set(CXX ON)
enable_language(CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_EXTENSIONS OFF)
add_definitions(-D_GLIBCXX_USE_CXX11_ABI=0)
add_definitions(-DIL_STD)
add_definitions(-D_ALLOW_ITERATOR_DEBUG_LEVEL_MISMATCH)

# If build type is not set, then use "Release"
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE "Release")
endif()

# Set MS Visual Studio compiler with static runtime libraries, if MSVS is the compiler
if(MSVC AND MT)
    set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} /MT")
    set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} /MTd")
    set(CMAKE_C_FLAGS_RELEASE "${CMAKE_C_FLAGS_RELEASE} /MT")
    set(CMAKE_C_FLAGS_DEBUG "${CMAKE_C_FLAGS_DEBUG} /MTd")
endif()


# =================================================================================================
# Third-party dependencies

list(APPEND CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake")

# Gurobi
find_package(GUROBI REQUIRED)

# CPLEX
#set(CPLEX_STUDIO_DIR "C:/Program Files/IBM/ILOG/CPLEX_Studio201")
#find_package(CPLEX REQUIRED)

# FICO Xpress
#find_package(XPRESS REQUIRED)


# =================================================================================================
# Paths to search for headers and libraries
include_directories(
        ${PROJECT_SOURCE_DIR}/lib/
        ${GUROBI_INCLUDE_DIR}
        
        )


# =================================================================================================
# Source files

set(SOURCE_FILES
        src/main.cpp
        src/solvers.h src/solvers.cpp)


# =================================================================================================
# Targets

add_executable(mip-solve ${SOURCE_FILES})
target_link_libraries(mip-solve optimized ${GUROBI_CXX_LIBRARY} debug ${GUROBI_CXX_DEBUG_LIBRARY})

target_link_libraries(mip-solve ${GUROBI_LIBRARY})
