cmake_minimum_required(VERSION 3.14)
project( cvat_cpp )

file(GLOB_RECURSE SOURCES "*.cpp")

find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})

# add the executables
foreach(sourcefile ${SOURCES})
    get_filename_component(name ${sourcefile} NAME_WE)
    add_executable(${name} ${sourcefile})
    target_link_libraries(
        ${name}  
        ${OpenCV_LIBS}
    )

    endforeach(sourcefile ${SOURCES})
