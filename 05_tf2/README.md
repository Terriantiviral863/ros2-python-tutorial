# 第五阶段：TF2坐标变换系统

## 学习目标

- 理解TF2坐标变换系统
- 学习发布和监听坐标变换
- 掌握静态和动态变换
- 理解坐标系树结构
- 学习时间旅行和变换查询

---

## 目录结构

```
05_tf2/
├── README.md                           # 本文件
├── static_tf_publisher.py              # 静态变换发布者
├── dynamic_tf_publisher.py             # 动态变换发布者
├── tf_listener.py                      # 变换监听器
├── tf_broadcaster.py                   # 变换广播器
├── frame_listener.py                   # 坐标系监听器
├── turtle_tf_broadcaster.py            # 海龟TF广播器
├── turtle_tf_listener.py               # 海龟TF监听器
└── robot_tf_tree.py                    # 机器人TF树示例
```

---

## TF2基础概念

### 什么是TF2？

TF2是ROS2的坐标变换系统，用于：
- 管理多个坐标系之间的关系
- 自动计算坐标系之间的变换
- 处理时间相关的变换
- 构建机器人的坐标系树

### 坐标系树结构

```
map (世界坐标系)
 └── odom (里程计坐标系)
      └── base_link (机器人基座)
           ├── base_laser (激光雷达)
           ├── camera_link (相机)
           └── imu_link (IMU)
```

### 关键概念

1. **Frame (坐标系)**: 参考坐标系
2. **Transform (变换)**: 两个坐标系之间的位置和姿态关系
3. **Static Transform**: 不随时间变化的变换
4. **Dynamic Transform**: 随时间变化的变换
5. **TF Tree**: 所有坐标系组成的树状结构

---

## 练习列表

### 练习1：静态变换发布
**文件**: `static_tf_publisher.py`
**目标**: 发布静态坐标变换

**运行**:
```bash
python3 05_tf2/static_tf_publisher.py
```

**验证**:
```bash
# 查看TF树
ros2 run tf2_tools view_frames

# 查看变换
ros2 run tf2_ros tf2_echo base_link camera_link
```

**说明**:
- 发布传感器相对于机器人基座的固定变换
- 使用StaticTransformBroadcaster
- 理解静态变换的应用场景

---

### 练习2：动态变换发布
**文件**: `dynamic_tf_publisher.py`
**目标**: 发布随时间变化的变换

**运行**:
```bash
python3 05_tf2/dynamic_tf_publisher.py
```

**验证**:
```bash
ros2 run tf2_ros tf2_echo world robot_base
```

**说明**:
- 发布机器人在世界坐标系中的位置
- 使用TransformBroadcaster
- 模拟机器人运动

---

### 练习3：变换监听
**文件**: `tf_listener.py`
**目标**: 监听并使用坐标变换

**运行**:
```bash
# 先启动发布者
python3 05_tf2/dynamic_tf_publisher.py

# 再启动监听器
python3 05_tf2/tf_listener.py
```

**说明**:
- 使用TransformListener查询变换
- 处理变换异常
- 坐标点变换

---

### 练习4：TF广播器
**文件**: `tf_broadcaster.py`
**目标**: 创建完整的TF广播系统

**运行**:
```bash
python3 05_tf2/tf_broadcaster.py
```

**说明**:
- 发布多个坐标系
- 构建完整的TF树
- 实时更新变换

---

### 练习5：海龟TF示例
**文件**: `turtle_tf_broadcaster.py` 和 `turtle_tf_listener.py`
**目标**: 使用TF控制海龟跟随

**运行**:
```bash
# 终端1：启动turtlesim
ros2 run turtlesim turtlesim_node

# 终端2：启动广播器
python3 05_tf2/turtle_tf_broadcaster.py

# 终端3：启动监听器
python3 05_tf2/turtle_tf_listener.py

# 终端4：控制海龟1
ros2 run turtlesim turtle_teleop_key
```

**说明**:
- 广播海龟位置为TF
- 监听TF控制另一只海龟跟随
- 实际应用TF系统

