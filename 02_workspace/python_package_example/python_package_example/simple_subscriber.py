#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class SimpleSubscriber(Node):
    """
    简单的订阅者节点示例
    演示如何在ROS2包中创建订阅者
    """
    
    def __init__(self):
        super().__init__('simple_subscriber')
        
        self.subscription = self.create_subscription(
            String,
            'example_topic',
            self.listener_callback,
            10
        )
        
        self.get_logger().info('简单订阅者节点已启动，等待消息...')
    
    def listener_callback(self, msg):
        self.get_logger().info(f'收到消息: "{msg.data}"')


def main(args=None):
    rclpy.init(args=args)
    node = SimpleSubscriber()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
