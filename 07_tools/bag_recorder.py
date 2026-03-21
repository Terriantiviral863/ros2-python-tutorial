#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class BagRecorder(Node):
    def __init__(self):
        super().__init__('bag_recorder')
        
        self.publisher = self.create_publisher(String, 'test_topic', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.counter = 0
        
        self.get_logger().info('Bag录制示例节点已启动')
        self.get_logger().info('使用: ros2 bag record /test_topic')
    
    def timer_callback(self):
        msg = String()
        msg.data = f'消息 {self.counter}'
        self.publisher.publish(msg)
        self.get_logger().info(f'发布: {msg.data}')
        self.counter += 1


def main(args=None):
    rclpy.init(args=args)
    node = BagRecorder()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
