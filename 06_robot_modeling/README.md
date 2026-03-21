# 第六阶段：机器人建模

## 学习目标

- 理解URDF机器人描述格式
- 学习创建机器人模型
- 掌握关节和连杆定义
- 理解Xacro宏语言
- 学习在RViz中可视化机器人

---

## 目录结构

```
06_robot_modeling/
├── README.md                           # 本文件
├── urdf/                               # URDF文件目录
│   ├── simple_robot.urdf              # 简单机器人模型
│   ├── mobile_robot.urdf              # 移动机器人模型
│   └── sensor_robot.urdf              # 带传感器的机器人
├── xacro/                              # Xacro文件目录
│   ├── robot.xacro                    # 主机器人文件
│   ├── robot_base.xacro               # 基座定义
│   ├── robot_sensors.xacro            # 传感器定义
│   └── materials.xacro                # 材质定义
├── meshes/                             # 网格文件目录
├── config/                             # 配置文件
│   └── robot_description.yaml
├── display_robot.py                    # 显示机器人模型
├── state_publisher.py                  # 状态发布器
└── joint_controller.py                 # 关节控制器
```

---

## URDF基础

### 什么是URDF？

URDF (Unified Robot Description Format) 是ROS中描述机器人模型的XML格式文件。

**主要元素**:
- **link**: 连杆（刚体部件）
- **joint**: 关节（连接两个连杆）
- **robot**: 根元素

### 基本结构

```xml
<?xml version="1.0"?>
<robot name="my_robot">
  <!-- 定义连杆 -->
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.6 0.4 0.2"/>
      </geometry>
      <material name="blue">
        <color rgba="0 0 0.8 1"/>
      </material>
    </visual>
  </link>
  
  <!-- 定义关节 -->
  <joint name="base_to_wheel" type="continuous">
    <parent link="base_link"/>
    <child link="wheel_link"/>
    <origin xyz="0 0.2 0" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
  </joint>
  
  <link name="wheel_link">
    <visual>
      <geometry>
        <cylinder radius="0.1" length="0.05"/>
      </geometry>
    </visual>
  </link>
</robot>
```

---

## 练习列表

### 练习1：简单机器人模型
**文件**: `urdf/simple_robot.urdf`
**目标**: 创建第一个URDF模型

**运行**:
```bash
# 检查URDF语法
check_urdf urdf/simple_robot.urdf

# 查看模型树结构
urdf_to_graphiz urdf/simple_robot.urdf

# 在RViz中显示
python3 06_robot_modeling/display_robot.py
```

**说明**:
- 定义基本连杆和关节
- 理解坐标系和变换
- 添加可视化几何体

---

### 练习2：移动机器人
**文件**: `urdf/mobile_robot.urdf`
**目标**: 创建差分驱动移动机器人

**运行**:
```bash
python3 06_robot_modeling/display_robot.py --urdf urdf/mobile_robot.urdf
```

**说明**:
- 添加轮子和万向轮
- 定义连续关节
- 设置碰撞和惯性属性

---

### 练习3：传感器集成
**文件**: `urdf/sensor_robot.urdf`
**目标**: 在机器人上添加传感器

**运行**:
```bash
python3 06_robot_modeling/display_robot.py --urdf urdf/sensor_robot.urdf
```

**说明**:
- 添加激光雷达
- 添加相机
- 添加IMU
- 正确设置传感器坐标系

---

### 练习4：Xacro宏语言
**文件**: `xacro/robot.xacro`
**目标**: 使用Xacro简化URDF

**运行**:
```bash
# 转换Xacro为URDF
ros2 run xacro xacro xacro/robot.xacro > /tmp/robot.urdf

# 显示
python3 06_robot_modeling/display_robot.py --urdf /tmp/robot.urdf
```

**说明**:
- 使用宏定义重复结构
- 参数化模型
- 模块化设计

---

### 练习5：状态发布
**文件**: `state_publisher.py`
**目标**: 发布机器人状态

**运行**:
```bash
python3 06_robot_modeling/state_publisher.py
```

**说明**:
- 使用robot_state_publisher
- 发布TF变换
- 在RViz中实时显示

---

### 练习6：关节控制
**文件**: `joint_controller.py`
**目标**: 控制机器人关节

**运行**:
```bash
python3 06_robot_modeling/joint_controller.py
```

**说明**:
- 发布关节状态
- 使用joint_state_publisher
- 交互式控制关节

---

## URDF元素详解

### 1. Link（连杆）

