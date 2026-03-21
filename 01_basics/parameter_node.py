#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import ParameterDescriptor


class ParameterNode(Node):
    def __init__(self):
        super().__init__('param_node')
        
        my_param_descriptor = ParameterDescriptor(
            description='这是一个示例参数'
        )
        
        self.declare_parameter('my_parameter', 'default_value', my_param_descriptor)
        self.declare_parameter('update_rate', 1.0)
        
        self.timer = self.create_timer(1.0, self.timer_callback)
        
        self.get_logger().info('参数节点已启动')
        self.get_logger().info(f'初始参数值: {self.get_parameter("my_parameter").value}')
    
    def timer_callback(self):
        my_param = self.get_parameter('my_parameter').value
        update_rate = self.get_parameter('update_rate').value
        
        self.get_logger().info(f'当前参数 my_parameter = {my_param}')
        self.get_logger().info(f'当前参数 update_rate = {update_rate}')
        
        if update_rate != self.timer.timer_period_ns / 1e9:
            self.timer.cancel()
            self.timer = self.create_timer(update_rate, self.timer_callback)
            self.get_logger().info(f'更新定时器频率为 {update_rate} 秒')


def main(args=None):
    rclpy.init(args=args)
    node = ParameterNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
