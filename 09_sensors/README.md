# 第九阶段：传感器集成

## 学习目标

- 理解常见机器人传感器
- 学习激光雷达数据处理
- 掌握相机图像处理
- 理解IMU数据融合
- 学习传感器标定

---

## 目录结构

```
09_sensors/
├── README.md                           # 本文件
├── laser_scan_simulator.py             # 激光雷达模拟器
├── laser_scan_processor.py             # 激光数据处理
├── camera_simulator.py                 # 相机模拟器
├── image_processor.py                  # 图像处理
├── imu_simulator.py                    # IMU模拟器
├── imu_processor.py                    # IMU数据处理
├── sensor_fusion.py                    # 传感器融合
└── obstacle_detector.py                # 障碍物检测
```

---

## 常见传感器类型

### 1. 激光雷达 (LiDAR)

**消息类型**: `sensor_msgs/LaserScan`

```python
from sensor_msgs.msg import LaserScan

scan = LaserScan()
scan.header.frame_id = "laser_link"
scan.angle_min = -3.14159  # 起始角度
scan.angle_max = 3.14159   # 结束角度
scan.angle_increment = 0.0174533  # 角度增量
scan.range_min = 0.1       # 最小距离
scan.range_max = 10.0      # 最大距离
scan.ranges = [...]        # 距离数据
scan.intensities = [...]   # 强度数据
```

### 2. 相机 (Camera)

**消息类型**: `sensor_msgs/Image`

```python
from sensor_msgs.msg import Image

image = Image()
image.header.frame_id = "camera_link"
image.height = 480
image.width = 640
image.encoding = "bgr8"
image.step = 640 * 3
image.data = [...]  # 图像数据
```

### 3. IMU (惯性测量单元)

**消息类型**: `sensor_msgs/Imu`

```python
from sensor_msgs.msg import Imu

imu = Imu()
imu.header.frame_id = "imu_link"
imu.orientation.x = 0.0
imu.orientation.y = 0.0
imu.orientation.z = 0.0
imu.orientation.w = 1.0
imu.angular_velocity.x = 0.0
imu.angular_velocity.y = 0.0
imu.angular_velocity.z = 0.0
imu.linear_acceleration.x = 0.0
imu.linear_acceleration.y = 0.0
imu.linear_acceleration.z = 9.81
```

### 4. 深度相机

**消息类型**: `sensor_msgs/PointCloud2`

### 5. GPS

**消息类型**: `sensor_msgs/NavSatFix`

---

## 激光雷达处理

### 基本操作

```python
def scan_callback(self, msg):
    # 获取距离数据
    ranges = msg.ranges
    
    # 遍历所有点
    for i, r in enumerate(ranges):
        if r < msg.range_min or r > msg.range_max:
            continue
        
        # 计算角度
        angle = msg.angle_min + i * msg.angle_increment
        
        # 转换为笛卡尔坐标
        x = r * math.cos(angle)
        y = r * math.sin(angle)
```

### 障碍物检测

```python
def detect_obstacles(self, scan):
    min_distance = float('inf')
    min_angle = 0.0
    
    for i, r in enumerate(scan.ranges):
        if scan.range_min < r < scan.range_max:
            if r < min_distance:
                min_distance = r
                min_angle = scan.angle_min + i * scan.angle_increment
    
    return min_distance, min_angle
```

---

## 图像处理

### 使用OpenCV

```python
import cv2
from cv_bridge import CvBridge

bridge = CvBridge()

def image_callback(self, msg):
    # ROS Image转OpenCV
    cv_image = bridge.imgmsg_to_cv2(msg, "bgr8")
    
    # 图像处理
    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    
    # 检测圆形
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20)
    
    # OpenCV转ROS Image
    processed_msg = bridge.cv2_to_imgmsg(edges, "mono8")
    self.publisher.publish(processed_msg)
```

### 特征检测

```python
# SIFT特征
sift = cv2.SIFT_create()
keypoints, descriptors = sift.detectAndCompute(gray, None)

# ORB特征
orb = cv2.ORB_create()
keypoints, descriptors = orb.detectAndCompute(gray, None)
```

---

## IMU数据处理

### 姿态解算

