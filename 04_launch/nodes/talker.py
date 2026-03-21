#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Talker(Node):
    def __init__(self):
        super().__init__('talker')
        
        self.declare_parameter('message', 'Hello ROS2')
        self.declare_parameter('publish_rate', 1.0)
        
        message = self.get_parameter('message').value
        rate = self.get_parameter('publish_rate').value
        
        self.publisher = self.create_publisher(String, 'chatter', 10)
        self.timer = self.create_timer(1.0 / rate, self.timer_callback)
        self.counter = 0
        
        self.get_logger().info(f'Talker节点已启动 - 消息: "{message}", 频率: {rate}Hz')
    
    def timer_callback(self):
        msg = String()
        message = self.get_parameter('message').value
        msg.data = f'{message} #{self.counter}'
        self.publisher.publish(msg)
        self.get_logger().info(f'发布: "{msg.data}"')
        self.counter += 1


def main(args=None):
    rclpy.init(args=args)
    node = Talker()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
