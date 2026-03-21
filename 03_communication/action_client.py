#!/usr/bin/env python3

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from custom_interfaces.action import Fibonacci
import sys


class FibonacciActionClient(Node):
    """斐波那契动作客户端"""
    
    def __init__(self):
        super().__init__('fibonacci_action_client')
        
        # 创建动作客户端
        self.action_client = ActionClient(
            self,
            Fibonacci,
            'fibonacci'
        )
        
        self.get_logger().info('斐波那契动作客户端已启动')
    
    def send_goal(self, order):
        """发送目标"""
        self.get_logger().info(f'等待动作服务器...')
        self.action_client.wait_for_server()
        
        # 创建目标
        goal_msg = Fibonacci.Goal()
        goal_msg.order = order
        
        self.get_logger().info(f'发送目标: 计算斐波那契数列 (阶数={order})')
        
        # 发送目标并设置回调
        self.send_goal_future = self.action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )
        
        self.send_goal_future.add_done_callback(self.goal_response_callback)
    
    def goal_response_callback(self, future):
        """处理目标响应"""
        goal_handle = future.result()
        
        if not goal_handle.accepted:
            self.get_logger().error('✗ 目标被拒绝')
            return
        
        self.get_logger().info('✓ 目标被接受')
        
        # 获取结果
        self.result_future = goal_handle.get_result_async()
        self.result_future.add_done_callback(self.get_result_callback)
    
    def feedback_callback(self, feedback_msg):
        """处理反馈"""
        feedback = feedback_msg.feedback
        self.get_logger().info(
            f'收到反馈: 当前序列长度={len(feedback.partial_sequence)}, '
            f'最新值={feedback.partial_sequence[-1] if feedback.partial_sequence else 0}'
        )
    
    def get_result_callback(self, future):
        """处理结果"""
        result = future.result().result
        status = future.result().status
        
        if status == 4:  # SUCCEEDED
            self.get_logger().info(
                f'✓ 动作成功完成!'
                f'\n  最终序列: {result.sequence}'
                f'\n  序列长度: {len(result.sequence)}'
            )
        elif status == 5:  # CANCELED
            self.get_logger().warn('动作被取消')
        else:
            self.get_logger().error(f'动作失败，状态码: {status}')
        
        # 完成后关闭节点
        rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)
    
    node = FibonacciActionClient()
    
    # 从命令行参数获取阶数，默认为10
    order = 10
    if len(sys.argv) > 1:
        try:
            order = int(sys.argv[1])
        except ValueError:
            node.get_logger().error('无效的阶数参数，使用默认值10')
    
    node.send_goal(order)
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('客户端被用户中断')
    finally:
        node.destroy_node()


if __name__ == '__main__':
    main()
