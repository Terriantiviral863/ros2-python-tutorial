# 第三阶段：通信机制深入

## 学习目标

- 深入理解话题通信机制
- 学习创建自定义消息类型
- 掌握服务的高级用法
- 理解动作(Action)通信
- 学习多节点协作

---

## 目录结构

```
03_communication/
├── README.md                           # 本文件
├── custom_interfaces/                  # 自定义接口包
│   ├── msg/                           # 自定义消息
│   ├── srv/                           # 自定义服务
│   ├── action/                        # 自定义动作
│   └── package.xml
├── topic_communication.py              # 话题通信示例
├── custom_msg_publisher.py             # 自定义消息发布者
├── custom_msg_subscriber.py            # 自定义消息订阅者
├── async_service_server.py             # 异步服务服务器
├── async_service_client.py             # 异步服务客户端
├── action_server.py                    # 动作服务器
├── action_client.py                    # 动作客户端
└── multi_node_system.py                # 多节点协作示例
```

---

## 练习列表

### 练习1：话题通信进阶
**文件**: `topic_communication.py`
**目标**: 理解QoS配置和多话题通信

**任务**:
1. 配置不同的QoS策略
2. 在单个节点中处理多个话题
3. 理解发布频率控制

**运行**:
```bash
python3 topic_communication.py
```

**验证**:
```bash
ros2 topic list
ros2 topic info /sensor_data --verbose
ros2 topic hz /sensor_data
```

---

### 练习2：自定义消息类型
**目录**: `custom_interfaces/`
**目标**: 创建和使用自定义消息

**步骤**:
```bash
# 1. 进入工作空间
cd /home/jetson/ddxd

# 2. 构建自定义接口包
colcon build --packages-select custom_interfaces

# 3. 设置环境
source install/setup.bash

# 4. 运行发布者和订阅者
python3 03_communication/custom_msg_publisher.py
python3 03_communication/custom_msg_subscriber.py
```

**验证**:
```bash
ros2 interface show custom_interfaces/msg/RobotStatus
ros2 topic echo /robot_status
```

---

### 练习3：异步服务
**文件**: `async_service_server.py` 和 `async_service_client.py`
**目标**: 学习异步服务调用

**任务**:
1. 实现异步服务服务器
2. 使用异步客户端调用服务
3. 处理服务超时

**运行**:
```bash
# 终端1
python3 async_service_server.py

# 终端2
python3 async_service_client.py
```

**验证**:
```bash
ros2 service list
ros2 service type /compute_trajectory
ros2 service call /compute_trajectory custom_interfaces/srv/ComputeTrajectory "{start: {x: 0.0, y: 0.0}, goal: {x: 5.0, y: 5.0}}"
```

---

### 练习4：动作通信
**文件**: `action_server.py` 和 `action_client.py`
**目标**: 理解动作的使用场景和实现

**任务**:
1. 创建动作服务器处理长时间任务
2. 实现动作客户端发送目标
3. 处理反馈和结果
4. 实现取消功能

**运行**:
```bash
# 终端1
python3 action_server.py

# 终端2
python3 action_client.py
```

**验证**:
```bash
ros2 action list
ros2 action info /fibonacci
ros2 action send_goal /fibonacci custom_interfaces/action/Fibonacci "{order: 10}"
```

---

### 练习5：多节点协作
**文件**: `multi_node_system.py`
**目标**: 实现多个节点协同工作

**任务**:
1. 创建传感器节点
2. 创建处理节点
3. 创建控制节点
4. 实现节点间通信

**运行**:
```bash
python3 multi_node_system.py
```

---

## 自定义接口说明

### 消息 (msg)
- **RobotStatus.msg**: 机器人状态信息
- **SensorData.msg**: 传感器数据

### 服务 (srv)
- **ComputeTrajectory.srv**: 计算轨迹服务
- **SetMode.srv**: 设置模式服务

### 动作 (action)
- **Fibonacci.action**: 斐波那契数列计算
- **Navigate.action**: 导航动作

