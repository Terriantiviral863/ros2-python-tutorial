#!/usr/bin/env python3

import rclpy
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.node import Node
from rclpy.callback_groups import ReentrantCallbackGroup
from custom_interfaces.action import Fibonacci
import time


class FibonacciActionServer(Node):
    """斐波那契动作服务器"""
    
    def __init__(self):
        super().__init__('fibonacci_action_server')
        
        # 使用可重入回调组以支持并发
        self.callback_group = ReentrantCallbackGroup()
        
        # 创建动作服务器
        self.action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            execute_callback=self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback,
            callback_group=self.callback_group
        )
        
        self.get_logger().info('斐波那契动作服务器已启动')
        self.get_logger().info('等待动作目标...')
    
    def goal_callback(self, goal_request):
        """处理新的目标请求"""
        self.get_logger().info(f'收到目标请求: 计算斐波那契数列，阶数={goal_request.order}')
        
        # 验证目标
        if goal_request.order < 0:
            self.get_logger().warn('拒绝目标: 阶数不能为负数')
            return GoalResponse.REJECT
        
        if goal_request.order > 50:
            self.get_logger().warn('拒绝目标: 阶数过大 (最大50)')
            return GoalResponse.REJECT
        
        self.get_logger().info('接受目标')
        return GoalResponse.ACCEPT
    
    def cancel_callback(self, goal_handle):
        """处理取消请求"""
        self.get_logger().info('收到取消请求')
        return CancelResponse.ACCEPT
    
    async def execute_callback(self, goal_handle):
        """执行动作"""
        self.get_logger().info(f'开始执行: 计算斐波那契数列 (阶数={goal_handle.request.order})')
        
        # 初始化反馈和结果
        feedback_msg = Fibonacci.Feedback()
        result = Fibonacci.Result()
        
        # 计算斐波那契数列
        sequence = [0, 1]
        
        for i in range(1, goal_handle.request.order):
            # 检查是否被取消
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('目标被取消')
                result.sequence = sequence
                return result
            
            # 计算下一个数
            sequence.append(sequence[i] + sequence[i-1])
            
            # 发送反馈
            feedback_msg.partial_sequence = sequence.copy()
            goal_handle.publish_feedback(feedback_msg)
            
            self.get_logger().info(f'进度: {i+1}/{goal_handle.request.order} - 当前序列: {sequence}')
            
            # 模拟计算时间
            time.sleep(0.5)
        
        # 标记成功并返回结果
        goal_handle.succeed()
        result.sequence = sequence
        
        self.get_logger().info(f'✓ 完成! 最终序列: {result.sequence}')
        
        return result


def main(args=None):
    rclpy.init(args=args)
    
    node = FibonacciActionServer()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('服务器被用户中断')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
