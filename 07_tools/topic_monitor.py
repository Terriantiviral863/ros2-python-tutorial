#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class TopicMonitor(Node):
    def __init__(self):
        super().__init__('topic_monitor')
        
        self.subscription = self.create_subscription(
            String,
            'test_topic',
            self.listener_callback,
            10
        )
        
        self.msg_count = 0
        self.get_logger().info('话题监控器已启动')
    
    def listener_callback(self, msg):
        self.msg_count += 1
        self.get_logger().info(f'收到消息 #{self.msg_count}: {msg.data}')


def main(args=None):
    rclpy.init(args=args)
    node = TopicMonitor()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
