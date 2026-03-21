#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class SubscriberNode(Node):
    def __init__(self):
        super().__init__('subscriber_node')
        
        self.subscription = self.create_subscription(
            String,
            'chatter',
            self.listener_callback,
            10
        )
        
        self.get_logger().info('订阅者节点已启动，等待消息...')
    
    def listener_callback(self, msg):
        self.get_logger().info(f'收到: "{msg.data}"')


def main(args=None):
    rclpy.init(args=args)
    node = SubscriberNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
