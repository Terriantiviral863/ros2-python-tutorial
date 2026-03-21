# 第二阶段：工作空间和包管理

## 学习目标

- 理解ROS2工作空间的概念和结构
- 学习使用colcon构建系统
- 创建Python和C++包
- 掌握package.xml和setup.py的配置
- 理解依赖管理

---

## ROS2工作空间结构

```
ros2_ws/                    # 工作空间根目录
├── src/                    # 源代码目录（所有包都在这里）
│   ├── my_python_pkg/      # Python包
│   └── my_cpp_pkg/         # C++包
├── build/                  # 构建目录（自动生成）
├── install/                # 安装目录（自动生成）
└── log/                    # 日志目录（自动生成）
```

---

## 练习列表

### 练习1：创建工作空间
**目标**: 理解工作空间的基本结构

**步骤**:
```bash
# 1. 创建工作空间
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws

# 2. 构建空工作空间
colcon build

# 3. 查看生成的目录
ls -la

# 4. 设置环境变量
source install/setup.bash
```

---

### 练习2：创建Python包
**目标**: 学习创建和配置Python包

**步骤**:
```bash
cd ~/ros2_ws/src

# 创建Python包
ros2 pkg create --build-type ament_python my_python_pkg \
  --dependencies rclpy std_msgs

# 查看包结构
tree my_python_pkg
```

**包结构**:
```
my_python_pkg/
├── package.xml              # 包描述文件
├── setup.py                 # Python安装配置
├── setup.cfg                # 安装配置
├── resource/                # 资源文件
├── test/                    # 测试文件
└── my_python_pkg/           # Python模块目录
    └── __init__.py
```

**实践**: 参考 `python_package_example/` 目录

---

### 练习3：创建C++包
**目标**: 学习创建和配置C++包

**步骤**:
```bash
cd ~/ros2_ws/src

# 创建C++包
ros2 pkg create --build-type ament_cmake my_cpp_pkg \
  --dependencies rclcpp std_msgs

# 查看包结构
tree my_cpp_pkg
```

**包结构**:
```
my_cpp_pkg/
├── CMakeLists.txt          # CMake配置文件
├── package.xml             # 包描述文件
├── include/                # 头文件目录
│   └── my_cpp_pkg/
├── src/                    # 源代码目录
└── test/                   # 测试文件
```

**实践**: 参考 `cpp_package_example/` 目录

---

### 练习4：构建和运行包
**目标**: 学习使用colcon构建和运行包

**步骤**:
```bash
# 1. 返回工作空间根目录
cd ~/ros2_ws

# 2. 构建所有包
colcon build

# 3. 构建特定包
colcon build --packages-select my_python_pkg

# 4. 设置环境变量
source install/setup.bash

# 5. 运行节点
ros2 run my_python_pkg my_node
```

**常用colcon命令**:
```bash
colcon build                              # 构建所有包
colcon build --packages-select <pkg>     # 构建指定包
colcon build --symlink-install           # 符号链接安装（Python推荐）
colcon build --cmake-args -DCMAKE_BUILD_TYPE=Release  # Release模式
colcon test                               # 运行测试
colcon test-result --all                  # 查看测试结果
```

---

## 重要文件说明

### package.xml
包的元数据文件，包含：
- 包名、版本、描述
- 维护者信息
- 许可证
- 依赖关系

### setup.py (Python包)
Python包的安装配置：
- 入口点（可执行文件）
- 包数据
- 依赖项

### CMakeLists.txt (C++包)
C++包的构建配置：
- 编译选项
- 依赖查找
- 可执行文件定义
- 安装规则

---

## 依赖类型

### 1. build依赖
构建时需要的包
```xml
<build_depend>rclcpp</build_depend>
```

### 2. exec依赖
运行时需要的包
```xml
<exec_depend>rclcpp</exec_depend>
```

### 3. 同时依赖
构建和运行都需要
```xml
<depend>rclcpp</depend>
```

### 4. test依赖
测试时需要
```xml
<test_depend>ament_lint_auto</test_depend>
```

---

## 实践项目

本目录包含两个完整的示例包：

### 1. `python_package_example/`
- 简单的发布者节点
- 简单的订阅者节点
- 完整的package.xml和setup.py配置

### 2. `cpp_package_example/`
- C++发布者节点
- C++订阅者节点
- 完整的CMakeLists.txt和package.xml配置

---

## 练习任务

### 任务1：创建自己的Python包
1. 创建名为 `my_robot_pkg` 的Python包
2. 添加一个发布者节点，发布机器人状态
3. 添加一个订阅者节点，接收并显示状态
4. 构建并测试

### 任务2：创建自己的C++包
1. 创建名为 `my_sensor_pkg` 的C++包
2. 实现一个简单的传感器数据发布节点
3. 构建并运行

### 任务3：包依赖管理
1. 创建一个包，依赖于之前创建的包
2. 正确配置package.xml中的依赖
3. 验证依赖关系

---

## 常见问题

### Q1: colcon build失败？
```bash
# 清理构建
rm -rf build install log
colcon build
```

### Q2: 找不到包？
```bash
# 确保source了环境
source install/setup.bash
# 或添加到.bashrc
echo "source ~/ros2_ws/install/setup.bash" >> ~/.bashrc
```

### Q3: Python代码修改后不生效？
```bash
# 使用符号链接安装
colcon build --symlink-install
```

---

## 最佳实践

1. **使用符号链接** - Python包开发时使用 `--symlink-install`
2. **分离工作空间** - 不同项目使用不同工作空间
3. **版本控制** - 只提交src目录，不提交build/install/log
4. **依赖明确** - 在package.xml中明确列出所有依赖
5. **命名规范** - 包名使用小写和下划线

---

## 下一步

完成所有练习后，进入 `03_communication/` 学习更高级的通信机制。
