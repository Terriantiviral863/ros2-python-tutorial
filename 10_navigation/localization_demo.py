#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseArray, Pose
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
import numpy as np


class LocalizationDemo(Node):
    def __init__(self):
        super().__init__('localization_demo')
        
        self.scan_sub = self.create_subscription(
            LaserScan,
            'scan',
            self.scan_callback,
            10
        )
        
        self.odom_sub = self.create_subscription(
            Odometry,
            'odom',
            self.odom_callback,
            10
        )
        
        self.particle_pub = self.create_publisher(PoseArray, 'particles', 10)
        
        self.num_particles = 500
        self.particles = self.initialize_particles()
        self.weights = np.ones(self.num_particles) / self.num_particles
        
        self.last_odom = None
        
        self.get_logger().info(f'定位演示已启动，粒子数: {self.num_particles}')
    
    def initialize_particles(self):
        particles = np.zeros((self.num_particles, 3))
        
        particles[:, 0] = np.random.uniform(-5, 5, self.num_particles)
        particles[:, 1] = np.random.uniform(-5, 5, self.num_particles)
        particles[:, 2] = np.random.uniform(-np.pi, np.pi, self.num_particles)
        
        return particles
    
    def odom_callback(self, msg):
        if self.last_odom is None:
            self.last_odom = msg
            return
        
        dx = msg.pose.pose.position.x - self.last_odom.pose.pose.position.x
        dy = msg.pose.pose.position.y - self.last_odom.pose.pose.position.y
        
        self.predict(dx, dy, 0.0)
        
        self.last_odom = msg
    
    def scan_callback(self, msg):
        self.update(msg)
        
        self.resample()
        
        self.publish_particles()
    
    def predict(self, dx, dy, dtheta):
        noise_std = 0.05
        
        for i in range(self.num_particles):
            self.particles[i, 0] += dx + np.random.normal(0, noise_std)
            self.particles[i, 1] += dy + np.random.normal(0, noise_std)
            self.particles[i, 2] += dtheta + np.random.normal(0, noise_std * 0.1)
    
    def update(self, scan):
        for i in range(self.num_particles):
            self.weights[i] = self.sensor_model(self.particles[i], scan)
        
        self.weights += 1e-300
        self.weights /= np.sum(self.weights)
    
    def sensor_model(self, particle, scan):
        likelihood = 1.0
        
        num_samples = 10
        step = len(scan.ranges) // num_samples
        
        for j in range(0, len(scan.ranges), step):
            if scan.ranges[j] < scan.range_min or scan.ranges[j] > scan.range_max:
                continue
            
            expected_range = 5.0
            
            diff = abs(scan.ranges[j] - expected_range)
            likelihood *= np.exp(-diff * diff / 2.0)
        
        return likelihood
    
    def resample(self):
        indices = np.random.choice(
            self.num_particles,
            self.num_particles,
            p=self.weights
        )
        
        self.particles = self.particles[indices]
        self.weights = np.ones(self.num_particles) / self.num_particles
    
    def publish_particles(self):
        pose_array = PoseArray()
        pose_array.header.frame_id = "map"
        pose_array.header.stamp = self.get_clock().now().to_msg()
        
        for i in range(self.num_particles):
            pose = Pose()
            pose.position.x = self.particles[i, 0]
            pose.position.y = self.particles[i, 1]
            pose.position.z = 0.0
            
            theta = self.particles[i, 2]
            pose.orientation.z = np.sin(theta / 2)
            pose.orientation.w = np.cos(theta / 2)
            
            pose_array.poses.append(pose)
        
        self.particle_pub.publish(pose_array)


def main(args=None):
    rclpy.init(args=args)
    node = LocalizationDemo()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
