#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from visualization_msgs.msg import Marker, MarkerArray
from geometry_msgs.msg import Point
import math


class RVizMarkerPublisher(Node):
    def __init__(self):
        super().__init__('rviz_marker_publisher')
        
        self.marker_pub = self.create_publisher(Marker, 'visualization_marker', 10)
        self.marker_array_pub = self.create_publisher(MarkerArray, 'visualization_marker_array', 10)
        
        self.timer = self.create_timer(0.1, self.timer_callback)
        
        self.counter = 0
        
        self.get_logger().info('RViz Marker发布器已启动')
        self.get_logger().info('在RViz中添加Marker显示，话题: /visualization_marker')
    
    def timer_callback(self):
        self.publish_sphere()
        self.publish_cube()
        self.publish_arrow()
        self.publish_line_strip()
        self.publish_text()
        self.publish_marker_array()
        
        self.counter += 1
    
    def publish_sphere(self):
        marker = Marker()
        marker.header.frame_id = "base_link"
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.ns = "basic_shapes"
        marker.id = 0
        marker.type = Marker.SPHERE
        marker.action = Marker.ADD
        
        marker.pose.position.x = 1.0
        marker.pose.position.y = 0.0
        marker.pose.position.z = 0.0
        marker.pose.orientation.w = 1.0
        
        marker.scale.x = 0.3
        marker.scale.y = 0.3
        marker.scale.z = 0.3
        
        marker.color.r = 1.0
        marker.color.g = 0.0
        marker.color.b = 0.0
        marker.color.a = 1.0
        
        marker.lifetime = rclpy.duration.Duration(seconds=0).to_msg()
        
        self.marker_pub.publish(marker)
    
    def publish_cube(self):
        marker = Marker()
        marker.header.frame_id = "base_link"
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.ns = "basic_shapes"
        marker.id = 1
        marker.type = Marker.CUBE
        marker.action = Marker.ADD
        
        marker.pose.position.x = 0.0
        marker.pose.position.y = 1.0
        marker.pose.position.z = 0.0
        marker.pose.orientation.w = 1.0
        
        marker.scale.x = 0.4
        marker.scale.y = 0.4
        marker.scale.z = 0.4
        
        marker.color.r = 0.0
        marker.color.g = 1.0
        marker.color.b = 0.0
        marker.color.a = 0.8
        
        self.marker_pub.publish(marker)
    
    def publish_arrow(self):
        marker = Marker()
        marker.header.frame_id = "base_link"
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.ns = "basic_shapes"
        marker.id = 2
        marker.type = Marker.ARROW
        marker.action = Marker.ADD
        
        angle = self.counter * 0.05
        marker.pose.position.x = 0.0
        marker.pose.position.y = 0.0
        marker.pose.position.z = 0.5
        marker.pose.orientation.z = math.sin(angle / 2)
        marker.pose.orientation.w = math.cos(angle / 2)
        
        marker.scale.x = 0.5
        marker.scale.y = 0.05
        marker.scale.z = 0.05
        
        marker.color.r = 0.0
        marker.color.g = 0.0
        marker.color.b = 1.0
        marker.color.a = 1.0
        
        self.marker_pub.publish(marker)
    
    def publish_line_strip(self):
        marker = Marker()
        marker.header.frame_id = "base_link"
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.ns = "lines"
        marker.id = 3
        marker.type = Marker.LINE_STRIP
        marker.action = Marker.ADD
        
        marker.scale.x = 0.02
        
        marker.color.r = 1.0
        marker.color.g = 1.0
        marker.color.b = 0.0
        marker.color.a = 1.0
        
        for i in range(100):
            p = Point()
            p.x = i * 0.02
            p.y = math.sin(i * 0.1)
            p.z = 0.0
            marker.points.append(p)
        
        self.marker_pub.publish(marker)
    
    def publish_text(self):
        marker = Marker()
        marker.header.frame_id = "base_link"
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.ns = "text"
        marker.id = 4
        marker.type = Marker.TEXT_VIEW_FACING
        marker.action = Marker.ADD
        
        marker.pose.position.x = 0.0
        marker.pose.position.y = 0.0
        marker.pose.position.z = 1.0
        marker.pose.orientation.w = 1.0
        
        marker.scale.z = 0.2
        
        marker.color.r = 1.0
        marker.color.g = 1.0
        marker.color.b = 1.0
        marker.color.a = 1.0
        
        marker.text = f"ROS2 Marker Demo {self.counter}"
        
        self.marker_pub.publish(marker)
    
    def publish_marker_array(self):
        marker_array = MarkerArray()
        
        for i in range(5):
            marker = Marker()
            marker.header.frame_id = "base_link"
            marker.header.stamp = self.get_clock().now().to_msg()
            marker.ns = "sphere_array"
            marker.id = i + 10
            marker.type = Marker.SPHERE
            marker.action = Marker.ADD
            
            angle = (self.counter * 0.05) + (i * 2 * math.pi / 5)
            marker.pose.position.x = 2.0 * math.cos(angle)
            marker.pose.position.y = 2.0 * math.sin(angle)
            marker.pose.position.z = 0.0
            marker.pose.orientation.w = 1.0
            
            marker.scale.x = 0.2
            marker.scale.y = 0.2
            marker.scale.z = 0.2
            
            marker.color.r = float(i) / 5.0
            marker.color.g = 1.0 - float(i) / 5.0
            marker.color.b = 0.5
            marker.color.a = 1.0
            
            marker_array.markers.append(marker)
        
        self.marker_array_pub.publish(marker_array)


def main(args=None):
    rclpy.init(args=args)
    node = RVizMarkerPublisher()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
