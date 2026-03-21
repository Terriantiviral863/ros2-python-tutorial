#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import numpy as np


class ObstacleAvoider(Node):
    def __init__(self):
        super().__init__('obstacle_avoider')
        
        self.scan_sub = self.create_subscription(
            LaserScan,
            'scan',
            self.scan_callback,
            10
        )
        
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        
        self.safe_distance = 0.5
        self.warning_distance = 1.0
        
        self.get_logger().info('避障控制器已启动')
    
    def scan_callback(self, msg):
        cmd = self.compute_avoidance_velocity(msg)
        self.cmd_vel_pub.publish(cmd)
    
    def compute_avoidance_velocity(self, scan):
        ranges = np.array(scan.ranges)
        ranges[np.isinf(ranges)] = scan.range_max
        ranges[np.isnan(ranges)] = scan.range_max
        
        num_sectors = 5
        sector_size = len(ranges) // num_sectors
        
        sector_mins = []
        for i in range(num_sectors):
            start = i * sector_size
            end = (i + 1) * sector_size
            sector_min = np.min(ranges[start:end])
            sector_mins.append(sector_min)
        
        left = sector_mins[0]
        front_left = sector_mins[1]
        front = sector_mins[2]
        front_right = sector_mins[3]
        right = sector_mins[4]
        
        cmd = Twist()
        
        if front < self.safe_distance:
            cmd.linear.x = 0.0
            
            if left > right:
                cmd.angular.z = 0.8
                self.get_logger().info('前方障碍，左转')
            else:
                cmd.angular.z = -0.8
                self.get_logger().info('前方障碍，右转')
        
        elif front < self.warning_distance:
            cmd.linear.x = 0.1
            
            if front_left < front_right:
                cmd.angular.z = -0.3
            else:
                cmd.angular.z = 0.3
            
            self.get_logger().info('减速避障')
        
        else:
            cmd.linear.x = 0.3
            cmd.angular.z = 0.0
        
        return cmd


def main(args=None):
    rclpy.init(args=args)
    node = ObstacleAvoider()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