```xml
<link name="base_link">
  <!-- 可视化 -->
  <visual>
    <origin xyz="0 0 0" rpy="0 0 0"/>
    <geometry>
      <box size="0.6 0.4 0.2"/>
      <!-- 或 -->
      <cylinder radius="0.1" length="0.5"/>
      <!-- 或 -->
      <sphere radius="0.1"/>
      <!-- 或 -->
      <mesh filename="package://pkg/meshes/model.stl" scale="1 1 1"/>
    </geometry>
    <material name="blue">
      <color rgba="0 0 0.8 1"/>
    </material>
  </visual>
  
  <!-- 碰撞 -->
  <collision>
    <origin xyz="0 0 0" rpy="0 0 0"/>
    <geometry>
      <box size="0.6 0.4 0.2"/>
    </geometry>
  </collision>
  
  <!-- 惯性 -->
  <inertial>
    <origin xyz="0 0 0" rpy="0 0 0"/>
    <mass value="10.0"/>
    <inertia ixx="1.0" ixy="0.0" ixz="0.0"
             iyy="1.0" iyz="0.0"
             izz="1.0"/>
  </inertial>
</link>
```

### 2. Joint（关节）

```xml
<!-- 固定关节 -->
<joint name="base_to_sensor" type="fixed">
  <parent link="base_link"/>
  <child link="sensor_link"/>
  <origin xyz="0.1 0 0.2" rpy="0 0 0"/>
</joint>

<!-- 旋转关节 -->
<joint name="base_to_arm" type="revolute">
  <parent link="base_link"/>
  <child link="arm_link"/>
  <origin xyz="0 0 0.1" rpy="0 0 0"/>
  <axis xyz="0 0 1"/>
  <limit lower="-1.57" upper="1.57" effort="10" velocity="1.0"/>
</joint>

<!-- 连续关节（轮子） -->
<joint name="base_to_wheel" type="continuous">
  <parent link="base_link"/>
  <child link="wheel_link"/>
  <origin xyz="0 0.15 0" rpy="0 0 0"/>
  <axis xyz="0 1 0"/>
</joint>

<!-- 平移关节 -->
<joint name="prismatic_joint" type="prismatic">
  <parent link="base_link"/>
  <child link="slider_link"/>
  <origin xyz="0 0 0" rpy="0 0 0"/>
  <axis xyz="0 0 1"/>
  <limit lower="0" upper="0.5" effort="100" velocity="0.5"/>
</joint>
```

### 关节类型

| 类型 | 说明 | 自由度 | 应用 |
|------|------|--------|------|
| fixed | 固定 | 0 | 传感器安装 |
| revolute | 旋转（有限） | 1 | 机械臂关节 |
| continuous | 连续旋转 | 1 | 轮子 |
| prismatic | 平移 | 1 | 升降机构 |
| floating | 浮动 | 6 | 移动机器人基座 |
| planar | 平面 | 2 | 特殊应用 |

---

## Xacro宏语言

### 基本语法

```xml
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="my_robot">
  
  <!-- 定义属性 -->
  <xacro:property name="wheel_radius" value="0.1"/>
  <xacro:property name="wheel_width" value="0.05"/>
  
  <!-- 定义宏 -->
  <xacro:macro name="wheel" params="prefix reflect">
    <link name="${prefix}_wheel">
      <visual>
        <geometry>
          <cylinder radius="${wheel_radius}" length="${wheel_width}"/>
        </geometry>
      </visual>
    </link>
    
    <joint name="base_to_${prefix}_wheel" type="continuous">
      <parent link="base_link"/>
      <child link="${prefix}_wheel"/>
      <origin xyz="0 ${reflect*0.2} 0" rpy="0 0 0"/>
      <axis xyz="0 1 0"/>
    </joint>
  </xacro:macro>
  
  <!-- 使用宏 -->
  <xacro:wheel prefix="left" reflect="1"/>
  <xacro:wheel prefix="right" reflect="-1"/>
  
  <!-- 包含其他文件 -->
  <xacro:include filename="$(find package_name)/urdf/common.xacro"/>
  
</robot>
```

### 常用技巧

```xml
<!-- 数学运算 -->
<xacro:property name="half_width" value="${width/2}"/>

<!-- 条件语句 -->
<xacro:if value="${use_sensor}">
  <link name="sensor_link"/>
</xacro:if>

<!-- 循环（需要Python脚本） -->
<xacro:macro name="create_links" params="count">
  <xacro:property name="i" value="0"/>
  <xacro:while value="${i &lt; count}">
    <link name="link_${i}"/>
    <xacro:property name="i" value="${i+1}"/>
  </xacro:while>
</xacro:macro>
```

