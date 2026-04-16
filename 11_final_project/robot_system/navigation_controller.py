#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped, Twist
from nav_msgs.msg import Path, Odometry
from sensor_msgs.msg import LaserScan
import math


def euler_from_quaternion(quaternion):
    """
    Convert quaternion to euler angles (roll, pitch, yaw)
    """
    x, y, z, w = quaternion
    
    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    roll = math.atan2(t0, t1)
    
    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    pitch = math.asin(t2)
    
    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    yaw = math.atan2(t3, t4)
    
    return roll, pitch, yaw


class NavigationController(Node):
    def __init__(self):
        super().__init__('navigation_controller')
        
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
        
        self.scan_sub = self.create_subscription(
            LaserScan,
            'scan',
            self.scan_callback,
            10
        )
        
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.path_pub = self.create_publisher(Path, 'planned_path', 10)
        
        self.timer = self.create_timer(0.1, self.control_loop)
        
        self.current_pose = None
        self.goal_pose = None
        self.scan_data = None
        
        self.goal_tolerance = 0.2
        self.obstacle_distance = 0.5
        
        self.get_logger().info('导航控制器已启动')
    
    def goal_callback(self, msg):
        self.goal_pose = msg
        self.get_logger().info(
            f'收到导航目标: ({msg.pose.position.x:.2f}, {msg.pose.position.y:.2f})'
        )
    
    def odom_callback(self, msg):
        self.current_pose = msg.pose.pose
    
    def scan_callback(self, msg):
        self.scan_data = msg
    
    def control_loop(self):
        if self.current_pose is None or self.goal_pose is None:
            return
        
        if self.check_obstacle():
            self.avoid_obstacle()
            return
        
        if self.reached_goal():
            self.stop_robot()
            self.get_logger().info('已到达目标点')
            self.goal_pose = None
            return
        
        self.navigate_to_goal()
    
    def check_obstacle(self):
        if self.scan_data is None:
            return False
        
        front_ranges = self.scan_data.ranges[
            len(self.scan_data.ranges)//2 - 20:
            len(self.scan_data.ranges)//2 + 20
        ]
        
        valid_ranges = [r for r in front_ranges 
                       if self.scan_data.range_min < r < self.scan_data.range_max]
        
        if valid_ranges and min(valid_ranges) < self.obstacle_distance:
            return True
        
        return False
    
    def avoid_obstacle(self):
        cmd = Twist()
        cmd.linear.x = 0.0
        cmd.angular.z = 0.5
        self.cmd_vel_pub.publish(cmd)
        self.get_logger().warn('检测到障碍物，执行避障')
    
    def navigate_to_goal(self):
        dx = self.goal_pose.pose.position.x - self.current_pose.position.x
        dy = self.goal_pose.pose.position.y - self.current_pose.position.y
        distance = math.sqrt(dx**2 + dy**2)
        
        q = self.current_pose.orientation
        _, _, current_yaw = euler_from_quaternion([q.x, q.y, q.z, q.w])
        
        target_yaw = math.atan2(dy, dx)
        angle_diff = self.normalize_angle(target_yaw - current_yaw)
        
        cmd = Twist()
        
        if abs(angle_diff) > 0.2:
            cmd.linear.x = 0.0
            cmd.angular.z = 1.0 * angle_diff
        else:
            cmd.linear.x = min(0.5, distance * 0.5)
            cmd.angular.z = 0.5 * angle_diff
        
        self.cmd_vel_pub.publish(cmd)
    
    def reached_goal(self):
        dx = self.goal_pose.pose.position.x - self.current_pose.position.x
        dy = self.goal_pose.pose.position.y - self.current_pose.position.y
        distance = math.sqrt(dx**2 + dy**2)
        
        return distance < self.goal_tolerance
    
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
    node = NavigationController()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
