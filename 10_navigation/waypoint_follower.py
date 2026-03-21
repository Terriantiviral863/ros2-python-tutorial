#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped, Twist
from nav_msgs.msg import Odometry, Path
from tf_transformations import euler_from_quaternion
import math


class WaypointFollower(Node):
    def __init__(self):
        super().__init__('waypoint_follower')
        
        self.odom_sub = self.create_subscription(
            Odometry,
            'odom',
            self.odom_callback,
            10
        )
        
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.path_pub = self.create_publisher(Path, 'waypoint_path', 10)
        
        self.timer = self.create_timer(0.1, self.control_loop)
        
        self.waypoints = [
            (2.0, 0.0),
            (2.0, 2.0),
            (0.0, 2.0),
            (0.0, 0.0)
        ]
        
        self.current_waypoint_idx = 0
        self.current_pose = None
        
        self.waypoint_tolerance = 0.2
        
        self.get_logger().info('航点跟随器已启动')
        self.get_logger().info(f'航点数量: {len(self.waypoints)}')
        
        self.publish_path()
    
    def odom_callback(self, msg):
        self.current_pose = msg.pose.pose
    
    def control_loop(self):
        if self.current_pose is None:
            return
        
        if self.current_waypoint_idx >= len(self.waypoints):
            self.stop_robot()
            self.get_logger().info('所有航点已完成！')
            return
        
        target_x, target_y = self.waypoints[self.current_waypoint_idx]
        
        dx = target_x - self.current_pose.position.x
        dy = target_y - self.current_pose.position.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance < self.waypoint_tolerance:
            self.current_waypoint_idx += 1
            self.get_logger().info(
                f'到达航点 {self.current_waypoint_idx}/{len(self.waypoints)}'
            )
            return
        
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
    
    def publish_path(self):
        path = Path()
        path.header.frame_id = "map"
        path.header.stamp = self.get_clock().now().to_msg()
        
        for wp in self.waypoints:
            pose = PoseStamped()
            pose.header.frame_id = "map"
            pose.pose.position.x = wp[0]
            pose.pose.position.y = wp[1]
            pose.pose.orientation.w = 1.0
            path.poses.append(pose)
        
        self.path_pub.publish(path)


def main(args=None):
    rclpy.init(args=args)
    node = WaypointFollower()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