---

## 在RViz中可视化

### 配置RViz

```python
# display_robot.py 示例
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Header

class RobotDisplay(Node):
    def __init__(self):
        super().__init__('robot_display')
        
        # 发布关节状态
        self.joint_pub = self.create_publisher(
            JointState, 
            'joint_states', 
            10
        )
        
        self.timer = self.create_timer(0.1, self.timer_callback)
        
    def timer_callback(self):
        msg = JointState()
        msg.header = Header()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = ['joint1', 'joint2']
        msg.position = [0.0, 0.0]
        msg.velocity = []
        msg.effort = []
        
        self.joint_pub.publish(msg)
```

### RViz配置

1. 添加 **RobotModel** 显示
2. 添加 **TF** 显示
3. 设置 Fixed Frame 为 `base_link`
4. 调整视角和颜色

---

## 实践任务

### 任务1：创建两轮差分机器人
1. 定义机器人基座
2. 添加两个驱动轮
3. 添加一个万向轮
4. 设置正确的惯性参数

### 任务2：添加机械臂
1. 创建3自由度机械臂
2. 定义旋转关节
3. 设置关节限位
4. 在RViz中控制

### 任务3：完整移动机器人
1. 结合移动底盘和传感器
2. 使用Xacro模块化设计
3. 添加激光雷达和相机
4. 配置正确的TF树

---

## 常用工具

### 1. 检查URDF

```bash
# 检查语法
check_urdf my_robot.urdf

# 查看模型树
urdf_to_graphiz my_robot.urdf
```

### 2. Xacro转换

```bash
# 转换为URDF
ros2 run xacro xacro robot.xacro > robot.urdf

# 带参数转换
ros2 run xacro xacro robot.xacro use_sensor:=true > robot.urdf
```

### 3. 可视化

```bash
# 启动RViz
rviz2

# 使用joint_state_publisher_gui
ros2 run joint_state_publisher_gui joint_state_publisher_gui
```

---

## 惯性参数计算

### 常见几何体惯性

**长方体** (质量m, 尺寸x,y,z):
```
ixx = m/12 * (y² + z²)
iyy = m/12 * (x² + z²)
izz = m/12 * (x² + y²)
```

**圆柱体** (质量m, 半径r, 高度h):
```
ixx = iyy = m/12 * (3r² + h²)
izz = m/2 * r²
```

**球体** (质量m, 半径r):
```
ixx = iyy = izz = 2/5 * m * r²
```

---

## 调试技巧

### 1. 检查TF树

```bash
# 查看TF树
ros2 run tf2_tools view_frames

# 检查特定变换
ros2 run tf2_ros tf2_echo base_link sensor_link
```

### 2. 验证关节

```bash
# 查看关节状态
ros2 topic echo /joint_states

# 发布测试关节状态
ros2 topic pub /joint_states sensor_msgs/msg/JointState ...
```

### 3. 常见错误

- **TF树断开**: 检查所有关节连接
- **模型不显示**: 检查Fixed Frame设置
- **关节不动**: 确认joint_state_publisher运行

---

## 常见问题

### Q1: URDF文件找不到？
确保使用正确的package路径：
```xml
<mesh filename="package://my_package/meshes/model.stl"/>
```

### Q2: 模型在RViz中倒置？
检查坐标系定义，ROS使用右手坐标系（Z轴向上）。

### Q3: 关节限位不起作用？
在Gazebo仿真中才会生效，RViz只是可视化。

---

## 最佳实践

1. **命名规范**
   - 使用描述性名称
   - 保持一致的命名风格
   - 避免特殊字符

2. **坐标系**
   - 遵循REP-103标准
   - X向前，Y向左，Z向上
   - 使用右手坐标系

3. **模块化**
   - 使用Xacro分离组件
   - 参数化尺寸和属性
   - 便于维护和复用

4. **性能**
   - 简化碰撞几何体
   - 使用低多边形网格
   - 合理设置更新频率

5. **文档**
   - 注释关键参数
   - 说明坐标系定义
   - 记录修改历史

---

## 参考资源

- [URDF官方教程](http://wiki.ros.org/urdf/Tutorials)
- [Xacro文档](http://wiki.ros.org/xacro)
- [REP-103坐标系标准](https://www.ros.org/reps/rep-0103.html)
- [URDF在线验证器](https://mymodelrobot.appspot.com/)

---

## 下一步

完成所有练习后，进入 `07_tools/` 学习ROS2开发工具。
