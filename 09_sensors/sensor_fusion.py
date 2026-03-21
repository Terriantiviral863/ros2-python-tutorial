#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped
from tf_transformations import euler_from_quaternion, quaternion_from_euler
import numpy as np


class SensorFusion(Node):
    def __init__(self):
        super().__init__('sensor_fusion')
        
        self.imu_sub = self.create_subscription(Imu, 'imu/data', self.imu_callback, 10)
        self.odom_sub = self.create_subscription(Odometry, 'odom', self.odom_callback, 10)
        
        self.pose_pub = self.create_publisher(PoseStamped, 'fused_pose', 10)
        
        self.x = np.zeros((6, 1))
        self.P = np.eye(6) * 0.1
        
        self.last_time = None
        
        self.get_logger().info('传感器融合节点已启动')
    
    def imu_callback(self, msg):
        current_time = self.get_clock().now()
        
        if self.last_time is None:
            self.last_time = current_time
            return
        
        dt = (current_time - self.last_time).nanoseconds / 1e9
        self.last_time = current_time
        
        q = [msg.orientation.x, msg.orientation.y, msg.orientation.z, msg.orientation.w]
        roll, pitch, yaw = euler_from_quaternion(q)
        
        self.predict(dt)
        
        z = np.array([[yaw]])
        self.update_imu(z)
    
    def odom_callback(self, msg):
        z = np.array([
            [msg.pose.pose.position.x],
            [msg.pose.pose.position.y]
        ])
        
        self.update_odom(z)
        
        self.publish_fused_pose()
    
    def predict(self, dt):
        F = np.eye(6)
        F[0, 3] = dt
        F[1, 4] = dt
        F[2, 5] = dt
        
        self.x = F @ self.x
        
        Q = np.eye(6) * 0.01
        self.P = F @ self.P @ F.T + Q
    
    def update_imu(self, z):
        H = np.zeros((1, 6))
        H[0, 2] = 1.0
        
        R = np.array([[0.1]])
        
        y = z - H @ self.x
        S = H @ self.P @ H.T + R
        K = self.P @ H.T @ np.linalg.inv(S)
        
        self.x = self.x + K @ y
        self.P = (np.eye(6) - K @ H) @ self.P
    
    def update_odom(self, z):
        H = np.zeros((2, 6))
        H[0, 0] = 1.0
        H[1, 1] = 1.0
        
        R = np.eye(2) * 0.05
        
        y = z - H @ self.x
        S = H @ self.P @ H.T + R
        K = self.P @ H.T @ np.linalg.inv(S)
        
        self.x = self.x + K @ y
        self.P = (np.eye(6) - K @ H) @ self.P
    
    def publish_fused_pose(self):
        pose = PoseStamped()
        pose.header.stamp = self.get_clock().now().to_msg()
        pose.header.frame_id = "map"
        
        pose.pose.position.x = float(self.x[0, 0])
        pose.pose.position.y = float(self.x[1, 0])
        pose.pose.position.z = 0.0
        
        yaw = float(self.x[2, 0])
        q = quaternion_from_euler(0, 0, yaw)
        pose.pose.orientation.x = q[0]
        pose.pose.orientation.y = q[1]
        pose.pose.orientation.z = q[2]
        pose.pose.orientation.w = q[3]
        
        self.pose_pub.publish(pose)


def main(args=None):
    rclpy.init(args=args)
    node = SensorFusion()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
