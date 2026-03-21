#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy
from std_msgs.msg import String, Int32, Float32
from sensor_msgs.msg import Temperature
import random
import math


class MultiTopicNode(Node):
    """演示多话题通信和QoS配置的节点"""
    
    def __init__(self):
        super().__init__('multi_topic_node')
        
        # 定义不同的QoS配置
        self.sensor_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )
        
        self.reliable_qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10,
            durability=DurabilityPolicy.TRANSIENT_LOCAL
        )
        
        # 创建多个发布者
        self.temp_publisher = self.create_publisher(
            Temperature, 
            'sensor/temperature', 
            self.sensor_qos
        )
        
        self.status_publisher = self.create_publisher(
            String, 
            'robot/status', 
            self.reliable_qos
        )
        
        self.counter_publisher = self.create_publisher(
            Int32, 
            'system/counter', 
            10
        )
        
        self.voltage_publisher = self.create_publisher(
            Float32, 
            'sensor/voltage', 
            self.sensor_qos
        )
        
        # 创建多个订阅者
        self.temp_subscriber = self.create_subscription(
            Temperature,
            'sensor/temperature',
            self.temperature_callback,
            self.sensor_qos
        )
        
        self.status_subscriber = self.create_subscription(
            String,
            'robot/status',
            self.status_callback,
            self.reliable_qos
        )
        
        # 定时器 - 不同频率发布不同数据
        self.timer1 = self.create_timer(0.5, self.publish_temperature)  # 2Hz
        self.timer2 = self.create_timer(1.0, self.publish_status)       # 1Hz
        self.timer3 = self.create_timer(0.1, self.publish_counter)      # 10Hz
        self.timer4 = self.create_timer(0.2, self.publish_voltage)      # 5Hz
        
        # 计数器
        self.counter = 0
        self.status_index = 0
        self.statuses = ['IDLE', 'RUNNING', 'PAUSED', 'ERROR', 'CHARGING']
        
        self.get_logger().info('多话题通信节点已启动')
        self.get_logger().info('发布话题: /sensor/temperature, /robot/status, /system/counter, /sensor/voltage')
    
    def publish_temperature(self):
        """发布温度数据 - 使用BEST_EFFORT QoS"""
        msg = Temperature()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'temperature_sensor'
        # 模拟温度波动 (20-30度)
        msg.temperature = 25.0 + 5.0 * math.sin(self.counter * 0.1)
        msg.variance = 0.5
        
        self.temp_publisher.publish(msg)
        self.get_logger().debug(f'发布温度: {msg.temperature:.2f}°C')
    
    def publish_status(self):
        """发布状态信息 - 使用RELIABLE QoS"""
        msg = String()
        msg.data = self.statuses[self.status_index]
        
        self.status_publisher.publish(msg)
        self.get_logger().info(f'发布状态: {msg.data}')
        
        self.status_index = (self.status_index + 1) % len(self.statuses)
    
    def publish_counter(self):
        """发布计数器 - 高频率"""
        msg = Int32()
        msg.data = self.counter
        
        self.counter_publisher.publish(msg)
        self.counter += 1
    
    def publish_voltage(self):
        """发布电压数据"""
        msg = Float32()
        # 模拟电压 (11.5-12.5V)
        msg.data = 12.0 + 0.5 * random.uniform(-1, 1)
        
        self.voltage_publisher.publish(msg)
        self.get_logger().debug(f'发布电压: {msg.data:.2f}V')
    
    def temperature_callback(self, msg):
        """温度订阅回调"""
        if msg.temperature > 28.0:
            self.get_logger().warn(f'温度过高: {msg.temperature:.2f}°C')
    
    def status_callback(self, msg):
        """状态订阅回调"""
        if msg.data == 'ERROR':
            self.get_logger().error(f'系统错误状态: {msg.data}')


def main(args=None):
    rclpy.init(args=args)
    
    node = MultiTopicNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('节点被用户中断')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