---

## QoS (Quality of Service) 配置

### 常用QoS配置

```python
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy

# 传感器数据 - 最新数据优先
sensor_qos = QoSProfile(
    reliability=ReliabilityPolicy.BEST_EFFORT,
    history=HistoryPolicy.KEEP_LAST,
    depth=10
)

# 可靠通信 - 保证送达
reliable_qos = QoSProfile(
    reliability=ReliabilityPolicy.RELIABLE,
    history=HistoryPolicy.KEEP_ALL,
    durability=DurabilityPolicy.TRANSIENT_LOCAL
)
```

### QoS策略说明

1. **Reliability (可靠性)**
   - `BEST_EFFORT`: 尽力传输，可能丢包（适合传感器数据）
   - `RELIABLE`: 可靠传输，保证送达（适合命令）

2. **History (历史)**
   - `KEEP_LAST`: 保留最后N条消息
   - `KEEP_ALL`: 保留所有消息

3. **Durability (持久性)**
   - `VOLATILE`: 只对当前订阅者有效
   - `TRANSIENT_LOCAL`: 对后来的订阅者也有效

---

## 通信模式对比

| 特性 | 话题(Topic) | 服务(Service) | 动作(Action) |
|------|-------------|---------------|--------------|
| 通信模式 | 发布/订阅 | 请求/响应 | 目标/反馈/结果 |
| 方向 | 一对多 | 一对一 | 一对一 |
| 同步性 | 异步 | 同步/异步 | 异步 |
| 适用场景 | 传感器数据 | 快速计算 | 长时间任务 |
| 反馈 | 无 | 无 | 有 |
| 可取消 | 不适用 | 不适用 | 可以 |

---

## 实践任务

### 任务1：创建温度监控系统
1. 创建温度传感器节点（发布温度数据）
2. 创建监控节点（订阅并显示温度）
3. 创建报警节点（温度过高时发出警告）
4. 使用自定义消息类型

### 任务2：实现计算服务
1. 创建数学计算服务（加减乘除）
2. 实现异步客户端
3. 处理错误情况（如除零）

### 任务3：实现文件下载动作
1. 创建文件下载动作服务器
2. 提供下载进度反馈
3. 支持取消下载
4. 返回下载结果

---

## 调试技巧

### 1. 查看通信图
```bash
# 安装rqt_graph
sudo apt install ros-humble-rqt-graph

# 运行
rqt_graph
```

### 2. 监控话题
```bash
# 实时显示消息
ros2 topic echo /topic_name

# 显示发布频率
ros2 topic hz /topic_name

# 显示带宽
ros2 topic bw /topic_name
```

### 3. 测试服务
```bash
# 列出服务
ros2 service list

# 查看服务类型
ros2 service type /service_name

# 调用服务
ros2 service call /service_name service_type "request_data"
```

### 4. 测试动作
```bash
# 列出动作
ros2 action list

# 查看动作类型
ros2 action info /action_name

# 发送目标
ros2 action send_goal /action_name action_type "goal_data" --feedback
```

---

## 常见问题

### Q1: 自定义消息找不到？
```bash
# 确保构建了接口包
colcon build --packages-select custom_interfaces
source install/setup.bash
```

### Q2: QoS不匹配？
检查发布者和订阅者的QoS配置是否兼容。

### Q3: 服务调用超时？
增加超时时间或检查服务器是否正在运行。

---

## 最佳实践

1. **选择合适的通信方式**
   - 传感器数据 → 话题
   - 快速查询 → 服务
   - 长时间任务 → 动作

2. **QoS配置**
   - 根据数据特性选择合适的QoS
   - 传感器数据使用BEST_EFFORT
   - 命令使用RELIABLE

3. **错误处理**
   - 总是处理服务调用失败
   - 动作要处理取消和中断

4. **命名规范**
   - 话题名使用小写和下划线
   - 使用命名空间避免冲突

---

## 下一步

完成所有练习后，进入 `04_launch/` 学习Launch文件系统。
