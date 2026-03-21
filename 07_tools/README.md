# 第七阶段：ROS2开发工具

## 学习目标

- 掌握ROS2命令行工具
- 学习使用RQt可视化工具
- 理解bag文件录制和回放
- 学习参数服务器使用
- 掌握日志系统

---

## 目录结构

```
07_tools/
├── README.md
├── bag_recorder.py
├── bag_player.py
├── param_manager.py
├── logger_demo.py
└── topic_monitor.py
```

---

## ROS2命令行工具

### 节点管理

```bash
# 列出所有节点
ros2 node list

# 查看节点信息
ros2 node info /node_name

# 运行节点
ros2 run package_name node_name
```

### 话题操作

```bash
# 列出话题
ros2 topic list

# 查看话题信息
ros2 topic info /topic_name

# 显示话题内容
ros2 topic echo /topic_name

# 发布话题
ros2 topic pub /topic_name msg_type "data"

# 查看发布频率
ros2 topic hz /topic_name
```

### 服务操作

```bash
# 列出服务
ros2 service list

# 调用服务
ros2 service call /service_name srv_type "request"
```

### 参数操作

```bash
# 列出参数
ros2 param list

# 获取参数
ros2 param get /node_name param_name

# 设置参数
ros2 param set /node_name param_name value

# 保存参数
ros2 param dump /node_name
```

---

## Bag文件

### 录制

```bash
# 录制所有话题
ros2 bag record -a

# 录制指定话题
ros2 bag record /topic1 /topic2

# 指定输出文件
ros2 bag record -o output_name /topic_name
```

### 回放

```bash
# 回放bag文件
ros2 bag play bag_file

# 循环回放
ros2 bag play -l bag_file

# 查看bag信息
ros2 bag info bag_file
```

---

## RQt工具

### 安装

```bash
sudo apt install ros-humble-rqt*
```

### 常用工具

```bash
# 图形界面
rqt

# 话题监控
rqt_graph

# 消息发布
rqt_publisher

# 服务调用
rqt_service_caller

# 参数配置
rqt_reconfigure

# 绘图工具
rqt_plot

# 控制台
rqt_console
```

---

## 日志系统

### 日志级别

- DEBUG
- INFO
- WARN
- ERROR
- FATAL

### Python日志

```python
self.get_logger().debug('调试信息')
self.get_logger().info('普通信息')
self.get_logger().warn('警告信息')
self.get_logger().error('错误信息')
self.get_logger().fatal('致命错误')
```

### 设置日志级别

```bash
ros2 run package node --ros-args --log-level debug
```

---

## 下一步

完成所有练习后，进入 `08_visualization/` 学习可视化工具。
