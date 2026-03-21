#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from custom_interfaces.srv import ComputeTrajectory, SetMode
from geometry_msgs.msg import Point
import math
import time


class AsyncServiceServer(Node):
    """异步服务服务器节点"""
    
    def __init__(self):
        super().__init__('async_service_server')
        
        # 创建服务
        self.trajectory_service = self.create_service(
            ComputeTrajectory,
            'compute_trajectory',
            self.compute_trajectory_callback
        )
        
        self.mode_service = self.create_service(
            SetMode,
            'set_mode',
            self.set_mode_callback
        )
        
        # 当前模式
        self.current_mode = 'MANUAL'
        
        self.get_logger().info('异步服务服务器已启动')
        self.get_logger().info('提供服务: /compute_trajectory, /set_mode')
    
    def compute_trajectory_callback(self, request, response):
        """计算轨迹服务回调"""
        self.get_logger().info(
            f'收到轨迹计算请求:'
            f'\n  起点: ({request.start.x:.2f}, {request.start.y:.2f})'
            f'\n  终点: ({request.goal.x:.2f}, {request.goal.y:.2f})'
            f'\n  最大速度: {request.max_velocity:.2f} m/s'
            f'\n  最大加速度: {request.max_acceleration:.2f} m/s²'
        )
        
        # 模拟计算时间
        time.sleep(1.0)
        
        # 计算距离
        dx = request.goal.x - request.start.x
        dy = request.goal.y - request.start.y
        distance = math.sqrt(dx * dx + dy * dy)
        
        # 生成简单的直线轨迹
        num_points = 10
        trajectory = []
        
        for i in range(num_points + 1):
            t = i / num_points
            point = Point()
            point.x = request.start.x + t * dx
            point.y = request.start.y + t * dy
            point.z = 0.0
            trajectory.append(point)
        
        # 估算时间 (简化的运动学计算)
        if request.max_velocity > 0:
            estimated_time = distance / request.max_velocity
        else:
            estimated_time = 0.0
        
        # 填充响应
        response.trajectory = trajectory
        response.total_distance = distance
        response.estimated_time = estimated_time
        response.success = True
        response.message = f'成功计算轨迹，共 {len(trajectory)} 个点'
        
        self.get_logger().info(
            f'轨迹计算完成:'
            f'\n  距离: {distance:.2f} m'
            f'\n  预计时间: {estimated_time:.2f} s'
            f'\n  轨迹点数: {len(trajectory)}'
        )
        
        return response
    
    def set_mode_callback(self, request, response):
        """设置模式服务回调"""
        self.get_logger().info(
            f'收到模式设置请求:'
            f'\n  目标模式: {request.mode}'
            f'\n  参数: {request.parameters}'
        )
        
        # 验证模式
        valid_modes = ['MANUAL', 'AUTO', 'EMERGENCY']
        
        if request.mode in valid_modes:
            old_mode = self.current_mode
            self.current_mode = request.mode
            
            response.success = True
            response.current_mode = self.current_mode
            response.message = f'模式已从 {old_mode} 切换到 {self.current_mode}'
            
            self.get_logger().info(f'✓ {response.message}')
        else:
            response.success = False
            response.current_mode = self.current_mode
            response.message = f'无效的模式: {request.mode}. 有效模式: {valid_modes}'
            
            self.get_logger().warn(f'✗ {response.message}')
        
        return response


def main(args=None):
    rclpy.init(args=args)
    
    node = AsyncServiceServer()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('服务器被用户中断')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
