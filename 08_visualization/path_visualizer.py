#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped
import math


class PathVisualizer(Node):
    def __init__(self):
        super().__init__('path_visualizer')
        
        self.publisher = self.create_publisher(Path, 'robot_path', 10)
        
        self.timer = self.create_timer(0.1, self.timer_callback)
        
        self.path = Path()
        self.path.header.frame_id = "map"
        
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        
        self.get_logger().info('路径可视化器已启动')
        self.get_logger().info('在RViz中添加Path显示，话题: /robot_path')
    
    def timer_callback(self):
        self.x += 0.05 * math.cos(self.theta)
        self.y += 0.05 * math.sin(self.theta)
        self.theta += 0.02
        
        pose = PoseStamped()
        pose.header.frame_id = "map"
        pose.header.stamp = self.get_clock().now().to_msg()
        pose.pose.position.x = self.x
        pose.pose.position.y = self.y
        pose.pose.position.z = 0.0
        
        pose.pose.orientation.z = math.sin(self.theta / 2)
        pose.pose.orientation.w = math.cos(self.theta / 2)
        
        self.path.poses.append(pose)
        
        if len(self.path.poses) > 500:
            self.path.poses.pop(0)
        
        self.path.header.stamp = self.get_clock().now().to_msg()
        self.publisher.publish(self.path)


def main(args=None):
    rclpy.init(args=args)
    node = PathVisualizer()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
