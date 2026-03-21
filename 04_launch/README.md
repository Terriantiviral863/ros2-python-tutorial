# 第四阶段：Launch文件系统

## 学习目标

- 理解ROS2 Launch系统
- 学习编写Python Launch文件
- 掌握参数配置和传递
- 理解节点组合和命名空间
- 学习条件启动和事件处理

---

## 目录结构

```
04_launch/
├── README.md                           # 本文件
├── simple_launch.py                    # 简单启动文件
├── multi_node_launch.py                # 多节点启动
├── params_launch.py                    # 参数配置启动
├── namespace_launch.py                 # 命名空间启动
├── conditional_launch.py               # 条件启动
├── composed_launch.py                  # 组合启动
├── config/                             # 配置文件目录
│   ├── params.yaml                    # 参数配置文件
│   └── robot_config.yaml              # 机器人配置
└── nodes/                              # 测试节点
    ├── talker.py
    └── listener.py
```

---

## Launch文件基础

### 什么是Launch文件？

Launch文件用于：
- 同时启动多个节点
- 配置节点参数
- 设置命名空间和重映射
- 条件启动
- 事件处理

### Python Launch文件结构

```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='package_name',
            executable='node_name',
            name='custom_node_name',
            parameters=[{'param_name': param_value}],
            remappings=[('old_topic', 'new_topic')],
            namespace='robot1'
        )
    ])
```

---

## 练习列表

### 练习1：简单Launch文件
**文件**: `simple_launch.py`
**目标**: 创建第一个Launch文件

**运行**:
```bash
ros2 launch 04_launch simple_launch.py
```

**说明**:
- 启动单个节点
- 理解Launch文件基本结构
- 学习节点配置

---

### 练习2：多节点启动
**文件**: `multi_node_launch.py`
**目标**: 同时启动多个节点

**运行**:
```bash
ros2 launch 04_launch multi_node_launch.py
```

**说明**:
- 启动发布者和订阅者
- 配置不同的节点参数
- 理解节点间通信

---

### 练习3：参数配置
**文件**: `params_launch.py` 和 `config/params.yaml`
**目标**: 使用YAML文件配置参数

**运行**:
```bash
ros2 launch 04_launch params_launch.py
```

**说明**:
- 从YAML文件加载参数
- 命令行参数覆盖
- 参数验证

---

### 练习4：命名空间
**文件**: `namespace_launch.py`
**目标**: 使用命名空间管理多个相同节点

**运行**:
```bash
ros2 launch 04_launch namespace_launch.py
```

**说明**:
- 创建多个机器人实例
- 使用命名空间隔离
- 话题重映射

---

### 练习5：条件启动
**文件**: `conditional_launch.py`
**目标**: 根据条件启动不同节点

**运行**:
```bash
# 启动模拟模式
ros2 launch 04_launch conditional_launch.py use_sim:=true

# 启动真实模式
ros2 launch 04_launch conditional_launch.py use_sim:=false
```

**说明**:
- 声明Launch参数
- 条件判断
- 不同配置切换

---

### 练习6：组合Launch
**文件**: `composed_launch.py`
**目标**: 包含其他Launch文件

**运行**:
```bash
ros2 launch 04_launch composed_launch.py
```

**说明**:
- 包含其他Launch文件
- 模块化Launch配置
- 复杂系统启动

---

## Launch文件元素

### 1. Node - 节点

```python
Node(
    package='my_package',           # 包名
    executable='my_node',            # 可执行文件名
    name='custom_name',              # 自定义节点名
    namespace='robot1',              # 命名空间
    parameters=[{                    # 参数
        'param1': 'value1',
        'param2': 42
    }],
    remappings=[                     # 话题重映射
        ('old_topic', 'new_topic')
    ],
    arguments=['--ros-args'],        # 命令行参数
    output='screen',                 # 输出到屏幕
    respawn=True,                    # 崩溃后重启
    respawn_delay=2.0               # 重启延迟
)
```

### 2. DeclareLaunchArgument - 声明参数

```python
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

DeclareLaunchArgument(
    'param_name',
    default_value='default',
    description='参数描述'
)
```

### 3. IncludeLaunchDescription - 包含其他Launch

