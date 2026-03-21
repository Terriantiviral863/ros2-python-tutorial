#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from nav_msgs.msg import OccupancyGrid
import numpy as np


class GridMapVisualizer(Node):
    def __init__(self):
        super().__init__('grid_map_visualizer')
        
        self.publisher = self.create_publisher(OccupancyGrid, 'map', 10)
        
        self.timer = self.create_timer(1.0, self.timer_callback)
        
        self.width = 100
        self.height = 100
        self.resolution = 0.1
        
        self.get_logger().info('栅格地图可视化器已启动')
        self.get_logger().info('在RViz中添加Map显示，话题: /map')
    
    def timer_callback(self):
        grid = OccupancyGrid()
        
        grid.header.frame_id = "map"
        grid.header.stamp = self.get_clock().now().to_msg()
        
        grid.info.resolution = self.resolution
        grid.info.width = self.width
        grid.info.height = self.height
        grid.info.origin.position.x = -self.width * self.resolution / 2
        grid.info.origin.position.y = -self.height * self.resolution / 2
        grid.info.origin.position.z = 0.0
        grid.info.origin.orientation.w = 1.0
        
        data = np.zeros((self.height, self.width), dtype=np.int8)
        
        for i in range(self.height):
            for j in range(self.width):
                if i < 10 or i >= self.height - 10 or j < 10 or j >= self.width - 10:
                    data[i, j] = 100
                elif (i - 50) ** 2 + (j - 50) ** 2 < 400:
                    data[i, j] = 100
                else:
                    data[i, j] = 0
        
        grid.data = data.flatten().tolist()
        
        self.publisher.publish(grid)


def main(args=None):
    rclpy.init(args=args)
    node = GridMapVisualizer()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
