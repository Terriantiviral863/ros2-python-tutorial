# 机器人建模快速开始

## 快速验证URDF

```bash
# 检查URDF语法
check_urdf 06_robot_modeling/urdf/simple_robot.urdf

# 查看模型树结构
urdf_to_graphiz 06_robot_modeling/urdf/simple_robot.urdf
```

## 在RViz中显示机器人

### 方法1：使用display_robot.py

```bash
# 终端1：运行显示节点
python3 06_robot_modeling/display_robot.py --urdf 06_robot_modeling/urdf/simple_robot.urdf

# 终端2：启动RViz
rviz2
```

在RViz中：
1. 点击 Add -> RobotModel
2. 设置 Fixed Frame 为 `base_link`
3. 查看机器人模型

### 方法2：使用robot_state_publisher

```bash
# 终端1：发布机器人描述
ros2 run robot_state_publisher robot_state_publisher --ros-args -p robot_description:="$(cat 06_robot_modeling/urdf/simple_robot.urdf)"

# 终端2：发布关节状态
python3 06_robot_modeling/joint_controller.py

# 终端3：启动RViz
rviz2
```

## Xacro转换

```bash
# 转换Xacro为URDF
ros2 run xacro xacro 06_robot_modeling/xacro/robot.xacro > /tmp/robot.urdf

# 查看生成的URDF
cat /tmp/robot.urdf

# 显示
python3 06_robot_modeling/display_robot.py --urdf /tmp/robot.urdf
```

## 交互式关节控制

```bash
# 安装joint_state_publisher_gui
sudo apt install ros-humble-joint-state-publisher-gui

# 运行
ros2 run joint_state_publisher_gui joint_state_publisher_gui
```

## 查看TF树

```bash
# 生成TF树图
ros2 run tf2_tools view_frames

# 查看PDF
evince frames.pdf
```

## 常见问题

### Q: URDF文件找不到？
确保使用正确的相对路径或绝对路径。

### Q: RViz中看不到模型？
检查：
1. Fixed Frame 设置是否正确
2. robot_state_publisher 是否运行
3. URDF是否有语法错误

### Q: 关节不动？
确保发布了 `/joint_states` 话题。
