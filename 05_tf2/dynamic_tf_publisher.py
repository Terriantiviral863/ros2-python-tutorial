#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped
from tf_transformations import quaternion_from_euler
import math


class DynamicTFPublisher(Node):
    def __init__(self):
        super().__init__('dynamic_tf_publisher')
        
        self.tf_broadcaster = TransformBroadcaster(self)
        
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        
        self.timer = self.create_timer(0.1, self.broadcast_timer_callback)
        
        self.get_logger().info('动态TF发布器已启动')
        self.get_logger().info('发布 world -> base_link 的动态变换')
    
    def broadcast_timer_callback(self):
        t = TransformStamped()
        
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'world'
        t.child_frame_id = 'base_link'
        
        self.x += 0.01 * math.cos(self.theta)
        self.y += 0.01 * math.sin(self.theta)
        self.theta += 0.02
        
        t.transform.translation.x = self.x
        t.transform.translation.y = self.y
        t.transform.translation.z = 0.0
        
        q = quaternion_from_euler(0, 0, self.theta)
        t.transform.rotation.x = q[0]
        t.transform.rotation.y = q[1]
        t.transform.rotation.z = q[2]
        t.transform.rotation.w = q[3]
        
        self.tf_broadcaster.sendTransform(t)


def main(args=None):
    rclpy.init(args=args)
    node = DynamicTFPublisher()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