---

### 练习6：机器人TF树
**文件**: `robot_tf_tree.py`
**目标**: 构建完整的机器人坐标系树

**运行**:
```bash
python3 05_tf2/robot_tf_tree.py
```

**验证**:
```bash
# 生成TF树PDF
ros2 run tf2_tools view_frames

# 查看frames.pdf
evince frames.pdf
```

**说明**:
- 发布机器人所有坐标系
- 包含传感器、执行器坐标系
- 理解完整的TF树结构

---

## TF2 API详解

### 1. 发布静态变换

```python
from tf2_ros import StaticTransformBroadcaster
from geometry_msgs.msg import TransformStamped
import rclpy
from rclpy.node import Node

class StaticTFPublisher(Node):
    def __init__(self):
        super().__init__('static_tf_publisher')
        self.tf_static_broadcaster = StaticTransformBroadcaster(self)
        
        # 创建变换
        static_transform = TransformStamped()
        static_transform.header.stamp = self.get_clock().now().to_msg()
        static_transform.header.frame_id = 'base_link'
        static_transform.child_frame_id = 'camera_link'
        
        # 设置平移
        static_transform.transform.translation.x = 0.1
        static_transform.transform.translation.y = 0.0
        static_transform.transform.translation.z = 0.2
        
        # 设置旋转（四元数）
        static_transform.transform.rotation.x = 0.0
        static_transform.transform.rotation.y = 0.0
        static_transform.transform.rotation.z = 0.0
        static_transform.transform.rotation.w = 1.0
        
        # 发布
        self.tf_static_broadcaster.sendTransform(static_transform)
```

### 2. 发布动态变换

```python
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped

class DynamicTFPublisher(Node):
    def __init__(self):
        super().__init__('dynamic_tf_publisher')
        self.tf_broadcaster = TransformBroadcaster(self)
        self.timer = self.create_timer(0.1, self.broadcast_timer_callback)
        
    def broadcast_timer_callback(self):
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'world'
        t.child_frame_id = 'robot'
        
        # 动态更新位置
        t.transform.translation.x = # 计算位置
        t.transform.translation.y = # 计算位置
        t.transform.translation.z = 0.0
        
        # 发布
        self.tf_broadcaster.sendTransform(t)
```

### 3. 监听变换

```python
from tf2_ros import TransformListener, Buffer
from tf2_ros import LookupException, ConnectivityException, ExtrapolationException

class TFListener(Node):
    def __init__(self):
        super().__init__('tf_listener')
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.timer = self.create_timer(1.0, self.on_timer)
        
    def on_timer(self):
        try:
            # 查询变换
            trans = self.tf_buffer.lookup_transform(
                'target_frame',
                'source_frame',
                rclpy.time.Time()  # 最新的变换
            )
            
            # 使用变换
            x = trans.transform.translation.x
            y = trans.transform.translation.y
            
        except (LookupException, ConnectivityException, ExtrapolationException) as e:
            self.get_logger().warn(f'TF查询失败: {e}')
```

### 4. 坐标点变换

```python
from tf2_ros import TransformException
from geometry_msgs.msg import PointStamped
import tf2_geometry_msgs

# 创建点
point_in_source = PointStamped()
point_in_source.header.frame_id = 'source_frame'
point_in_source.header.stamp = self.get_clock().now().to_msg()
point_in_source.point.x = 1.0
point_in_source.point.y = 2.0
point_in_source.point.z = 0.0

try:
    # 变换到目标坐标系
    point_in_target = self.tf_buffer.transform(
        point_in_source,
        'target_frame',
        timeout=rclpy.duration.Duration(seconds=1.0)
    )
except TransformException as ex:
    self.get_logger().error(f'变换失败: {ex}')
```

---

## 四元数与欧拉角

### 欧拉角转四元数

