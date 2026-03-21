#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Listener(Node):
    def __init__(self):
        super().__init__('listener')
        
        self.declare_parameter('log_level', 'info')
        
        self.subscription = self.create_subscription(
            String,
            'chatter',
            self.listener_callback,
            10
        )
        
        log_level = self.get_parameter('log_level').value
        self.get_logger().info(f'Listener节点已启动 - 日志级别: {log_level}')
    
    def listener_callback(self, msg):
        self.get_logger().info(f'收到: "{msg.data}"')


def main(args=None):
    rclpy.init(args=args)
    node = Listener()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
