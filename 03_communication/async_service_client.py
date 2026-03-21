#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from custom_interfaces.srv import ComputeTrajectory, SetMode
from geometry_msgs.msg import Point
import sys


class AsyncServiceClient(Node):
    """异步服务客户端节点"""
    
    def __init__(self):
        super().__init__('async_service_client')
        
        # 创建客户端
        self.trajectory_client = self.create_client(
            ComputeTrajectory,
            'compute_trajectory'
        )
        
        self.mode_client = self.create_client(
            SetMode,
            'set_mode'
        )
        
        self.get_logger().info('异步服务客户端已启动')
    
    def wait_for_services(self, timeout_sec=5.0):
        """等待服务可用"""
        self.get_logger().info('等待服务可用...')
        
        trajectory_ready = self.trajectory_client.wait_for_service(timeout_sec=timeout_sec)
        mode_ready = self.mode_client.wait_for_service(timeout_sec=timeout_sec)
        
        if not trajectory_ready:
            self.get_logger().error('轨迹计算服务不可用')
            return False
        
        if not mode_ready:
            self.get_logger().error('模式设置服务不可用')
            return False
        
        self.get_logger().info('所有服务已就绪')
        return True
    
    async def call_compute_trajectory(self, start_x, start_y, goal_x, goal_y):
        """调用轨迹计算服务"""
        request = ComputeTrajectory.Request()
        request.start = Point(x=start_x, y=start_y, z=0.0)
        request.goal = Point(x=goal_x, y=goal_y, z=0.0)
        request.max_velocity = 1.0
        request.max_acceleration = 0.5
        
        self.get_logger().info(
            f'调用轨迹计算服务:'
            f'\n  起点: ({start_x}, {start_y})'
            f'\n  终点: ({goal_x}, {goal_y})'
        )
        
        try:
            future = self.trajectory_client.call_async(request)
            response = await future
            
            if response.success:
                self.get_logger().info(
                    f'✓ 轨迹计算成功:'
                    f'\n  距离: {response.total_distance:.2f} m'
                    f'\n  预计时间: {response.estimated_time:.2f} s'
                    f'\n  轨迹点数: {len(response.trajectory)}'
                    f'\n  消息: {response.message}'
                )
                
                # 显示部分轨迹点
                self.get_logger().info('轨迹点 (前5个):')
                for i, point in enumerate(response.trajectory[:5]):
                    self.get_logger().info(f'  [{i}] ({point.x:.2f}, {point.y:.2f})')
            else:
                self.get_logger().error(f'✗ 轨迹计算失败: {response.message}')
            
            return response
            
        except Exception as e:
            self.get_logger().error(f'服务调用异常: {str(e)}')
            return None
    
    async def call_set_mode(self, mode, parameters=None):
        """调用模式设置服务"""
        request = SetMode.Request()
        request.mode = mode
        request.parameters = parameters if parameters else []
        
        self.get_logger().info(f'调用模式设置服务: {mode}')
        
        try:
            future = self.mode_client.call_async(request)
            response = await future
            
            if response.success:
                self.get_logger().info(
                    f'✓ 模式设置成功:'
                    f'\n  当前模式: {response.current_mode}'
                    f'\n  消息: {response.message}'
                )
            else:
                self.get_logger().warn(
                    f'✗ 模式设置失败:'
                    f'\n  当前模式: {response.current_mode}'
                    f'\n  消息: {response.message}'
                )
            
            return response
            
        except Exception as e:
            self.get_logger().error(f'服务调用异常: {str(e)}')
            return None


async def main_async():
    """异步主函数"""
    rclpy.init()
    
    node = AsyncServiceClient()
    
    try:
        # 等待服务可用
        if not node.wait_for_services():
            node.get_logger().error('服务不可用，退出')
            return
        
        # 测试1: 设置模式为AUTO
        await node.call_set_mode('AUTO', ['param1', 'param2'])
        
        # 测试2: 计算轨迹
        await node.call_compute_trajectory(0.0, 0.0, 5.0, 5.0)
        
        # 测试3: 设置模式为EMERGENCY
        await node.call_set_mode('EMERGENCY')
        
        # 测试4: 尝试设置无效模式
        await node.call_set_mode('INVALID_MODE')
        
        # 测试5: 计算另一条轨迹
        await node.call_compute_trajectory(1.0, 2.0, 10.0, 8.0)
        
        node.get_logger().info('所有测试完成')
        
    except KeyboardInterrupt:
        node.get_logger().info('客户端被用户中断')
    finally:
        node.destroy_node()
        rclpy.shutdown()


def main(args=None):
    """主函数入口"""
    import asyncio
    asyncio.run(main_async())


if __name__ == '__main__':
    main()
