#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class SimplePublisher(Node):
    """
    简单的发布者节点示例
    演示如何在ROS2包中创建发布者
    """
    
    def __init__(self):
        super().__init__('simple_publisher')
        
        self.publisher_ = self.create_publisher(String, 'example_topic', 10)
        
        timer_period = 1.0
        self.timer = self.create_timer(timer_period, self.timer_callback)
        
        self.counter = 0
        
        self.get_logger().info('简单发布者节点已启动')
    
    def timer_callback(self):
        msg = String()
        msg.data = f'来自Python包的消息 #{self.counter}'
        
        self.publisher_.publish(msg)
        self.get_logger().info(f'发布: "{msg.data}"')
        
        self.counter += 1


def main(args=None):
    rclpy.init(args=args)
    node = SimplePublisher()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
