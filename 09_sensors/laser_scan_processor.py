#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import math


class LaserScanProcessor(Node):
    def __init__(self):
        super().__init__('laser_scan_processor')
        
        self.subscription = self.create_subscription(
            LaserScan,
            'scan',
            self.scan_callback,
            10
        )
        
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        
        self.get_logger().info('激光雷达处理器已启动')
    
    def scan_callback(self, msg):
        min_distance = float('inf')
        min_angle = 0.0
        
        for i, r in enumerate(msg.ranges):
            if msg.range_min < r < msg.range_max:
                if r < min_distance:
                    min_distance = r
                    min_angle = msg.angle_min + i * msg.angle_increment
        
        self.get_logger().info(
            f'最近障碍物: 距离={min_distance:.2f}m, '
            f'角度={math.degrees(min_angle):.1f}°'
        )
        
        front_ranges = []
        num_readings = len(msg.ranges)
        front_start = num_readings // 2 - 30
        front_end = num_readings // 2 + 30
        
        for i in range(front_start, front_end):
            if i >= 0 and i < num_readings:
                r = msg.ranges[i]
                if msg.range_min < r < msg.range_max:
                    front_ranges.append(r)
        
        if front_ranges:
            avg_front_distance = sum(front_ranges) / len(front_ranges)
            
            cmd = Twist()
            
            if avg_front_distance < 1.0:
                cmd.linear.x = 0.0
                cmd.angular.z = 0.5
                self.get_logger().warn('前方有障碍物，转向')
            elif avg_front_distance < 2.0:
                cmd.linear.x = 0.1
                cmd.angular.z = 0.0
                self.get_logger().info('减速前进')
            else:
                cmd.linear.x = 0.3
                cmd.angular.z = 0.0
            
            self.cmd_vel_pub.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = LaserScanProcessor()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
