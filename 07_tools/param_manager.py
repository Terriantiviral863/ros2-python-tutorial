#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import ParameterDescriptor


class ParamManager(Node):
    def __init__(self):
        super().__init__('param_manager')
        
        self.declare_parameter('my_string', 'hello', 
            ParameterDescriptor(description='字符串参数'))
        self.declare_parameter('my_int', 42,
            ParameterDescriptor(description='整数参数'))
        self.declare_parameter('my_float', 3.14,
            ParameterDescriptor(description='浮点数参数'))
        
        self.timer = self.create_timer(2.0, self.timer_callback)
        
        self.get_logger().info('参数管理器已启动')
    
    def timer_callback(self):
        my_string = self.get_parameter('my_string').value
        my_int = self.get_parameter('my_int').value
        my_float = self.get_parameter('my_float').value
        
        self.get_logger().info(f'参数值: {my_string}, {my_int}, {my_float}')


def main(args=None):
    rclpy.init(args=args)
    node = ParamManager()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
