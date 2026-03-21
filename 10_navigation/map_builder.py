#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import OccupancyGrid, Odometry
from tf_transformations import euler_from_quaternion
import numpy as np
import math


class MapBuilder(Node):
    def __init__(self):
        super().__init__('map_builder')
        
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
        
        self.map_pub = self.create_publisher(OccupancyGrid, 'map', 10)
        
        self.map_width = 200
        self.map_height = 200
        self.resolution = 0.05
        
        self.map_data = np.zeros((self.map_height, self.map_width), dtype=np.int8)
        
        self.robot_x = 0.0
        self.robot_y = 0.0
        self.robot_theta = 0.0
        
        self.timer = self.create_timer(1.0, self.publish_map)
        
        self.get_logger().info('地图构建器已启动')
    
    def odom_callback(self, msg):
        self.robot_x = msg.pose.pose.position.x
        self.robot_y = msg.pose.pose.position.y
        
        q = msg.pose.pose.orientation
        _, _, self.robot_theta = euler_from_quaternion([q.x, q.y, q.z, q.w])
    
    def scan_callback(self, msg):
        for i, r in enumerate(msg.ranges):
            if r < msg.range_min or r > msg.range_max:
                continue
            
            angle = msg.angle_min + i * msg.angle_increment
            
            world_angle = self.robot_theta + angle
            
            obstacle_x = self.robot_x + r * math.cos(world_angle)
            obstacle_y = self.robot_y + r * math.sin(world_angle)
            
            grid_x, grid_y = self.world_to_grid(obstacle_x, obstacle_y)
            
            if self.is_valid_cell(grid_x, grid_y):
                self.map_data[grid_y, grid_x] = 100
            
            robot_grid_x, robot_grid_y = self.world_to_grid(self.robot_x, self.robot_y)
            self.bresenham(robot_grid_x, robot_grid_y, grid_x, grid_y)
    
    def bresenham(self, x0, y0, x1, y1):
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        
        x, y = x0, y0
        
        while True:
            if self.is_valid_cell(x, y):
                if self.map_data[y, x] != 100:
                    self.map_data[y, x] = 0
            
            if x == x1 and y == y1:
                break
            
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy
    
    def world_to_grid(self, x, y):
        grid_x = int((x / self.resolution) + self.map_width // 2)
        grid_y = int((y / self.resolution) + self.map_height // 2)
        return grid_x, grid_y
    
    def is_valid_cell(self, x, y):
        return 0 <= x < self.map_width and 0 <= y < self.map_height
    
    def publish_map(self):
        grid = OccupancyGrid()
        
        grid.header.frame_id = "map"
        grid.header.stamp = self.get_clock().now().to_msg()
        
        grid.info.resolution = self.resolution
        grid.info.width = self.map_width
        grid.info.height = self.map_height
        
        grid.info.origin.position.x = -self.map_width * self.resolution / 2
        grid.info.origin.position.y = -self.map_height * self.resolution / 2
        grid.info.origin.position.z = 0.0
        grid.info.origin.orientation.w = 1.0
        
        grid.data = self.map_data.flatten().tolist()
        
        self.map_pub.publish(grid)


def main(args=None):
    rclpy.init(args=args)
    node = MapBuilder()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
