#!/usr/bin/env python3

import rclpy
from rclpy.node import Node


class LoggerDemo(Node):
    def __init__(self):
        super().__init__('logger_demo')
        
        self.timer = self.create_timer(2.0, self.timer_callback)
        self.counter = 0
        
        self.get_logger().info('日志示例节点已启动')
    
    def timer_callback(self):
        self.get_logger().debug(f'调试信息 {self.counter}')
        self.get_logger().info(f'普通信息 {self.counter}')
        self.get_logger().warn(f'警告信息 {self.counter}')
        
        if self.counter % 5 == 0:
            self.get_logger().error(f'错误信息 {self.counter}')
        
        self.counter += 1


def main(args=None):
    rclpy.init(args=args)
    node = LoggerDemo()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
