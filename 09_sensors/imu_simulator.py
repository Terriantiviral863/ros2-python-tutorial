#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from tf_transformations import quaternion_from_euler
import math
import random


class ImuSimulator(Node):
    def __init__(self):
        super().__init__('imu_simulator')
        
        self.publisher = self.create_publisher(Imu, 'imu/data', 10)
        
        self.timer = self.create_timer(0.01, self.timer_callback)
        
        self.roll = 0.0
        self.pitch = 0.0
        self.yaw = 0.0
        
        self.angular_velocity_z = 0.1
        
        self.get_logger().info('IMU模拟器已启动')
        self.get_logger().info('发布IMU数据到: /imu/data')
    
    def timer_callback(self):
        imu = Imu()
        
        imu.header.stamp = self.get_clock().now().to_msg()
        imu.header.frame_id = "imu_link"
        
        self.yaw += self.angular_velocity_z * 0.01
        if self.yaw > math.pi:
            self.yaw -= 2 * math.pi
        
        self.roll = 0.1 * math.sin(self.yaw * 2)
        self.pitch = 0.05 * math.cos(self.yaw * 3)
        
        q = quaternion_from_euler(self.roll, self.pitch, self.yaw)
        imu.orientation.x = q[0]
        imu.orientation.y = q[1]
        imu.orientation.z = q[2]
        imu.orientation.w = q[3]
        
        imu.angular_velocity.x = random.gauss(0, 0.01)
        imu.angular_velocity.y = random.gauss(0, 0.01)
        imu.angular_velocity.z = self.angular_velocity_z + random.gauss(0, 0.01)
        
        imu.linear_acceleration.x = random.gauss(0, 0.1)
        imu.linear_acceleration.y = random.gauss(0, 0.1)
        imu.linear_acceleration.z = 9.81 + random.gauss(0, 0.1)
        
        for i in range(9):
            imu.orientation_covariance[i] = 0.0
            imu.angular_velocity_covariance[i] = 0.0
            imu.linear_acceleration_covariance[i] = 0.0
        
        imu.orientation_covariance[0] = 0.01
        imu.orientation_covariance[4] = 0.01
        imu.orientation_covariance[8] = 0.01
        
        self.publisher.publish(imu)


def main(args=None):
    rclpy.init(args=args)
    node = ImuSimulator()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
