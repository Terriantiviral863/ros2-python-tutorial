#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
import argparse
import os


class RobotDisplay(Node):
    def __init__(self, urdf_file=None):
        super().__init__('robot_display')
        
        self.joint_pub = self.create_publisher(JointState, 'joint_states', 10)
        
        self.timer = self.create_timer(0.1, self.timer_callback)
        
        self.joint_angle = 0.0
        
        if urdf_file:
            self.get_logger().info(f'显示URDF模型: {urdf_file}')
        else:
            self.get_logger().info('显示默认机器人模型')
        
        self.get_logger().info('机器人显示节点已启动')
        self.get_logger().info('在RViz2中查看机器人模型:')
        self.get_logger().info('  1. 运行: rviz2')
        self.get_logger().info('  2. 添加 RobotModel 显示')
        self.get_logger().info('  3. 设置 Fixed Frame 为 base_link')
    
    def timer_callback(self):
        msg = JointState()
        msg.header = Header()
        msg.header.stamp = self.get_clock().now().to_msg()
        
        msg.name = ['left_wheel_joint', 'right_wheel_joint']
        msg.position = [self.joint_angle, self.joint_angle]
        msg.velocity = []
        msg.effort = []
        
        self.joint_pub.publish(msg)
        
        self.joint_angle += 0.01


def main(args=None):
    parser = argparse.ArgumentParser(description='显示机器人URDF模型')
    parser.add_argument('--urdf', type=str, help='URDF文件路径')
    cmd_args = parser.parse_args()
    
    rclpy.init(args=args)
    node = RobotDisplay(urdf_file=cmd_args.urdf)
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
