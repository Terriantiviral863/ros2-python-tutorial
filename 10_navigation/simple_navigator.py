#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped, Twist
from nav_msgs.msg import Odometry
from tf_transformations import euler_from_quaternion
import math


class SimpleNavigator(Node):
    def __init__(self):
        super().__init__('simple_navigator')
        
        self.goal_sub = self.create_subscription(
            PoseStamped,
            'goal_pose',
            self.goal_callback,
            10
        )
        
        self.odom_sub = self.create_subscription(
            Odometry,
            'odom',
            self.odom_callback,
            10
        )
        
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        
        self.timer = self.create_timer(0.1, self.control_loop)
        
        self.current_pose = None
        self.goal_pose = None
        self.goal_reached = True
        
        self.linear_tolerance = 0.1
        self.angular_tolerance = 0.1
        
        self.get_logger().info('简单导航器已启动')
        self.get_logger().info('发送目标点到: /goal_pose')
    
    def goal_callback(self, msg):
        self.goal_pose = msg
        self.goal_reached = False
        self.get_logger().info(
            f'收到新目标: x={msg.pose.position.x:.2f}, '
            f'y={msg.pose.position.y:.2f}'
        )
    
    def odom_callback(self, msg):
        self.current_pose = msg.pose.pose
    
    def control_loop(self):
        if self.current_pose is None or self.goal_pose is None or self.goal_reached:
            return
        
        dx = self.goal_pose.pose.position.x - self.current_pose.position.x
        dy = self.goal_pose.pose.position.y - self.current_pose.position.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance < self.linear_tolerance:
            self.stop_robot()
            self.goal_reached = True
            self.get_logger().info('目标已到达！')
            return
        
        q = self.current_pose.orientation
        _, _, current_yaw = euler_from_quaternion([q.x, q.y, q.z, q.w])
        
        target_yaw = math.atan2(dy, dx)
        angle_diff = self.normalize_angle(target_yaw - current_yaw)
        
        cmd = Twist()
        
        if abs(angle_diff) > self.angular_tolerance:
            cmd.linear.x = 0.0
            cmd.angular.z = 1.0 * angle_diff
        else:
            cmd.linear.x = min(0.5, distance * 0.5)
            cmd.angular.z = 0.5 * angle_diff
        
        self.cmd_vel_pub.publish(cmd)
    
    def stop_robot(self):
        cmd = Twist()
        cmd.linear.x = 0.0
        cmd.angular.z = 0.0
        self.cmd_vel_pub.publish(cmd)
    
    def normalize_angle(self, angle):
        while angle > math.pi:
            angle -= 2 * math.pi
        while angle < -math.pi:
            angle += 2 * math.pi
        return angle


def main(args=None):
    rclpy.init(args=args)
    node = SimpleNavigator()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
