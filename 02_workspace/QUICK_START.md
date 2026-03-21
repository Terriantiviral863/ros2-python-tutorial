# 02_workspace 快速开始指南

## 🚀 快速体验工作空间

### 步骤1：创建工作空间并复制示例包

```bash
# 创建工作空间
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src

# 复制Python示例包
cp -r /home/jetson/ddxd/02_workspace/python_package_example .

# 复制C++示例包
cp -r /home/jetson/ddxd/02_workspace/cpp_package_example .
```

### 步骤2：构建工作空间

```bash
# 返回工作空间根目录
cd ~/ros2_ws

# 构建所有包
colcon build

# 或者使用符号链接（Python开发推荐）
colcon build --symlink-install
```

### 步骤3：设置环境变量

```bash
# 加载工作空间环境
source install/setup.bash

# 验证包是否可用
ros2 pkg list | grep example
```

---

## 🐍 测试Python包

### 运行Python发布者
```bash
# 终端1
cd ~/ros2_ws
source install/setup.bash
ros2 run python_package_example simple_publisher
```

### 运行Python订阅者
```bash
# 终端2
cd ~/ros2_ws
source install/setup.bash
ros2 run python_package_example simple_subscriber
```

---

## ⚙️ 测试C++包

### 运行C++发布者
```bash
# 终端1
cd ~/ros2_ws
source install/setup.bash
ros2 run cpp_package_example simple_publisher
```

### 运行C++订阅者
```bash
# 终端2
cd ~/ros2_ws
source install/setup.bash
ros2 run cpp_package_example simple_subscriber
```

---

## 🔍 验证和调试

### 查看节点
```bash
ros2 node list
```

### 查看话题
```bash
ros2 topic list
ros2 topic echo /example_topic
ros2 topic hz /example_topic
```

### 查看包信息
```bash
ros2 pkg list
ros2 pkg prefix python_package_example
ros2 pkg executables python_package_example
```

---

## 📝 修改代码后重新构建

### Python包（使用了--symlink-install）
```bash
# 不需要重新构建，直接运行即可
ros2 run python_package_example simple_publisher
```

### C++包
```bash
# 需要重新构建
cd ~/ros2_ws
colcon build --packages-select cpp_package_example
source install/setup.bash
ros2 run cpp_package_example simple_publisher
```

---

## 🎯 创建自己的包

### 创建Python包
```bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_python my_robot_pkg \
  --dependencies rclpy std_msgs

# 编辑代码...
# 然后构建
cd ~/ros2_ws
colcon build --packages-select my_robot_pkg
```

### 创建C++包
```bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_cmake my_sensor_pkg \
  --dependencies rclcpp std_msgs

# 编辑代码...
# 然后构建
cd ~/ros2_ws
colcon build --packages-select my_sensor_pkg
```

---

## 💡 常用技巧

### 自动加载工作空间环境
```bash
# 添加到.bashrc，每次打开终端自动加载
echo "source ~/ros2_ws/install/setup.bash" >> ~/.bashrc
```

### 只构建修改的包
```bash
colcon build --packages-select <package_name>
```

### 清理构建
```bash
cd ~/ros2_ws
rm -rf build install log
colcon build
```

### 查看构建日志
```bash
cd ~/ros2_ws
cat log/latest_build/events.log
```

---

## ❓ 常见问题

**Q: 找不到包？**
```bash
# 确保source了环境
source ~/ros2_ws/install/setup.bash
```

**Q: Python代码修改不生效？**
```bash
# 使用符号链接构建
colcon build --symlink-install
```

**Q: C++编译错误？**
```bash
# 检查CMakeLists.txt和package.xml
# 确保所有依赖都正确声明
```

---

## 📚 文件结构参考

### Python包必需文件
- `package.xml` - 包描述
- `setup.py` - 安装配置
- `setup.cfg` - 安装路径配置
- `resource/<package_name>` - 资源标记文件
- `<package_name>/__init__.py` - Python模块初始化

### C++包必需文件
- `package.xml` - 包描述
- `CMakeLists.txt` - 构建配置
- `src/` - 源代码目录

---

完成这些练习后，您将掌握ROS2的包管理和工作空间使用！
