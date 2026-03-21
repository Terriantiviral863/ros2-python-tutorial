#!/usr/bin/env python3

import sys
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts


class ServiceClient(Node):
    def __init__(self):
        super().__init__('service_client')
        
        self.client = self.create_client(AddTwoInts, 'add_two_ints')
        
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('等待服务启动...')
        
        self.get_logger().info('服务客户端已连接')
    
    def send_request(self, a, b):
        request = AddTwoInts.Request()
        request.a = a
        request.b = b
        
        self.get_logger().info(f'发送请求: {a} + {b}')
        
        future = self.client.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        
        if future.result() is not None:
            self.get_logger().info(f'收到结果: {future.result().sum}')
            return future.result().sum
        else:
            self.get_logger().error('服务调用失败')
            return None


def main(args=None):
    rclpy.init(args=args)
    node = ServiceClient()
    
    if len(sys.argv) >= 3:
        a = int(sys.argv[1])
        b = int(sys.argv[2])
    else:
        a = 10
        b = 20
    
    result = node.send_request(a, b)
    
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
