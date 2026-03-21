#!/usr/bin/env python3

import rclpy
from rclpy.node import Node


class HelloNode(Node):
    def __init__(self):
        super().__init__('hello_node')
        self.get_logger().info('Hello ROS2! 节点已启动')
        
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.counter = 0
    
    def timer_callback(self):
        self.counter += 1
        self.get_logger().info(f'计数器: {self.counter}')


def main(args=None):
    rclpy.init(args=args)
    node = HelloNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
