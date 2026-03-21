#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from std_msgs.msg import String, Float32
from geometry_msgs.msg import Twist
import random
import math


class SensorNode(Node):
    """传感器节点 - 模拟传感器数据"""
    
    def __init__(self):
        super().__init__('sensor_node')
        
        # 发布传感器数据
        self.temp_pub = self.create_publisher(Float32, 'sensor/temperature', 10)
        self.distance_pub = self.create_publisher(Float32, 'sensor/distance', 10)
        
        # 定时发布
        self.timer = self.create_timer(0.5, self.publish_sensor_data)
        
        self.counter = 0
        self.get_logger().info('传感器节点已启动')
    
    def publish_sensor_data(self):
        """发布传感器数据"""
        # 温度数据 (20-30度)
        temp_msg = Float32()
        temp_msg.data = 25.0 + 5.0 * math.sin(self.counter * 0.1)
        self.temp_pub.publish(temp_msg)
        
        # 距离数据 (0.5-5米)
        dist_msg = Float32()
        dist_msg.data = 2.5 + 2.0 * random.uniform(-1, 1)
        self.distance_pub.publish(dist_msg)
        
        self.counter += 1


class ProcessingNode(Node):
    """处理节点 - 处理传感器数据并做出决策"""
    
    def __init__(self):
        super().__init__('processing_node')
        
        # 订阅传感器数据
        self.temp_sub = self.create_subscription(
            Float32, 'sensor/temperature', self.temperature_callback, 10
        )
        self.dist_sub = self.create_subscription(
            Float32, 'sensor/distance', self.distance_callback, 10
        )
        
        # 发布决策结果
        self.decision_pub = self.create_publisher(String, 'decision/command', 10)
        
        # 状态变量
        self.current_temp = 0.0
        self.current_distance = 0.0
        
        # 定时做出决策
        self.timer = self.create_timer(1.0, self.make_decision)
        
        self.get_logger().info('处理节点已启动')
    
    def temperature_callback(self, msg):
        """温度回调"""
        self.current_temp = msg.data
        self.get_logger().debug(f'接收温度: {self.current_temp:.2f}°C')
    
    def distance_callback(self, msg):
        """距离回调"""
        self.current_distance = msg.data
        self.get_logger().debug(f'接收距离: {self.current_distance:.2f}m')
    
    def make_decision(self):
        """基于传感器数据做出决策"""
        command = String()
        
        # 决策逻辑
        if self.current_temp > 28.0:
            command.data = 'COOLING_NEEDED'
            self.get_logger().warn(f'温度过高 ({self.current_temp:.2f}°C), 需要降温')
        elif self.current_distance < 1.0:
            command.data = 'OBSTACLE_DETECTED'
            self.get_logger().warn(f'检测到障碍物 ({self.current_distance:.2f}m), 停止')
        elif self.current_distance < 2.0:
            command.data = 'SLOW_DOWN'
            self.get_logger().info(f'接近障碍物 ({self.current_distance:.2f}m), 减速')
        else:
            command.data = 'NORMAL'
            self.get_logger().info('状态正常，继续前进')
        
        self.decision_pub.publish(command)


class ControlNode(Node):
    """控制节点 - 根据决策执行控制命令"""
    
    def __init__(self):
        super().__init__('control_node')
        
        # 订阅决策命令
        self.command_sub = self.create_subscription(
            String, 'decision/command', self.command_callback, 10
        )
        
        # 发布控制指令
        self.control_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        
        # 发布状态
        self.status_pub = self.create_publisher(String, 'robot/status', 10)
        
        self.current_command = 'NORMAL'
        
        # 定时发布控制指令
        self.timer = self.create_timer(0.2, self.publish_control)
        
        self.get_logger().info('控制节点已启动')
    
    def command_callback(self, msg):
        """命令回调"""
        if msg.data != self.current_command:
            self.get_logger().info(f'收到新命令: {msg.data}')
            self.current_command = msg.data
    
    def publish_control(self):
        """发布控制指令"""
        twist = Twist()
        status = String()
        
        # 根据命令设置速度
        if self.current_command == 'NORMAL':
            twist.linear.x = 0.5
            twist.angular.z = 0.0
            status.data = 'RUNNING'
        elif self.current_command == 'SLOW_DOWN':
            twist.linear.x = 0.2
            twist.angular.z = 0.0
            status.data = 'SLOWING'
        elif self.current_command == 'OBSTACLE_DETECTED':
            twist.linear.x = 0.0
            twist.angular.z = 0.0
            status.data = 'STOPPED'
        elif self.current_command == 'COOLING_NEEDED':
            twist.linear.x = 0.0
            twist.angular.z = 0.0
            status.data = 'COOLING'
        else:
            twist.linear.x = 0.0
            twist.angular.z = 0.0
            status.data = 'IDLE'
        
        self.control_pub.publish(twist)
        self.status_pub.publish(status)


def main(args=None):
    rclpy.init(args=args)
    
    # 创建所有节点
    sensor_node = SensorNode()
    processing_node = ProcessingNode()
    control_node = ControlNode()
    
    # 使用多线程执行器
    executor = MultiThreadedExecutor()
    executor.add_node(sensor_node)
    executor.add_node(processing_node)
    executor.add_node(control_node)
    
    try:
        print('\n' + '='*60)
        print('多节点系统已启动')
        print('='*60)
        print('节点架构:')
        print('  [传感器节点] -> 发布温度和距离数据')
        print('  [处理节点]   -> 分析数据并做出决策')
        print('  [控制节点]   -> 执行控制命令')
        print('='*60 + '\n')
        
        executor.spin()
    except KeyboardInterrupt:
        print('\n系统被用户中断')
    finally:
        sensor_node.destroy_node()
        processing_node.destroy_node()
        control_node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
