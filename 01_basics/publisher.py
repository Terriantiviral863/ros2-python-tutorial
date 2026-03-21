#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class PublisherNode(Node):
    def __init__(self):
        super().__init__('publisher_node')
        
        self.publisher = self.create_publisher(String, 'chatter', 10)
        
        self.timer = self.create_timer(0.5, self.timer_callback)
        self.counter = 0
        
        self.get_logger().info('发布者节点已启动')
    
    def timer_callback(self):
        msg = String()
        msg.data = f'Hello ROS2! 消息编号: {self.counter}'
        
        self.publisher.publish(msg)
        self.get_logger().info(f'发布: "{msg.data}"')
        
        self.counter += 1


def main(args=None):
    rclpy.init(args=args)
    node = PublisherNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
