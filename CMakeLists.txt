cmake_minimum_required(VERSION 3.8)
project(jetson_stm32_poc_msgs)

# Enable good compiler warnings (optional but recommended)
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Required packages
find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)

# Generate message interfaces
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/DataVector.msg"
)

# Export runtime dependency so other packages can use the message
ament_export_dependencies(rosidl_default_runtime)

# Required at the end
ament_package()
