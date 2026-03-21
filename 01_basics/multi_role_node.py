#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Int32
from example_interfaces.srv import AddTwoInts


class MultiRoleNode(Node):
    """
    一个多功能节点示例：
    - 订阅 /input_topic 话题
    - 发布到 /output_topic 话题
    - 提供 /add_service 服务
    - 使用参数配置行为
    """
    
    def __init__(self):
        super().__init__('multi_role_node')
        
        # 1. 声明参数
        self.declare_parameter('publish_rate', 1.0)
        self.declare_parameter('prefix', 'Processed: ')
        
        # 2. 创建订阅者 - 订阅数据
        self.subscription = self.create_subscription(
            String,
            'input_topic',
            self.input_callback,
            10
        )
        
        # 3. 创建发布者 - 发布数据
        self.publisher = self.create_publisher(Int32, 'output_topic', 10)
        
        # 4. 创建服务 - 提供服务
        self.service = self.create_service(
            AddTwoInts,
            'add_service',
            self.add_callback
        )
        
        # 5. 创建定时器 - 定期发布数据
        rate = self.get_parameter('publish_rate').value
        self.timer = self.create_timer(rate, self.timer_callback)
        
        self.counter = 0
        
        self.get_logger().info('多功能节点已启动！')
        self.get_logger().info('- 订阅话题: /input_topic')
        self.get_logger().info('- 发布话题: /output_topic')
        self.get_logger().info('- 提供服务: /add_service')
    
    def input_callback(self, msg):
        """订阅者回调 - 接收并处理数据"""
        prefix = self.get_parameter('prefix').value
        self.get_logger().info(f'收到订阅消息: {prefix}{msg.data}')
    
    def timer_callback(self):
        """定时器回调 - 定期发布数据"""
        msg = Int32()
        msg.data = self.counter
        self.publisher.publish(msg)
        self.get_logger().info(f'发布计数: {self.counter}')
        self.counter += 1
    
    def add_callback(self, request, response):
        """服务回调 - 提供加法服务"""
        response.sum = request.a + request.b
        self.get_logger().info(f'服务请求: {request.a} + {request.b} = {response.sum}')
        return response


def main(args=None):
    rclpy.init(args=args)
    node = MultiRoleNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
