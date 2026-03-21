#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Path, OccupancyGrid
import heapq
import math


class PathPlanner(Node):
    def __init__(self):
        super().__init__('path_planner')
        
        self.goal_sub = self.create_subscription(
            PoseStamped,
            'goal_pose',
            self.goal_callback,
            10
        )
        
        self.map_sub = self.create_subscription(
            OccupancyGrid,
            'map',
            self.map_callback,
            10
        )
        
        self.path_pub = self.create_publisher(Path, 'planned_path', 10)
        
        self.map = None
        self.start = (0, 0)
        
        self.get_logger().info('路径规划器已启动')
    
    def map_callback(self, msg):
        self.map = msg
    
    def goal_callback(self, msg):
        if self.map is None:
            self.get_logger().warn('地图未加载')
            return
        
        goal_x = msg.pose.position.x
        goal_y = msg.pose.position.y
        
        goal = self.world_to_grid(goal_x, goal_y)
        
        self.get_logger().info(f'规划路径: {self.start} -> {goal}')
        
        path_grid = self.a_star(self.start, goal)
        
        if path_grid:
            path_msg = self.grid_path_to_msg(path_grid)
            self.path_pub.publish(path_msg)
            self.get_logger().info(f'路径规划成功，长度: {len(path_grid)}')
        else:
            self.get_logger().warn('路径规划失败')
    
    def a_star(self, start, goal):
        open_set = []
        heapq.heappush(open_set, (0, start))
        
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}
        
        while open_set:
            current = heapq.heappop(open_set)[1]
            
            if current == goal:
                return self.reconstruct_path(came_from, current)
            
            for neighbor in self.get_neighbors(current):
                if not self.is_free(neighbor):
                    continue
                
                tentative_g = g_score[current] + self.distance(current, neighbor)
                
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + self.heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
        
        return None
    
    def heuristic(self, a, b):
        return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)
    
    def distance(self, a, b):
        return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)
    
    def get_neighbors(self, pos):
        x, y = pos
        neighbors = []
        
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                
                nx, ny = x + dx, y + dy
                
                if 0 <= nx < self.map.info.width and 0 <= ny < self.map.info.height:
                    neighbors.append((nx, ny))
        
        return neighbors
    
    def is_free(self, pos):
        x, y = pos
        index = y * self.map.info.width + x
        
        if index >= len(self.map.data):
            return False
        
        return self.map.data[index] < 50
    
    def reconstruct_path(self, came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path
    
    def world_to_grid(self, x, y):
        grid_x = int((x - self.map.info.origin.position.x) / self.map.info.resolution)
        grid_y = int((y - self.map.info.origin.position.y) / self.map.info.resolution)
        return (grid_x, grid_y)
    
    def grid_to_world(self, grid_x, grid_y):
        x = grid_x * self.map.info.resolution + self.map.info.origin.position.x
        y = grid_y * self.map.info.resolution + self.map.info.origin.position.y
        return (x, y)
    
    def grid_path_to_msg(self, path_grid):
        path_msg = Path()
        path_msg.header.frame_id = "map"
        path_msg.header.stamp = self.get_clock().now().to_msg()
        
        for grid_pos in path_grid:
            pose = PoseStamped()
            pose.header.frame_id = "map"
            
            x, y = self.grid_to_world(grid_pos[0], grid_pos[1])
            pose.pose.position.x = x
            pose.pose.position.y = y
            pose.pose.orientation.w = 1.0
            
            path_msg.poses.append(pose)
        
        return path_msg


def main(args=None):
    rclpy.init(args=args)
    node = PathPlanner()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
