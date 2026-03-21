# 综合项目开发指南

## 项目概述

本项目是一个完整的自主移动机器人系统，整合了ROS2的所有核心功能。

---

## 快速开始

**注意**: 本项目的示例是独立的Python脚本，可以直接运行，不需要构建ROS2包。

### 1. 启动机器人主控制节点

```bash
cd /home/jetson/ddxd/11_final_project

# 启动主控制节点
python3 robot_system/robot_main.py
```

### 2. 启动传感器管理器（新终端）

```bash
cd /home/jetson/ddxd/11_final_project

# 启动传感器管理器
python3 robot_system/sensor_manager.py
```

### 3. 启动导航控制器（新终端）

```bash
cd /home/jetson/ddxd/11_final_project

# 启动导航控制器
python3 robot_system/navigation_controller.py
```

### 4. 使用用户界面发送命令（新终端）

```bash
cd /home/jetson/ddxd/11_final_project

# 启动交互式界面
python3 robot_system/ui_interface.py
```

### 5. 或者直接执行任务

```bash
cd /home/jetson/ddxd/11_final_project

# 执行巡逻任务
python3 robot_system/task_executor.py patrol

# 前往指定位置
python3 robot_system/task_executor.py goto 2.0 1.5

# 停止任务
python3 robot_system/task_executor.py stop
```

---

## 系统架构

### 节点图

```
robot_main (主控制)
    ├── sensor_manager (传感器管理)
    │   ├── /scan (激光雷达)
    │   ├── /camera/image (相机)
    │   └── /imu/data (IMU)
    │
    ├── navigation_controller (导航控制)
    │   ├── /goal_pose (目标)
    │   ├── /cmd_vel (速度命令)
    │   └── /planned_path (规划路径)
    │
    └── task_executor (任务执行)
        ├── /task_command (任务命令)
        └── /task_status (任务状态)
```

### 数据流

```
传感器数据 -> 数据融合 -> 定位 -> 路径规划 -> 运动控制 -> 执行器
     ↓            ↓         ↓         ↓           ↓
  可视化      障碍物检测  状态估计  避障决策   速度命令
```

---

## 开发流程

### 第1周：基础搭建

- [ ] 创建项目结构
- [ ] 配置开发环境
- [ ] 实现基本节点通信
- [ ] 搭建TF树

### 第2周：传感器集成

- [ ] 激光雷达数据处理
- [ ] 相机图像处理
- [ ] IMU数据融合
- [ ] 传感器可视化

### 第3周：导航功能

- [ ] 地图加载
- [ ] 定位实现
- [ ] 路径规划
- [ ] 避障控制

### 第4周：任务系统

- [ ] 任务定义
- [ ] 状态机实现
- [ ] 任务调度
- [ ] 异常处理

### 第5周：测试优化

- [ ] 单元测试
- [ ] 集成测试
- [ ] 性能优化
- [ ] 文档完善

---

## 关键技术

### 1. 状态管理

使用状态机管理机器人行为：

```python
IDLE -> NAVIGATING -> TASK_EXECUTING -> IDLE
         ↓
      AVOIDING (临时状态)
         ↓
      NAVIGATING
```

### 2. 异常恢复

实现多层次的异常恢复机制：

1. **局部恢复** - 重新规划路径
2. **中等恢复** - 后退并重试
3. **完全恢复** - 返回安全点

### 3. 性能优化

- 使用多线程处理传感器数据
- 降低不重要话题的发布频率
- 优化算法复杂度

---

## 调试技巧

### 1. 查看系统状态

```bash
# 查看所有节点
ros2 node list

# 查看话题
ros2 topic list

# 查看TF树
ros2 run tf2_tools view_frames
```

### 2. 监控性能

```bash
# CPU和内存使用
htop

# 话题频率
ros2 topic hz /scan

# 话题带宽
ros2 topic bw /camera/image
```

### 3. 日志分析

```bash
# 查看日志
ros2 run rqt_console rqt_console

# 设置日志级别
ros2 run <package> <node> --ros-args --log-level debug
```

---

## 常见问题

### Q1: 机器人不响应命令？

检查：
- 节点是否正常运行
- 话题是否正确连接
- TF树是否完整

### Q2: 导航失败？

检查：
- 地图是否正确加载
- 定位是否准确
- 目标点是否可达

### Q3: 传感器数据异常？

检查：
- 传感器连接
- 数据格式
- 坐标系配置

---

## 项目评估标准

### 功能完整性 (40%)
- [ ] 所有核心功能实现
- [ ] 异常处理完善
- [ ] 用户界面友好

### 代码质量 (30%)
- [ ] 代码结构清晰
- [ ] 注释完整
- [ ] 符合编码规范

### 性能表现 (20%)
- [ ] 满足性能指标
- [ ] 资源使用合理
- [ ] 响应及时

### 文档完善 (10%)
- [ ] 设计文档完整
- [ ] 用户手册清晰
- [ ] 代码注释充分

---

## 提交清单

- [ ] 完整源代码
- [ ] 配置文件
- [ ] Launch文件
- [ ] 测试脚本
- [ ] 系统设计文档
- [ ] 用户手册
- [ ] 演示视频
- [ ] 测试报告

---

## 参考资源

- ROS2官方教程
- Nav2文档
- 本课程前10个阶段内容
- 开源机器人项目

祝你项目开发顺利！🚀
