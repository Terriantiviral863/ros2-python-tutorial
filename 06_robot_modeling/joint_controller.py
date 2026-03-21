#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
import math


class JointController(Node):
    def __init__(self):
        super().__init__('joint_controller')
        
        self.joint_pub = self.create_publisher(JointState, 'joint_states', 10)
        
        self.timer = self.create_timer(0.05, self.timer_callback)
        
        self.declare_parameter('control_mode', 'sine')
        self.control_mode = self.get_parameter('control_mode').value
        
        self.time = 0.0
        
        self.get_logger().info('关节控制器已启动')
        self.get_logger().info(f'控制模式: {self.control_mode}')
        self.get_logger().info('可用模式: sine, square, triangle, manual')
    
    def timer_callback(self):
        joint_state = JointState()
        joint_state.header = Header()
        joint_state.header.stamp = self.get_clock().now().to_msg()
        
        joint_state.name = [
            'left_wheel_joint',
            'right_wheel_joint'
        ]
        
        if self.control_mode == 'sine':
            left_pos = math.sin(self.time)
            right_pos = math.sin(self.time + math.pi)
        elif self.control_mode == 'square':
            left_pos = 1.0 if math.sin(self.time) > 0 else -1.0
            right_pos = 1.0 if math.sin(self.time + math.pi) > 0 else -1.0
        elif self.control_mode == 'triangle':
            left_pos = (self.time % (2 * math.pi)) / math.pi - 1.0
            right_pos = ((self.time + math.pi) % (2 * math.pi)) / math.pi - 1.0
        else:
            left_pos = 0.0
            right_pos = 0.0
        
        joint_state.position = [left_pos, right_pos]
        joint_state.velocity = []
        joint_state.effort = []
        
        self.joint_pub.publish(joint_state)
        
        self.time += 0.05
        
        if int(self.time * 10) % 50 == 0:
            self.get_logger().info(
                f'关节位置: left={left_pos:.3f}, right={right_pos:.3f}'
            )


def main(args=None):
    rclpy.init(args=args)
    node = JointController()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
