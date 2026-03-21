# ROS2 Python 完整学习教程

<div align="center">

![ROS2](https://img.shields.io/badge/ROS2-Humble-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Platform](https://img.shields.io/badge/Platform-Linux-orange)

**从零开始学习ROS2机器人开发的完整Python教程**

[快速开始](#快速开始) • [课程内容](#课程内容) • [项目特色](#项目特色) • [学习路线](#学习路线)

</div>

---

## 📖 项目简介

这是一个完整的ROS2 Python学习教程，包含**11个阶段**、**111个示例文件**，涵盖从基础入门到综合项目的全部内容。所有代码均使用Python实现，适合机器人开发初学者和进阶学习者。

### ✨ 项目特色

- 🎯 **系统完整** - 11个阶段循序渐进，覆盖ROS2核心知识
- 💻 **纯Python实现** - 所有示例均使用Python，易学易用
- 🤖 **实战导向** - 每个阶段都有可运行的实例代码
- 📚 **文档详尽** - 每个阶段都有详细的README和注释
- 🚀 **综合项目** - 最终阶段整合所有知识点的完整机器人系统

### 📊 课程统计

| 指标 | 数量 |
|------|------|
| 学习阶段 | 11个 |
| 示例文件 | 111个 |
| Python脚本 | 90+ |
| 配置文件 | 20+ |
| 代码行数 | 8000+ |

---

## 🚀 快速开始

### 环境要求

- **操作系统**: Ubuntu 22.04 (推荐) 或其他Linux发行版
- **ROS2版本**: Humble Hawksbill
- **Python版本**: 3.8+
- **硬件**: 支持x86_64或ARM64架构（如Jetson）

### 安装ROS2

```bash
# 设置locale
sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8

# 添加ROS2源
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update && sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

# 安装ROS2
sudo apt update
sudo apt install ros-humble-desktop python3-argcomplete
sudo apt install ros-dev-tools

# 配置环境
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

### 克隆项目

```bash
git clone https://github.com/yourusername/ros2-python-tutorial.git
cd ros2-python-tutorial
```

### 运行第一个示例

```bash
# 进入基础教程目录
cd 01_basics

# 运行第一个ROS2节点
python3 hello_ros2.py

# 在另一个终端查看节点信息
ros2 node list
ros2 node info /hello_node
```

---

## 📚 课程内容

### 第一阶段：基础入门 (01_basics)
- ROS2基本概念
- 创建第一个节点
- 话题发布与订阅
- 服务调用
- **文件数**: 8个

### 第二阶段：工作空间 (02_workspace)
- 工作空间结构
- 包的创建与管理
- 依赖管理
- 构建系统
- **文件数**: 13个

### 第三阶段：通信机制 (03_communication)
- Topic通信详解
- Service请求响应
- Action长时间任务
- QoS服务质量
- 自定义消息类型
- **文件数**: 17个

### 第四阶段：Launch系统 (04_launch)
- Python Launch文件
- 多节点启动
- 参数配置
- 命名空间
- 条件启动
- **文件数**: 12个

### 第五阶段：TF2坐标变换 (05_tf2)
- 坐标系概念
- 静态变换发布
- 动态变换发布
- 变换监听
- TF树构建
- **文件数**: 8个

### 第六阶段：机器人建模 (06_robot_modeling)
- URDF机器人描述
- Xacro宏语言
- 关节与连杆
- RViz可视化
- 机器人状态发布
- **文件数**: 13个

### 第七阶段：开发工具 (07_tools)
- ROS2命令行工具
- Bag文件录制回放
- 参数服务器
- 日志系统
- RQt工具集
- **文件数**: 5个

### 第八阶段：可视化 (08_visualization)
- RViz2使用
- Marker可视化
- 点云显示
- 图像显示
- 路径可视化
- 交互式Marker
- **文件数**: 7个

### 第九阶段：传感器集成 (09_sensors)
- 激光雷达处理
- 相机图像处理
- IMU数据处理
- 传感器融合
- 障碍物检测
- **文件数**: 9个

### 第十阶段：导航系统 (10_navigation)
- 路径规划（A*算法）
- 定位（粒子滤波）
- 避障控制
- 地图构建
- 航点跟随
- **文件数**: 9个

### 第十一阶段：综合项目 (11_final_project)
- 完整机器人系统
- 状态机设计
- 任务调度
- 传感器管理
- 导航控制
- 用户界面
- **文件数**: 10个

---

## 🎯 学习路线

```mermaid
graph LR
    A[01 基础入门] --> B[02 工作空间]
    B --> C[03 通信机制]
    C --> D[04 Launch系统]
    D --> E[05 TF2坐标]
    E --> F[06 机器人建模]
    F --> G[07 开发工具]
    G --> H[08 可视化]
    H --> I[09 传感器]
    I --> J[10 导航系统]
    J --> K[11 综合项目]
```

### 建议学习时间

| 阶段 | 建议时间 | 难度 |
|------|---------|------|
| 01-02 | 1周 | ⭐ |
| 03-04 | 1-2周 | ⭐⭐ |
| 05-06 | 1-2周 | ⭐⭐⭐ |
| 07-08 | 1周 | ⭐⭐ |
| 09-10 | 2-3周 | ⭐⭐⭐⭐ |
| 11 | 2-3周 | ⭐⭐⭐⭐⭐ |

**总计**: 8-12周完成全部课程

---

## 💡 使用指南

### 学习建议

1. **循序渐进** - 按照编号顺序学习，不要跳过基础章节
2. **动手实践** - 运行每个示例，修改参数观察变化
3. **理解原理** - 不仅要会用，更要理解为什么这样做
4. **记录笔记** - 在`notes/`目录记录学习心得和问题
5. **查阅文档** - 遇到问题先查ROS2官方文档

### 常用命令速查

```bash
# 节点操作
ros2 node list                    # 列出所有节点
ros2 node info /node_name         # 查看节点信息

# 话题操作
ros2 topic list                   # 列出所有话题
ros2 topic echo /topic_name       # 查看话题内容
ros2 topic hz /topic_name         # 查看发布频率
ros2 topic pub /topic_name ...    # 发布话题

# 服务操作
ros2 service list                 # 列出所有服务
ros2 service call /service ...    # 调用服务

# 参数操作
ros2 param list                   # 列出所有参数
ros2 param get /node param        # 获取参数值
ros2 param set /node param value  # 设置参数值

# Bag操作
ros2 bag record -a                # 录制所有话题
ros2 bag play bag_file            # 回放bag文件

# TF操作
ros2 run tf2_tools view_frames    # 查看TF树
ros2 run tf2_ros tf2_echo ...     # 查看坐标变换
```

---

## 📁 目录结构

```
ros2-python-tutorial/
├── README.md                      # 项目说明（本文件）
├── ROS2_LEARNING_PLAN.md          # 详细学习计划
├── 01_basics/                     # 基础入门
│   ├── README.md
│   ├── hello_ros2.py
│   ├── publisher_demo.py
│   └── ...
├── 02_workspace/                  # 工作空间
│   ├── README.md
│   └── ...
├── 03_communication/              # 通信机制
│   ├── README.md
│   ├── topic_publisher.py
│   ├── service_server.py
│   └── ...
├── 04_launch/                     # Launch系统
├── 05_tf2/                        # 坐标变换
├── 06_robot_modeling/             # 机器人建模
│   ├── urdf/
│   ├── xacro/
│   └── ...
├── 07_tools/                      # 开发工具
├── 08_visualization/              # 可视化
├── 09_sensors/                    # 传感器集成
├── 10_navigation/                 # 导航系统
├── 11_final_project/              # 综合项目
│   ├── robot_system/
│   ├── launch/
│   ├── config/
│   └── ...
└── notes/                         # 学习笔记
```

---

## 🛠️ 技术栈

- **ROS2 Humble** - 机器人操作系统
- **Python 3** - 编程语言
- **rclpy** - ROS2 Python客户端库
- **NumPy** - 数值计算
- **OpenCV** - 图像处理
- **tf2** - 坐标变换
- **Nav2** - 导航框架

---

## 📖 参考资源

### 官方文档
- [ROS2 Humble官方文档](https://docs.ros.org/en/humble/)
- [ROS2教程](https://docs.ros.org/en/humble/Tutorials.html)
- [rclpy API文档](https://docs.ros2.org/humble/api/rclpy/)

### 推荐学习资源
- [ROS2设计文档](https://design.ros2.org/)
- [Nav2导航框架](https://navigation.ros.org/)
- [ROS Answers](https://answers.ros.org/)
- [ROS Discourse](https://discourse.ros.org/)

---

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

### 如何贡献

1. Fork本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交Pull Request

### 贡献方向

- 修复代码错误
- 改进文档说明
- 添加新的示例
- 优化代码性能
- 翻译成其他语言

---

## 📝 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 👨‍💻 作者

**DdXd**

- GitHub: [@ddxd001](https://github.com/ddxd001)
- Email: d18797323123@qq.com

---

## 🙏 致谢

- 感谢ROS2社区提供的优秀框架
- 感谢所有贡献者的支持
- 感谢开源社区的无私分享

---

## ⭐ Star History

如果这个项目对你有帮助，请给个Star支持一下！

[![Star History Chart](https://api.star-history.com/svg?repos=ddxd001/ros2-python-tutorial&type=Date)](https://star-history.com/#ddxd001/ros2-python-tutorial&Date)

---

<div align="center">

**开始你的ROS2学习之旅吧！🚀**

[回到顶部](#ros2-python-完整学习教程)

</div>
