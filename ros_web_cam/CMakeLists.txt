cmake_minimum_required(VERSION 2.8.3)
project(ros_web_cam)

find_package(catkin REQUIRED COMPONENTS roscpp rospy)

catkin_package()

include_directories(include
  ${catkin_INCLUDE_DIRS}
)
