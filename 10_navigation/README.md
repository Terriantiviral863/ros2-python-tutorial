# 第十阶段：导航系统

## 学习目标

- 理解ROS2导航框架
- 学习路径规划算法
- 掌握定位技术
- 理解避障策略
- 学习导航参数调优

---

## 目录结构

```
10_navigation/
├── README.md                           # 本文件
├── simple_navigator.py                 # 简单导航器
├── goal_sender.py                      # 目标点发送器
├── path_planner.py                     # 路径规划器
├── obstacle_avoider.py                 # 避障控制器
├── localization_demo.py                # 定位演示
├── map_builder.py                      # 地图构建
├── waypoint_follower.py                # 航点跟随器
└── config/
    └── navigation_params.yaml          # 导航参数
```

---

## 导航系统概述

### Nav2架构

ROS2导航系统（Nav2）包含以下核心组件：

1. **地图服务器** - 提供静态地图
2. **定位** - AMCL或其他定位算法
3. **全局规划器** - 计算全局路径
4. **局部规划器** - 实时避障和路径跟踪
5. **恢复行为** - 处理异常情况
6. **行为树** - 协调导航任务

### 坐标系

```
map -> odom -> base_link -> sensors
```

- **map**: 全局固定坐标系
- **odom**: 里程计坐标系（连续但有漂移）
- **base_link**: 机器人基座坐标系

---

## 基本导航流程

### 1. 发送导航目标

```python
from geometry_msgs.msg import PoseStamped

goal = PoseStamped()
goal.header.frame_id = "map"
goal.header.stamp = self.get_clock().now().to_msg()
goal.pose.position.x = 2.0
goal.pose.position.y = 1.0
goal.pose.orientation.w = 1.0

# 发送到导航系统
self.goal_pub.publish(goal)
```

### 2. 路径规划

```python
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped

def plan_path(self, start, goal):
    path = Path()
    path.header.frame_id = "map"
    path.header.stamp = self.get_clock().now().to_msg()
    
    # A*算法或其他规划算法
    waypoints = self.a_star(start, goal)
    
    for wp in waypoints:
        pose = PoseStamped()
        pose.header.frame_id = "map"
        pose.pose.position.x = wp[0]
        pose.pose.position.y = wp[1]
        pose.pose.orientation.w = 1.0
        path.poses.append(pose)
    
    return path
```

### 3. 路径跟踪

```python
from geometry_msgs.msg import Twist

def follow_path(self, path, current_pose):
    # 找到最近的路径点
    target = self.find_nearest_point(path, current_pose)
    
    # 计算控制命令
    cmd = Twist()
    
    # 计算到目标的距离和角度
    dx = target.x - current_pose.x
    dy = target.y - current_pose.y
    distance = math.sqrt(dx**2 + dy**2)
    target_angle = math.atan2(dy, dx)
    angle_diff = target_angle - current_pose.theta
    
    # 控制律
    cmd.linear.x = min(0.5, distance * 0.5)
    cmd.angular.z = angle_diff * 1.0
    
    return cmd
```

---

## 路径规划算法

### A*算法

```python
import heapq

def a_star(self, start, goal, grid):
    open_set = []
    heapq.heappush(open_set, (0, start))
    
    came_from = {}
    g_score = {start: 0}
    f_score = {start: self.heuristic(start, goal)}
    
    while open_set:
        current = heapq.heappop(open_set)[1]
        
        if current == goal:
            return self.reconstruct_path(came_from, current)
        
        for neighbor in self.get_neighbors(current, grid):
            tentative_g = g_score[current] + self.distance(current, neighbor)
            
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + self.heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
    
    return None

def heuristic(self, a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)
```

### DWA (动态窗口法)

```python
def dwa(self, current_state, goal, obstacles):
    # 动态窗口
    v_min, v_max = self.get_velocity_window(current_state)
    w_min, w_max = self.get_angular_window(current_state)
    
    best_v, best_w = 0, 0
    best_score = -float('inf')
    
    # 采样速度空间
    for v in np.linspace(v_min, v_max, 10):
        for w in np.linspace(w_min, w_max, 20):
            # 预测轨迹
            trajectory = self.predict_trajectory(current_state, v, w)
            
            # 评分
            if not self.check_collision(trajectory, obstacles):
                score = self.evaluate_trajectory(trajectory, goal)
                if score > best_score:
                    best_score = score
                    best_v, best_w = v, w
    
    return best_v, best_w
```

---

## 定位技术

### AMCL (自适应蒙特卡洛定位)

```python
class ParticleFilter:
    def __init__(self, num_particles=1000):
        self.particles = self.initialize_particles(num_particles)
        self.weights = np.ones(num_particles) / num_particles
    
    def predict(self, odom):
        # 运动模型
        for i in range(len(self.particles)):
            self.particles[i] = self.motion_model(
                self.particles[i], 
                odom
            )
    
    def update(self, scan, map):
        # 观测模型
        for i in range(len(self.particles)):
            self.weights[i] = self.sensor_model(
                self.particles[i],
                scan,
                map
            )
        
        # 归一化权重
        self.weights /= np.sum(self.weights)
        
        # 重采样
        if self.effective_sample_size() < len(self.particles) / 2:
            self.resample()
    
    def get_pose(self):
        # 加权平均
        return np.average(self.particles, weights=self.weights, axis=0)
```

