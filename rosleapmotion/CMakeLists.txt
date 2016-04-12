cmake_minimum_required(VERSION 2.8.3)
project(leap_motion)

find_package(catkin REQUIRED COMPONENTS roscpp rospy std_msgs geometry_msgs message_generation tf)

add_message_files(
    FILES
    leap.msg
    leapros.msg
)

generate_messages(
   DEPENDENCIES
   std_msgs
   geometry_msgs
   reflex_msgs
)

catkin_package(
   INCLUDE_DIRS include
#  LIBRARIES leap_motion
   CATKIN_DEPENDS roscpp rospy std_msgs message_runtime
#  DEPENDS system_lib
)

include_directories(include
  ${catkin_INCLUDE_DIRS}
)

add_executable(tf_listener
  src/tf_listener.cpp
)

target_link_libraries(tf_listener ${catkin_LIBRARIES})

install(PROGRAMS
  scripts/leap_interface.py scripts/sender.py scripts/subscriber.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)