```python
from tf_transformations import euler_from_quaternion, quaternion_from_euler

def imu_callback(self, msg):
    # 四元数转欧拉角
    q = [
        msg.orientation.x,
        msg.orientation.y,
        msg.orientation.z,
        msg.orientation.w
    ]
    roll, pitch, yaw = euler_from_quaternion(q)
    
    # 角速度
    wx = msg.angular_velocity.x
    wy = msg.angular_velocity.y
    wz = msg.angular_velocity.z
    
    # 线加速度
    ax = msg.linear_acceleration.x
    ay = msg.linear_acceleration.y
    az = msg.linear_acceleration.z
```

### 互补滤波

```python
class ComplementaryFilter:
    def __init__(self, alpha=0.98):
        self.alpha = alpha
        self.angle = 0.0
    
    def update(self, gyro, accel, dt):
        # 陀螺仪积分
        gyro_angle = self.angle + gyro * dt
        
        # 加速度计角度
        accel_angle = math.atan2(accel[1], accel[2])
        
        # 互补滤波
        self.angle = self.alpha * gyro_angle + (1 - self.alpha) * accel_angle
        
        return self.angle
```

---

## 传感器融合

### 卡尔曼滤波

```python
import numpy as np

class KalmanFilter:
    def __init__(self):
        self.x = np.zeros((4, 1))  # 状态 [x, y, vx, vy]
        self.P = np.eye(4)         # 协方差
        self.F = np.eye(4)         # 状态转移
        self.H = np.eye(2, 4)      # 观测矩阵
        self.R = np.eye(2) * 0.1   # 观测噪声
        self.Q = np.eye(4) * 0.01  # 过程噪声
    
    def predict(self, dt):
        self.F[0, 2] = dt
        self.F[1, 3] = dt
        
        self.x = self.F @ self.x
        self.P = self.F @ self.P @ self.F.T + self.Q
    
    def update(self, z):
        y = z - self.H @ self.x
        S = self.H @ self.P @ self.H.T + self.R
        K = self.P @ self.H.T @ np.linalg.inv(S)
        
        self.x = self.x + K @ y
        self.P = (np.eye(4) - K @ self.H) @ self.P
```

---

## 练习列表

### 练习1：激光雷达模拟
**文件**: `laser_scan_simulator.py`
**目标**: 模拟激光雷达数据

**运行**:
```bash
python3 09_sensors/laser_scan_simulator.py
rviz2
```

### 练习2：激光数据处理
**文件**: `laser_scan_processor.py`
**目标**: 处理激光雷达数据

### 练习3：相机模拟
**文件**: `camera_simulator.py`
**目标**: 模拟相机图像

### 练习4：图像处理
**文件**: `image_processor.py`
**目标**: 处理图像数据

### 练习5：IMU模拟
**文件**: `imu_simulator.py`
**目标**: 模拟IMU数据

### 练习6：传感器融合
**文件**: `sensor_fusion.py`
**目标**: 融合多传感器数据

### 练习7：障碍物检测
**文件**: `obstacle_detector.py`
**目标**: 基于激光雷达检测障碍物

---

## 实践任务

### 任务1：激光雷达避障
1. 模拟激光雷达数据
2. 检测最近障碍物
3. 计算安全方向
4. 发布速度命令

### 任务2：视觉跟踪
1. 获取相机图像
2. 检测目标颜色
3. 计算目标位置
4. 控制机器人跟随

### 任务3：姿态估计
1. 融合IMU和里程计
2. 使用卡尔曼滤波
3. 发布姿态估计
4. 可视化结果

---

## 传感器标定

### 相机标定

```bash
# 使用camera_calibration包
ros2 run camera_calibration cameracalibrator \
  --size 8x6 \
  --square 0.108 \
  image:=/camera/image \
  camera:=/camera
```

### 激光雷达-相机标定

需要标定激光雷达和相机之间的外参。

---

## 常见问题

### Q1: 激光数据有噪声？
使用中值滤波或均值滤波平滑数据。

### Q2: 图像处理太慢？
- 降低图像分辨率
- 使用GPU加速
- 优化算法

### Q3: IMU漂移？
- 使用传感器融合
- 定期校准
- 使用更高精度IMU

---

## 性能优化

### 1. 降采样

```python
# 激光数据降采样
step = 5
ranges_downsampled = scan.ranges[::step]
```

### 2. ROI处理

```python
# 只处理图像感兴趣区域
roi = cv_image[100:300, 200:400]
```

### 3. 多线程

```python
from threading import Thread

def process_image(self, image):
    thread = Thread(target=self._process, args=(image,))
    thread.start()
```

---

## 下一步

完成所有练习后，进入 `10_navigation/` 学习导航系统。