---

## 避障策略

### 1. 基于激光雷达的避障

```python
def laser_obstacle_avoidance(self, scan):
    # 分区域检测
    left_min = min(scan.ranges[0:len(scan.ranges)//3])
    front_min = min(scan.ranges[len(scan.ranges)//3:2*len(scan.ranges)//3])
    right_min = min(scan.ranges[2*len(scan.ranges)//3:])
    
    cmd = Twist()
    
    if front_min < 0.5:
        # 前方有障碍，转向
        cmd.linear.x = 0.0
        if left_min > right_min:
            cmd.angular.z = 0.5  # 左转
        else:
            cmd.angular.z = -0.5  # 右转
    elif front_min < 1.0:
        # 减速
        cmd.linear.x = 0.1
    else:
        # 正常前进
        cmd.linear.x = 0.3
    
    return cmd
```

### 2. 人工势场法

```python
def artificial_potential_field(self, robot_pos, goal, obstacles):
    # 吸引力
    attractive_force = self.attractive_potential(robot_pos, goal)
    
    # 排斥力
    repulsive_force = np.zeros(2)
    for obs in obstacles:
        repulsive_force += self.repulsive_potential(robot_pos, obs)
    
    # 合力
    total_force = attractive_force + repulsive_force
    
    # 转换为速度命令
    cmd = Twist()
    cmd.linear.x = min(0.5, np.linalg.norm(total_force))
    cmd.angular.z = math.atan2(total_force[1], total_force[0])
    
    return cmd

def attractive_potential(self, pos, goal):
    k_att = 1.0
    return k_att * (goal - pos)

def repulsive_potential(self, pos, obstacle):
    k_rep = 2.0
    d0 = 1.0  # 影响距离
    
    diff = pos - obstacle
    distance = np.linalg.norm(diff)
    
    if distance > d0:
        return np.zeros(2)
    
    return k_rep * (1.0/distance - 1.0/d0) * (1.0/distance**2) * (diff/distance)
```

---

## 练习列表

### 练习1：简单导航器
**文件**: `simple_navigator.py`
**目标**: 实现基本的点到点导航

**运行**:
```bash
python3 10_navigation/simple_navigator.py
```

### 练习2：目标点发送器
**文件**: `goal_sender.py`
**目标**: 发送导航目标点

### 练习3：路径规划器
**文件**: `path_planner.py`
**目标**: 实现A*路径规划

### 练习4：避障控制器
**文件**: `obstacle_avoider.py`
**目标**: 基于激光雷达的避障

### 练习5：定位演示
**文件**: `localization_demo.py`
**目标**: 粒子滤波定位

### 练习6：地图构建
**文件**: `map_builder.py`
**目标**: 构建占用栅格地图

### 练习7：航点跟随
**文件**: `waypoint_follower.py`
**目标**: 跟随一系列航点

---

## 实践任务

### 任务1：自主导航
1. 加载地图
2. 设置目标点
3. 规划路径
4. 执行导航
5. 避开障碍物

### 任务2：巡逻机器人
1. 定义巡逻路径
2. 循环访问航点
3. 处理异常情况
4. 记录巡逻日志

### 任务3：跟随目标
1. 检测目标
2. 计算相对位置
3. 保持安全距离
4. 实时跟随

---

## 调试技巧

### 1. 可视化路径

```bash
# 在RViz中添加Path显示
ros2 topic echo /plan
```

### 2. 检查TF树

```bash
ros2 run tf2_tools view_frames
```

### 3. 监控速度命令

```bash
ros2 topic echo /cmd_vel
```

---

## 常见问题

### Q1: 机器人不动？
- 检查速度命令是否发布
- 验证TF树完整性
- 确认目标点可达

### Q2: 路径规划失败？
- 检查地图是否正确
- 验证起点和终点在自由空间
- 调整规划器参数

### Q3: 定位不准？
- 增加粒子数量
- 调整传感器模型
- 检查地图匹配度

---

## 性能优化

### 1. 路径平滑

```python
def smooth_path(self, path, weight_data=0.5, weight_smooth=0.1):
    new_path = path.copy()
    tolerance = 0.000001
    change = tolerance
    
    while change >= tolerance:
        change = 0.0
        for i in range(1, len(path) - 1):
            for j in range(len(path[0])):
                aux = new_path[i][j]
                new_path[i][j] += weight_data * (path[i][j] - new_path[i][j])
                new_path[i][j] += weight_smooth * (
                    new_path[i-1][j] + new_path[i+1][j] - 2.0 * new_path[i][j]
                )
                change += abs(aux - new_path[i][j])
    
    return new_path
```

### 2. 降低计算频率

```python
# 降低规划频率
self.plan_timer = self.create_timer(1.0, self.plan_callback)

# 提高控制频率
self.control_timer = self.create_timer(0.05, self.control_callback)
```

---

## 下一步

完成所有练习后，进入 `11_final_project/` 完成综合项目。
