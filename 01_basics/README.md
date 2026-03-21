# 第一阶段：ROS2基础

## 学习目标

- 理解ROS2的核心概念
- 创建第一个ROS2节点
- 掌握发布者/订阅者模式
- 学习服务和参数的使用

## 练习列表

### 练习1：Hello ROS2
**文件**: `hello_ros2.py`
**目标**: 创建你的第一个ROS2节点

**任务**:
1. 运行示例节点
2. 查看节点信息
3. 理解节点的生命周期

**运行**:
```bash
python3 hello_ros2.py
```

**验证**:
```bash
# 在另一个终端
ros2 node list
ros2 node info /hello_node
```

---

### 练习2：发布者和订阅者
**文件**: `publisher.py` 和 `subscriber.py`
**目标**: 理解话题通信机制

**任务**:
1. 运行发布者节点，发布字符串消息
2. 运行订阅者节点，接收消息
3. 使用命令行工具查看话题

**运行**:
```bash
# 终端1
python3 publisher.py

# 终端2
python3 subscriber.py
```

**验证**:
```bash
ros2 topic list
ros2 topic echo /chatter
ros2 topic info /chatter
ros2 topic hz /chatter
```

---

### 练习3：服务
**文件**: `service_server.py` 和 `service_client.py`
**目标**: 学习服务的请求/响应模式

**任务**:
1. 启动服务服务器
2. 使用客户端调用服务
3. 理解同步通信

**运行**:
```bash
# 终端1
python3 service_server.py

# 终端2
python3 service_client.py
```

**验证**:
```bash
ros2 service list
ros2 service type /add_two_ints
ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 5, b: 3}"
```

---

### 练习4：参数
**文件**: `parameter_node.py`
**目标**: 学习参数的声明和使用

**任务**:
1. 声明和使用参数
2. 动态修改参数
3. 理解参数回调

**运行**:
```bash
python3 parameter_node.py
```

**验证**:
```bash
ros2 param list
ros2 param get /param_node my_parameter
ros2 param set /param_node my_parameter "new_value"
```

---

## 学习笔记

完成每个练习后，在 `/home/jetson/ddxd/notes/` 目录下记录：
- 遇到的问题
- 解决方案
- 心得体会

## 常用命令速查

```bash
# 节点相关
ros2 node list                    # 列出所有节点
ros2 node info <node_name>        # 查看节点信息

# 话题相关
ros2 topic list                   # 列出所有话题
ros2 topic echo <topic_name>      # 显示话题消息
ros2 topic info <topic_name>      # 查看话题信息
ros2 topic hz <topic_name>        # 显示发布频率

# 服务相关
ros2 service list                 # 列出所有服务
ros2 service type <service_name>  # 查看服务类型
ros2 service call <service_name> <service_type> <arguments>

# 参数相关
ros2 param list                   # 列出所有参数
ros2 param get <node_name> <param_name>
ros2 param set <node_name> <param_name> <value>

# 接口相关
ros2 interface list               # 列出所有接口
ros2 interface show <interface_name>
```

## 下一步

完成所有练习后，进入 `02_workspace/` 学习工作空间和包管理。
