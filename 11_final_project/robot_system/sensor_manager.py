#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan, Image, Imu
from std_msgs.msg import String
import json


class SensorManager(Node):
    def __init__(self):
        super().__init__('sensor_manager')
        
        self.laser_sub = self.create_subscription(
            LaserScan,
            'scan',
            self.laser_callback,
            10
        )
        
        self.camera_sub = self.create_subscription(
            Image,
            'camera/image_raw',
            self.camera_callback,
            10
        )
        
        self.imu_sub = self.create_subscription(
            Imu,
            'imu/data',
            self.imu_callback,
            10
        )
        
        self.sensor_status_pub = self.create_publisher(
            String,
            'sensor_status',
            10
        )
        
        self.timer = self.create_timer(1.0, self.publish_status)
        
        self.laser_data = None
        self.camera_data = None
        self.imu_data = None
        
        self.laser_count = 0
        self.camera_count = 0
        self.imu_count = 0
        
        self.get_logger().info('传感器管理器已启动')
    
    def laser_callback(self, msg):
        self.laser_data = msg
        self.laser_count += 1
        
        min_range = min([r for r in msg.ranges if msg.range_min < r < msg.range_max], default=msg.range_max)
        
        if min_range < 0.5:
            self.get_logger().warn(f'检测到近距离障碍物: {min_range:.2f}m')
    
    def camera_callback(self, msg):
        self.camera_data = msg
        self.camera_count += 1
    
    def imu_callback(self, msg):
        self.imu_data = msg
        self.imu_count += 1
    
    def publish_status(self):
        status = {
            'laser': {
                'active': self.laser_data is not None,
                'count': self.laser_count
            },
            'camera': {
                'active': self.camera_data is not None,
                'count': self.camera_count
            },
            'imu': {
                'active': self.imu_data is not None,
                'count': self.imu_count
            }
        }
        
        msg = String()
        msg.data = json.dumps(status)
        self.sensor_status_pub.publish(msg)
        
        self.get_logger().info(
            f'传感器状态 - 激光:{self.laser_count}, '
            f'相机:{self.camera_count}, IMU:{self.imu_count}'
        )


def main(args=None):
    rclpy.init(args=args)
    node = SensorManager()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
