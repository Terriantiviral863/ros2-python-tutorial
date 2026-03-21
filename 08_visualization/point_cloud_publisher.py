#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2, PointField
from std_msgs.msg import Header
import numpy as np
import struct


class PointCloudPublisher(Node):
    def __init__(self):
        super().__init__('point_cloud_publisher')
        
        self.publisher = self.create_publisher(PointCloud2, 'point_cloud', 10)
        
        self.timer = self.create_timer(0.1, self.timer_callback)
        
        self.counter = 0
        
        self.get_logger().info('点云发布器已启动')
        self.get_logger().info('在RViz中添加PointCloud2显示，话题: /point_cloud')
    
    def timer_callback(self):
        cloud_msg = self.create_point_cloud()
        self.publisher.publish(cloud_msg)
        
        self.counter += 1
    
    def create_point_cloud(self):
        header = Header()
        header.frame_id = "base_link"
        header.stamp = self.get_clock().now().to_msg()
        
        fields = [
            PointField(name='x', offset=0, datatype=PointField.FLOAT32, count=1),
            PointField(name='y', offset=4, datatype=PointField.FLOAT32, count=1),
            PointField(name='z', offset=8, datatype=PointField.FLOAT32, count=1),
            PointField(name='rgb', offset=12, datatype=PointField.UINT32, count=1),
        ]
        
        points = []
        num_points = 1000
        
        for i in range(num_points):
            angle = (i / num_points) * 2 * np.pi
            radius = 2.0 + 0.5 * np.sin(self.counter * 0.05 + angle * 3)
            
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            z = 0.5 * np.sin(angle * 5 + self.counter * 0.1)
            
            r = int(255 * (np.sin(angle) + 1) / 2)
            g = int(255 * (np.cos(angle) + 1) / 2)
            b = int(255 * (np.sin(self.counter * 0.05) + 1) / 2)
            
            rgb = (r << 16) | (g << 8) | b
            
            points.append(struct.pack('fffI', x, y, z, rgb))
        
        cloud_msg = PointCloud2()
        cloud_msg.header = header
        cloud_msg.height = 1
        cloud_msg.width = num_points
        cloud_msg.fields = fields
        cloud_msg.is_bigendian = False
        cloud_msg.point_step = 16
        cloud_msg.row_step = cloud_msg.point_step * num_points
        cloud_msg.is_dense = True
        cloud_msg.data = b''.join(points)
        
        return cloud_msg


def main(args=None):
    rclpy.init(args=args)
    node = PointCloudPublisher()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
