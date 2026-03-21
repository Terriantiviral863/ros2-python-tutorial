#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
import sys


class GoalSender(Node):
    def __init__(self):
        super().__init__('goal_sender')
        
        self.publisher = self.create_publisher(PoseStamped, 'goal_pose', 10)
        
        self.get_logger().info('目标点发送器已启动')
    
    def send_goal(self, x, y, yaw=0.0):
        goal = PoseStamped()
        goal.header.frame_id = "map"
        goal.header.stamp = self.get_clock().now().to_msg()
        
        goal.pose.position.x = x
        goal.pose.position.y = y
        goal.pose.position.z = 0.0
        
        import math
        goal.pose.orientation.z = math.sin(yaw / 2)
        goal.pose.orientation.w = math.cos(yaw / 2)
        
        self.publisher.publish(goal)
        self.get_logger().info(f'发送目标点: x={x}, y={y}, yaw={yaw}')


def main(args=None):
    rclpy.init(args=args)
    node = GoalSender()
    
    if len(sys.argv) >= 3:
        x = float(sys.argv[1])
        y = float(sys.argv[2])
        yaw = float(sys.argv[3]) if len(sys.argv) >= 4 else 0.0
        
        node.send_goal(x, y, yaw)
        
        rclpy.spin_once(node, timeout_sec=1.0)
    else:
        node.get_logger().info('用法: python3 goal_sender.py <x> <y> [yaw]')
        node.get_logger().info('示例: python3 goal_sender.py 2.0 1.5 0.0')
    
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
