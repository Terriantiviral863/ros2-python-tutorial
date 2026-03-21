#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from tf2_ros import StaticTransformBroadcaster
from geometry_msgs.msg import TransformStamped
from tf_transformations import quaternion_from_euler
import math


class StaticTFPublisher(Node):
    def __init__(self):
        super().__init__('static_tf_publisher')
        
        self.tf_static_broadcaster = StaticTransformBroadcaster(self)
        
        self.publish_static_transforms()
        
        self.get_logger().info('静态TF发布器已启动')
        self.get_logger().info('发布的坐标系:')
        self.get_logger().info('  base_link -> camera_link')
        self.get_logger().info('  base_link -> laser_link')
        self.get_logger().info('  base_link -> imu_link')
    
    def publish_static_transforms(self):
        static_transforms = []
        
        camera_tf = TransformStamped()
        camera_tf.header.stamp = self.get_clock().now().to_msg()
        camera_tf.header.frame_id = 'base_link'
        camera_tf.child_frame_id = 'camera_link'
        camera_tf.transform.translation.x = 0.1
        camera_tf.transform.translation.y = 0.0
        camera_tf.transform.translation.z = 0.2
        q = quaternion_from_euler(0, 0, 0)
        camera_tf.transform.rotation.x = q[0]
        camera_tf.transform.rotation.y = q[1]
        camera_tf.transform.rotation.z = q[2]
        camera_tf.transform.rotation.w = q[3]
        static_transforms.append(camera_tf)
        
        laser_tf = TransformStamped()
        laser_tf.header.stamp = self.get_clock().now().to_msg()
        laser_tf.header.frame_id = 'base_link'
        laser_tf.child_frame_id = 'laser_link'
        laser_tf.transform.translation.x = 0.15
        laser_tf.transform.translation.y = 0.0
        laser_tf.transform.translation.z = 0.1
        q = quaternion_from_euler(0, 0, 0)
        laser_tf.transform.rotation.x = q[0]
        laser_tf.transform.rotation.y = q[1]
        laser_tf.transform.rotation.z = q[2]
        laser_tf.transform.rotation.w = q[3]
        static_transforms.append(laser_tf)
        
        imu_tf = TransformStamped()
        imu_tf.header.stamp = self.get_clock().now().to_msg()
        imu_tf.header.frame_id = 'base_link'
        imu_tf.child_frame_id = 'imu_link'
        imu_tf.transform.translation.x = 0.0
        imu_tf.transform.translation.y = 0.0
        imu_tf.transform.translation.z = 0.05
        q = quaternion_from_euler(0, 0, math.pi/4)
        imu_tf.transform.rotation.x = q[0]
        imu_tf.transform.rotation.y = q[1]
        imu_tf.transform.rotation.z = q[2]
        imu_tf.transform.rotation.w = q[3]
        static_transforms.append(imu_tf)
        
        self.tf_static_broadcaster.sendTransform(static_transforms)


def main(args=None):
    rclpy.init(args=args)
    node = StaticTFPublisher()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
