#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from custom_interfaces.msg import RobotStatus, SensorData
from geometry_msgs.msg import Point
import random
import math


class CustomMessagePublisher(Node):
    """发布自定义消息的节点"""
    
    def __init__(self):
        super().__init__('custom_msg_publisher')
        
        # 创建发布者
        self.robot_status_pub = self.create_publisher(
            RobotStatus,
            'robot_status',
            10
        )
        
        self.sensor_data_pub = self.create_publisher(
            SensorData,
            'sensor_data',
            10
        )
        
        # 定时器
        self.timer1 = self.create_timer(1.0, self.publish_robot_status)
        self.timer2 = self.create_timer(0.5, self.publish_sensor_data)
        
        # 状态变量
        self.counter = 0
        self.statuses = ['IDLE', 'RUNNING', 'PAUSED', 'CHARGING']
        self.battery_level = 100.0
        self.position_x = 0.0
        self.position_y = 0.0
        
        self.get_logger().info('自定义消息发布者已启动')
    
    def publish_robot_status(self):
        """发布机器人状态"""
        msg = RobotStatus()
        
        # 填充消息头
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'
        
        # 机器人信息
        msg.robot_id = 'robot_001'
        msg.status = self.statuses[self.counter % len(self.statuses)]
        
        # 电池逐渐消耗
        self.battery_level = max(0.0, self.battery_level - 0.5)
        if self.battery_level < 20.0:
            msg.status = 'CHARGING'
            self.battery_level = min(100.0, self.battery_level + 5.0)
        msg.battery_level = self.battery_level
        
        # 位置更新
        self.position_x += 0.1 * math.cos(self.counter * 0.1)
        self.position_y += 0.1 * math.sin(self.counter * 0.1)
        msg.position = Point(x=self.position_x, y=self.position_y, z=0.0)
        
        # 速度
        msg.velocity = 0.5 if msg.status == 'RUNNING' else 0.0
        
        # 任务状态
        msg.is_busy = msg.status == 'RUNNING'
        
        # 错误代码
        msg.error_code = 0 if msg.status != 'PAUSED' else 100
        
        # 消息
        msg.message = f'机器人正常运行，计数: {self.counter}'
        
        self.robot_status_pub.publish(msg)
        self.get_logger().info(
            f'发布状态: {msg.status}, 电池: {msg.battery_level:.1f}%, '
            f'位置: ({msg.position.x:.2f}, {msg.position.y:.2f})'
        )
        
        self.counter += 1
    
    def publish_sensor_data(self):
        """发布传感器数据"""
        msg = SensorData()
        
        # 填充消息头
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'sensor_frame'
        
        # 传感器信息
        msg.sensor_type = 'LIDAR'
        msg.sensor_id = 1
        
        # 模拟激光雷达数据 (360度扫描)
        num_points = 36
        msg.values = [
            random.uniform(0.5, 10.0) for _ in range(num_points)
        ]
        
        # 数据质量
        msg.quality = random.uniform(0.8, 1.0)
        
        # 有效性
        msg.is_valid = msg.quality > 0.85
        
        self.sensor_data_pub.publish(msg)
        self.get_logger().debug(
            f'发布传感器数据: {msg.sensor_type}, '
            f'点数: {len(msg.values)}, 质量: {msg.quality:.2f}'
        )


def main(args=None):
    rclpy.init(args=args)
    
    node = CustomMessagePublisher()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('节点被用户中断')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