```python
from tf_transformations import quaternion_from_euler
import math

# 欧拉角 (roll, pitch, yaw) 单位：弧度
roll = 0.0
pitch = 0.0
yaw = math.pi / 4  # 45度

# 转换为四元数
q = quaternion_from_euler(roll, pitch, yaw)

# 使用四元数
transform.transform.rotation.x = q[0]
transform.transform.rotation.y = q[1]
transform.transform.rotation.z = q[2]
transform.transform.rotation.w = q[3]
```

### 四元数转欧拉角

```python
from tf_transformations import euler_from_quaternion

# 从变换中获取四元数
q = [
    transform.transform.rotation.x,
    transform.transform.rotation.y,
    transform.transform.rotation.z,
    transform.transform.rotation.w
]

# 转换为欧拉角
roll, pitch, yaw = euler_from_quaternion(q)
```

---

## 常用TF命令

### 1. 查看TF树

```bash
# 生成TF树图
ros2 run tf2_tools view_frames

# 实时查看TF树
ros2 run tf2_tools tf2_monitor
```

### 2. 查看变换

```bash
# 查看两个坐标系之间的变换
ros2 run tf2_ros tf2_echo <source_frame> <target_frame>

# 示例
ros2 run tf2_ros tf2_echo base_link camera_link
```

### 3. 发布静态变换（命令行）

```bash
ros2 run tf2_ros static_transform_publisher x y z yaw pitch roll frame_id child_frame_id

# 示例：相机相对于base_link的位置
ros2 run tf2_ros static_transform_publisher 0.1 0 0.2 0 0 0 base_link camera_link
```

---

## 实践任务

### 任务1：传感器标定
1. 创建机器人基座坐标系
2. 发布激光雷达的静态变换
3. 发布相机的静态变换
4. 验证TF树结构

### 任务2：移动机器人TF
1. 发布odom到base_link的动态变换
2. 模拟机器人运动
3. 监听并记录机器人轨迹

### 任务3：多机器人系统
1. 为每个机器人创建独立的TF树
2. 使用命名空间隔离
3. 实现机器人间的相对定位

---

## 调试技巧

### 1. 检查TF树完整性

```bash
# 查看所有坐标系
ros2 run tf2_ros tf2_monitor

# 检查是否有断开的坐标系
ros2 run tf2_tools view_frames
```

### 2. 时间同步问题

```python
# 使用最新的变换
trans = self.tf_buffer.lookup_transform(
    target_frame,
    source_frame,
    rclpy.time.Time()  # 使用Time()获取最新
)

# 使用特定时间的变换
trans = self.tf_buffer.lookup_transform(
    target_frame,
    source_frame,
    specific_time,
    timeout=rclpy.duration.Duration(seconds=1.0)
)
```

### 3. 常见错误处理

```python
from tf2_ros import LookupException, ConnectivityException, ExtrapolationException

try:
    trans = self.tf_buffer.lookup_transform(...)
except LookupException:
    # 坐标系不存在
    self.get_logger().error('坐标系不存在')
except ConnectivityException:
    # TF树不连通
    self.get_logger().error('TF树断开')
except ExtrapolationException:
    # 时间超出范围
    self.get_logger().error('时间查询超出范围')
```

---

## 常见问题

### Q1: TF查询失败？
- 检查坐标系名称是否正确
- 确认TF已经发布
- 使用`tf2_echo`验证变换

### Q2: 时间戳问题？
- 使用`self.get_clock().now().to_msg()`获取当前时间
- 确保时间戳一致性

### Q3: TF树断开？
- 检查所有变换是否持续发布
- 确认父子坐标系关系正确
- 不能有循环依赖

---

## 最佳实践

1. **命名规范**
   - 使用小写和下划线
   - 清晰描述坐标系用途
   - 避免特殊字符

2. **静态vs动态**
   - 固定关系使用静态变换
   - 运动关系使用动态变换
   - 静态变换只需发布一次

3. **时间处理**
   - 使用正确的时间戳
   - 处理时间查询异常
   - 考虑网络延迟

4. **性能优化**
   - 避免高频发布静态变换
   - 合理设置查询超时
   - 缓存常用变换

---

## 下一步

完成所有练习后，进入 `06_robot_modeling/` 学习机器人建模。
