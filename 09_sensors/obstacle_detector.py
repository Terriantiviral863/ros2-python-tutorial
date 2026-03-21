#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from visualization_msgs.msg import Marker, MarkerArray
from geometry_msgs.msg import Point
import math


class ObstacleDetector(Node):
    def __init__(self):
        super().__init__('obstacle_detector')
        
        self.subscription = self.create_subscription(
            LaserScan,
            'scan',
            self.scan_callback,
            10
        )
        
        self.marker_pub = self.create_publisher(MarkerArray, 'obstacles', 10)
        
        self.obstacle_threshold = 0.5
        
        self.get_logger().info('障碍物检测器已启动')
    
    def scan_callback(self, msg):
        obstacles = self.detect_obstacles(msg)
        
        self.visualize_obstacles(obstacles)
        
        if obstacles:
            self.get_logger().info(f'检测到 {len(obstacles)} 个障碍物')
    
    def detect_obstacles(self, scan):
        obstacles = []
        current_cluster = []
        
        for i, r in enumerate(scan.ranges):
            if scan.range_min < r < scan.range_max:
                angle = scan.angle_min + i * scan.angle_increment
                
                x = r * math.cos(angle)
                y = r * math.sin(angle)
                
                if not current_cluster:
                    current_cluster.append((x, y))
                else:
                    last_x, last_y = current_cluster[-1]
                    distance = math.sqrt((x - last_x)**2 + (y - last_y)**2)
                    
                    if distance < self.obstacle_threshold:
                        current_cluster.append((x, y))
                    else:
                        if len(current_cluster) > 3:
                            obstacles.append(current_cluster)
                        current_cluster = [(x, y)]
        
        if len(current_cluster) > 3:
            obstacles.append(current_cluster)
        
        return obstacles
    
    def visualize_obstacles(self, obstacles):
        marker_array = MarkerArray()
        
        for i, cluster in enumerate(obstacles):
            marker = Marker()
            marker.header.frame_id = "laser_link"
            marker.header.stamp = self.get_clock().now().to_msg()
            marker.ns = "obstacles"
            marker.id = i
            marker.type = Marker.LINE_STRIP
            marker.action = Marker.ADD
            
            marker.scale.x = 0.05
            
            marker.color.r = 1.0
            marker.color.g = 0.0
            marker.color.b = 0.0
            marker.color.a = 1.0
            
            for x, y in cluster:
                p = Point()
                p.x = x
                p.y = y
                p.z = 0.0
                marker.points.append(p)
            
            marker_array.markers.append(marker)
        
        self.marker_pub.publish(marker_array)


def main(args=None):
    rclpy.init(args=args)
    node = ObstacleDetector()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
