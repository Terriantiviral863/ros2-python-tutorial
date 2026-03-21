#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import math
import random


class LaserScanSimulator(Node):
    def __init__(self):
        super().__init__('laser_scan_simulator')
        
        self.publisher = self.create_publisher(LaserScan, 'scan', 10)
        
        self.timer = self.create_timer(0.1, self.timer_callback)
        
        self.angle = 0.0
        
        self.get_logger().info('激光雷达模拟器已启动')
        self.get_logger().info('在RViz中添加LaserScan显示，话题: /scan')
    
    def timer_callback(self):
        scan = LaserScan()
        
        scan.header.stamp = self.get_clock().now().to_msg()
        scan.header.frame_id = "laser_link"
        
        scan.angle_min = -math.pi
        scan.angle_max = math.pi
        scan.angle_increment = math.pi / 180.0
        scan.time_increment = 0.0
        scan.scan_time = 0.1
        
        scan.range_min = 0.1
        scan.range_max = 10.0
        
        num_readings = int((scan.angle_max - scan.angle_min) / scan.angle_increment)
        
        scan.ranges = []
        scan.intensities = []
        
        for i in range(num_readings):
            angle = scan.angle_min + i * scan.angle_increment
            
            distance = 5.0
            
            if -0.5 < angle < 0.5:
                distance = 2.0 + 0.5 * math.sin(self.angle * 2)
            elif 0.5 < angle < 1.5:
                distance = 3.0
            elif -1.5 < angle < -0.5:
                distance = 4.0
            
            noise = random.uniform(-0.05, 0.05)
            distance += noise
            
            scan.ranges.append(distance)
            scan.intensities.append(100.0)
        
        self.publisher.publish(scan)
        
        self.angle += 0.05


def main(args=None):
    rclpy.init(args=args)
    node = LaserScanSimulator()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
