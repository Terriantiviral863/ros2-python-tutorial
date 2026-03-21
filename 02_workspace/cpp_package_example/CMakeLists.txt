cmake_minimum_required(VERSION 3.8)
project(cpp_package_example)

# 编译选项
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# 查找依赖
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

# 添加可执行文件 - 发布者
add_executable(simple_publisher src/simple_publisher.cpp)
ament_target_dependencies(simple_publisher rclcpp std_msgs)

# 添加可执行文件 - 订阅者
add_executable(simple_subscriber src/simple_subscriber.cpp)
ament_target_dependencies(simple_subscriber rclcpp std_msgs)

# 安装可执行文件
install(TARGETS
  simple_publisher
  simple_subscriber
  DESTINATION lib/${PROJECT_NAME}
)

# 测试
if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
