# Launch文件快速开始指南

## 前提条件

确保已安装ROS2 Humble并source了环境：
```bash
source /opt/ros/humble/setup.bash
```

## 运行示例

### 1. 简单Launch
启动单个节点：
```bash
cd /home/jetson/ddxd/04_launch
ros2 launch simple_launch.py
```

### 2. 多节点Launch
同时启动多个节点：
```bash
ros2 launch multi_node_launch.py
```

查看运行的节点：
```bash
# 新终端
ros2 node list
ros2 topic list
```

### 3. 参数配置Launch
使用YAML配置文件：
```bash
ros2 launch params_launch.py
```

使用自定义参数：
```bash
ros2 launch params_launch.py use_sim_time:=true
```

### 4. 命名空间Launch
启动多个机器人实例：
```bash
ros2 launch namespace_launch.py
```

查看命名空间：
```bash
ros2 node list
# 输出：
# /robot1/listener
# /robot1/talker
# /robot2/listener
# /robot2/talker
# /robot3/listener
# /robot3/talker
```

查看话题：
```bash
ros2 topic list
# 输出：
# /robot1/chatter
# /robot2/chatter
# /robot3/chatter
```

### 5. 条件Launch
仿真模式：
```bash
ros2 launch conditional_launch.py use_sim:=true
```

真实硬件模式：
```bash
ros2 launch conditional_launch.py use_sim:=false
```

禁用摄像头：
```bash
ros2 launch conditional_launch.py enable_camera:=false
```

组合参数：
```bash
ros2 launch conditional_launch.py use_sim:=true enable_camera:=false robot_name:=robot_alpha
```

### 6. 组合Launch
启动完整系统：
```bash
ros2 launch composed_launch.py
```

使用命名空间：
```bash
ros2 launch composed_launch.py namespace:=my_robot
```

## 查看Launch参数

查看Launch文件支持的参数：
```bash
ros2 launch conditional_launch.py --show-args
```

## 调试技巧

### 1. 查看节点信息
```bash
ros2 node list
ros2 node info /node_name
```

### 2. 查看话题
```bash
ros2 topic list
ros2 topic echo /topic_name
ros2 topic hz /topic_name
```

### 3. 查看参数
```bash
ros2 param list
ros2 param get /node_name param_name
```

### 4. 使用rqt_graph可视化
```bash
rqt_graph
```

## 常见问题

### Q: Launch文件启动失败？
检查ROS2环境是否正确source：
```bash
echo $ROS_DISTRO
# 应该输出: humble
```

### Q: 找不到demo_nodes_cpp包？
安装demo节点：
```bash
sudo apt install ros-humble-demo-nodes-cpp
```

### Q: 如何停止Launch？
在运行Launch的终端按 `Ctrl+C`

## 下一步

1. 修改配置文件 `config/params.yaml` 和 `config/robot_config.yaml`
2. 创建自己的Launch文件
3. 结合前面学习的自定义节点使用Launch文件
4. 进入 `05_tf2/` 学习坐标变换

## 练习建议

1. 创建一个Launch文件启动03_communication中的自定义消息节点
2. 使用命名空间启动多个机器人实例
3. 创建条件Launch文件在不同模式间切换
4. 编写YAML配置文件管理复杂参数