```python
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

IncludeLaunchDescription(
    PythonLaunchDescriptionSource([
        get_package_share_directory('package_name'),
        '/launch/other_launch.py'
    ]),
    launch_arguments={'arg': 'value'}.items()
)
```

### 4. GroupAction - 分组

```python
from launch.actions import GroupAction

GroupAction([
    Node(...),
    Node(...)
])
```

### 5. ExecuteProcess - 执行进程

```python
from launch.actions import ExecuteProcess

ExecuteProcess(
    cmd=['echo', 'Hello ROS2'],
    output='screen'
)
```

---

## 参数配置文件 (YAML)

### 基本格式

```yaml
# config/params.yaml
node_name:
  ros__parameters:
    param1: value1
    param2: 42
    param3: true
    param4: [1, 2, 3]
    nested:
      sub_param: "nested value"
```

### 加载参数文件

```python
import os
from ament_index_python.packages import get_package_share_directory

config_file = os.path.join(
    get_package_share_directory('package_name'),
    'config',
    'params.yaml'
)

Node(
    package='package_name',
    executable='node_name',
    parameters=[config_file]
)
```

---

## 常用Launch技巧

### 1. 条件启动

```python
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import LaunchConfiguration

Node(
    package='my_package',
    executable='my_node',
    condition=IfCondition(LaunchConfiguration('use_sim'))
)
```

### 2. 话题重映射

```python
Node(
    package='my_package',
    executable='my_node',
    remappings=[
        ('input_topic', 'sensor/data'),
        ('output_topic', 'processed/data')
    ]
)
```

### 3. 命名空间

```python
# 单个节点
Node(
    package='my_package',
    executable='my_node',
    namespace='robot1'
)

# 分组命名空间
from launch_ros.actions import PushRosNamespace

GroupAction([
    PushRosNamespace('robot1'),
    Node(...),
    Node(...)
])
```

### 4. 日志级别

```python
Node(
    package='my_package',
    executable='my_node',
    arguments=['--ros-args', '--log-level', 'debug']
)
```

---

## 实践任务

### 任务1：创建多机器人系统
1. 创建Launch文件启动3个机器人
2. 每个机器人有独立的命名空间
3. 配置不同的初始位置参数

### 任务2：模拟与真实切换
1. 创建条件Launch文件
2. 模拟模式启动仿真节点
3. 真实模式启动硬件驱动节点

### 任务3：分层Launch系统
1. 创建传感器Launch文件
2. 创建导航Launch文件
3. 创建主Launch文件包含所有子系统

---

## 调试技巧

### 1. 查看Launch文件信息

```bash
# 列出包中的Launch文件
ros2 launch <package_name> --show-args

# 查看Launch参数
ros2 launch <package_name> <launch_file> --show-args
```

### 2. 打印Launch配置

```python
from launch.actions import LogInfo

LogInfo(msg='Launch configuration loaded')
```

### 3. 事件处理

```python
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessStart, OnProcessExit

RegisterEventHandler(
    OnProcessStart(
        target_action=node1,
        on_start=[LogInfo(msg='Node started')]
    )
)
```

---

## 常见问题

### Q1: Launch文件找不到？
确保Launch文件在正确的目录，并在setup.py中配置：
```python
data_files=[
    ('share/' + package_name + '/launch', 
     glob('launch/*.py')),
]
```

### Q2: 参数文件加载失败？
检查YAML文件格式和路径是否正确。

### Q3: 节点名冲突？
使用命名空间或设置不同的节点名。

---

## 最佳实践

1. **模块化** - 将大型系统分解为多个Launch文件
2. **参数化** - 使用Launch参数提高灵活性
3. **文档化** - 为Launch参数添加描述
4. **命名规范** - 使用清晰的命名空间和节点名
5. **错误处理** - 配置节点重启策略
6. **版本控制** - 将配置文件纳入版本控制

---

## Launch vs 直接运行

| 方式 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| 直接运行 | 简单快速 | 难以管理多节点 | 单节点测试 |
| Launch文件 | 统一管理、可配置 | 需要编写文件 | 生产环境 |

---

## 下一步

完成所有练习后，进入 `05_tf2/` 学习坐标变换系统。
