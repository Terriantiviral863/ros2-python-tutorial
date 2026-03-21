#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from tf_transformations import euler_from_quaternion
import math


class ImuProcessor(Node):
    def __init__(self):
        super().__init__('imu_processor')
        
        self.subscription = self.create_subscription(
            Imu,
            'imu/data',
            self.imu_callback,
            10
        )
        
        self.get_logger().info('IMU处理器已启动')
    
    def imu_callback(self, msg):
        q = [
            msg.orientation.x,
            msg.orientation.y,
            msg.orientation.z,
            msg.orientation.w
        ]
        
        roll, pitch, yaw = euler_from_quaternion(q)
        
        wx = msg.angular_velocity.x
        wy = msg.angular_velocity.y
        wz = msg.angular_velocity.z
        
        ax = msg.linear_acceleration.x
        ay = msg.linear_acceleration.y
        az = msg.linear_acceleration.z
        
        self.get_logger().info(
            f'姿态: roll={math.degrees(roll):.1f}°, '
            f'pitch={math.degrees(pitch):.1f}°, '
            f'yaw={math.degrees(yaw):.1f}°'
        )
        
        self.get_logger().info(
            f'角速度: wx={wx:.3f}, wy={wy:.3f}, wz={wz:.3f} rad/s'
        )
        
        self.get_logger().info(
            f'加速度: ax={ax:.2f}, ay={ay:.2f}, az={az:.2f} m/s²'
        )


def main(args=None):
    rclpy.init(args=args)
    node = ImuProcessor()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
