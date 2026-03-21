# 第八阶段：可视化工具

## 学习目标

- 掌握RViz2可视化工具
- 学习Marker可视化
- 理解点云可视化
- 学习图像显示
- 掌握自定义可视化

---

## 目录结构

```
08_visualization/
├── README.md                           # 本文件
├── rviz_marker_publisher.py            # Marker发布器
├── point_cloud_publisher.py            # 点云发布器
├── image_publisher.py                  # 图像发布器
├── interactive_marker.py               # 交互式Marker
├── path_visualizer.py                  # 路径可视化
├── grid_map_visualizer.py              # 栅格地图可视化
└── config/
    └── default.rviz                    # RViz配置文件
```

---

## RViz2基础

### 启动RViz2

```bash
# 基本启动
rviz2

# 加载配置文件
rviz2 -d config/default.rviz
```

### 常用显示类型

- **RobotModel** - 机器人模型
- **TF** - 坐标变换
- **LaserScan** - 激光扫描
- **PointCloud2** - 点云
- **Image** - 图像
- **Marker** - 标记
- **Path** - 路径
- **Map** - 地图

---

## Marker可视化

### Marker类型

```python
from visualization_msgs.msg import Marker

# 基本形状
Marker.ARROW = 0
Marker.CUBE = 1
Marker.SPHERE = 2
Marker.CYLINDER = 3
Marker.LINE_STRIP = 4
Marker.LINE_LIST = 5
Marker.CUBE_LIST = 6
Marker.SPHERE_LIST = 7
Marker.POINTS = 8
Marker.TEXT_VIEW_FACING = 9
Marker.MESH_RESOURCE = 10
Marker.TRIANGLE_LIST = 11
```

### 基本用法

```python
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point

marker = Marker()
marker.header.frame_id = "base_link"
marker.header.stamp = self.get_clock().now().to_msg()
marker.ns = "basic_shapes"
marker.id = 0
marker.type = Marker.SPHERE
marker.action = Marker.ADD

# 位置和姿态
marker.pose.position.x = 1.0
marker.pose.position.y = 0.0
marker.pose.position.z = 0.0
marker.pose.orientation.w = 1.0

# 尺寸
marker.scale.x = 0.5
marker.scale.y = 0.5
marker.scale.z = 0.5

# 颜色 (RGBA)
marker.color.r = 1.0
marker.color.g = 0.0
marker.color.b = 0.0
marker.color.a = 1.0

# 生命周期
marker.lifetime = rclpy.duration.Duration(seconds=0).to_msg()  # 永久

publisher.publish(marker)
```

---

## 点云可视化

### PointCloud2消息

```python
from sensor_msgs.msg import PointCloud2, PointField
from sensor_msgs_py import point_cloud2
import numpy as np

# 创建点云数据
points = np.random.rand(100, 3) * 10.0  # 100个随机点

# 创建PointCloud2消息
header = Header()
header.frame_id = "base_link"
header.stamp = self.get_clock().now().to_msg()

fields = [
    PointField(name='x', offset=0, datatype=PointField.FLOAT32, count=1),
    PointField(name='y', offset=4, datatype=PointField.FLOAT32, count=1),
    PointField(name='z', offset=8, datatype=PointField.FLOAT32, count=1),
]

cloud_msg = point_cloud2.create_cloud(header, fields, points)
publisher.publish(cloud_msg)
```

---

## 图像可视化

### 发布图像

```python
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np

bridge = CvBridge()

# 创建图像
img = np.zeros((480, 640, 3), dtype=np.uint8)
cv2.circle(img, (320, 240), 50, (0, 255, 0), -1)

# 转换为ROS消息
msg = bridge.cv2_to_imgmsg(img, encoding="bgr8")
msg.header.stamp = self.get_clock().now().to_msg()
msg.header.frame_id = "camera_link"

publisher.publish(msg)
```

---

## 路径可视化

```python
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped

path = Path()
path.header.frame_id = "map"
path.header.stamp = self.get_clock().now().to_msg()

# 添加路径点
for i in range(100):
    pose = PoseStamped()
    pose.header.frame_id = "map"
    pose.pose.position.x = i * 0.1
    pose.pose.position.y = math.sin(i * 0.1)
    pose.pose.orientation.w = 1.0
    path.poses.append(pose)

publisher.publish(path)
```

---

## 练习列表

### 练习1：Marker发布器
**文件**: `rviz_marker_publisher.py`
**目标**: 发布各种类型的Marker

**运行**:
```bash
python3 08_visualization/rviz_marker_publisher.py
rviz2
```

### 练习2：点云可视化
**文件**: `point_cloud_publisher.py`
**目标**: 生成和可视化点云

**运行**:
```bash
python3 08_visualization/point_cloud_publisher.py
rviz2
```

### 练习3：图像发布
**文件**: `image_publisher.py`
**目标**: 发布图像数据

**运行**:
```bash
python3 08_visualization/image_publisher.py
rviz2
```

### 练习4：交互式Marker
**文件**: `interactive_marker.py`
**目标**: 创建可交互的Marker

### 练习5：路径可视化
**文件**: `path_visualizer.py`
**目标**: 可视化机器人路径

### 练习6：栅格地图
**文件**: `grid_map_visualizer.py`
**目标**: 显示占用栅格地图

---

## RViz配置

### 保存配置

1. 在RViz中配置好所有显示
2. File -> Save Config As
3. 保存为 `.rviz` 文件

### 加载配置

```bash
rviz2 -d config/default.rviz
```

---

## 常用技巧

### 1. 多个Marker

```python
from visualization_msgs.msg import MarkerArray

marker_array = MarkerArray()
for i in range(10):
    marker = Marker()
    marker.id = i
    # 配置marker...
    marker_array.markers.append(marker)

publisher.publish(marker_array)
```

### 2. 删除Marker

```python
marker = Marker()
marker.action = Marker.DELETE
marker.id = marker_id_to_delete
publisher.publish(marker)
```

### 3. 文本标签

```python
marker = Marker()
marker.type = Marker.TEXT_VIEW_FACING
marker.text = "Hello ROS2"
marker.scale.z = 0.2  # 文字高度
```

---

## 实践任务

### 任务1：机器人轨迹可视化
1. 记录机器人位置
2. 用LINE_STRIP显示轨迹
3. 用箭头显示方向

### 任务2：传感器数据可视化
1. 模拟激光雷达数据
2. 用点云显示
3. 添加颜色编码

### 任务3：交互式控制
1. 创建交互式Marker
2. 拖动Marker控制机器人
3. 实时更新位置

---

## 调试技巧

### 检查话题

```bash
# 查看Marker话题
ros2 topic echo /visualization_marker

# 查看点云话题
ros2 topic echo /point_cloud
```

### 常见问题

**Q: Marker不显示？**
- 检查frame_id是否正确
- 确认Fixed Frame设置
- 检查颜色alpha值

**Q: 点云不显示？**
- 确认PointCloud2格式正确
- 检查点的数量
- 验证坐标范围

---

## 下一步

完成所有练习后，进入 `09_sensors/` 学习传感器集成。
