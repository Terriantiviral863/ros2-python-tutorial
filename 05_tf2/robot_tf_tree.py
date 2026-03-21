#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from tf2_ros import TransformBroadcaster, StaticTransformBroadcaster
from geometry_msgs.msg import TransformStamped
from tf_transformations import quaternion_from_euler
import math


class RobotTFTree(Node):
    def __init__(self):
        super().__init__('robot_tf_tree')
        
        self.tf_broadcaster = TransformBroadcaster(self)
        self.tf_static_broadcaster = StaticTransformBroadcaster(self)
        
        self.publish_static_transforms()
        
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        
        self.timer = self.create_timer(0.05, self.broadcast_timer_callback)
        
        self.get_logger().info('机器人完整TF树已启动')
        self.print_tf_tree()
    
    def print_tf_tree(self):
        self.get_logger().info('TF树结构:')
        self.get_logger().info('map')
        self.get_logger().info('└── odom')
        self.get_logger().info('    └── base_footprint')
        self.get_logger().info('        └── base_link')
        self.get_logger().info('            ├── laser_link')
        self.get_logger().info('            ├── camera_link')
        self.get_logger().info('            │   └── camera_optical_frame')
        self.get_logger().info('            ├── imu_link')
        self.get_logger().info('            ├── left_wheel_link')
        self.get_logger().info('            └── right_wheel_link')
    
    def publish_static_transforms(self):
        static_transforms = []
        current_time = self.get_clock().now().to_msg()
        
        base_footprint_to_base_link = TransformStamped()
        base_footprint_to_base_link.header.stamp = current_time
        base_footprint_to_base_link.header.frame_id = 'base_footprint'
        base_footprint_to_base_link.child_frame_id = 'base_link'
        base_footprint_to_base_link.transform.translation.x = 0.0
        base_footprint_to_base_link.transform.translation.y = 0.0
        base_footprint_to_base_link.transform.translation.z = 0.1
        q = quaternion_from_euler(0, 0, 0)
        base_footprint_to_base_link.transform.rotation.x = q[0]
        base_footprint_to_base_link.transform.rotation.y = q[1]
        base_footprint_to_base_link.transform.rotation.z = q[2]
        base_footprint_to_base_link.transform.rotation.w = q[3]
        static_transforms.append(base_footprint_to_base_link)
        
        laser_tf = TransformStamped()
        laser_tf.header.stamp = current_time
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
        
        camera_tf = TransformStamped()
        camera_tf.header.stamp = current_time
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
        
        camera_optical_tf = TransformStamped()
        camera_optical_tf.header.stamp = current_time
        camera_optical_tf.header.frame_id = 'camera_link'
        camera_optical_tf.child_frame_id = 'camera_optical_frame'
        camera_optical_tf.transform.translation.x = 0.0
        camera_optical_tf.transform.translation.y = 0.0
        camera_optical_tf.transform.translation.z = 0.0
        q = quaternion_from_euler(-math.pi/2, 0, -math.pi/2)
        camera_optical_tf.transform.rotation.x = q[0]
        camera_optical_tf.transform.rotation.y = q[1]
        camera_optical_tf.transform.rotation.z = q[2]
        camera_optical_tf.transform.rotation.w = q[3]
        static_transforms.append(camera_optical_tf)
        
        imu_tf = TransformStamped()
        imu_tf.header.stamp = current_time
        imu_tf.header.frame_id = 'base_link'
        imu_tf.child_frame_id = 'imu_link'
        imu_tf.transform.translation.x = 0.0
        imu_tf.transform.translation.y = 0.0
        imu_tf.transform.translation.z = 0.05
        q = quaternion_from_euler(0, 0, 0)
        imu_tf.transform.rotation.x = q[0]
        imu_tf.transform.rotation.y = q[1]
        imu_tf.transform.rotation.z = q[2]
        imu_tf.transform.rotation.w = q[3]
        static_transforms.append(imu_tf)
        
        left_wheel_tf = TransformStamped()
        left_wheel_tf.header.stamp = current_time
        left_wheel_tf.header.frame_id = 'base_link'
        left_wheel_tf.child_frame_id = 'left_wheel_link'
        left_wheel_tf.transform.translation.x = 0.0
        left_wheel_tf.transform.translation.y = 0.15
        left_wheel_tf.transform.translation.z = -0.05
        q = quaternion_from_euler(0, 0, 0)
        left_wheel_tf.transform.rotation.x = q[0]
        left_wheel_tf.transform.rotation.y = q[1]
        left_wheel_tf.transform.rotation.z = q[2]
        left_wheel_tf.transform.rotation.w = q[3]
        static_transforms.append(left_wheel_tf)
        
        right_wheel_tf = TransformStamped()
        right_wheel_tf.header.stamp = current_time
        right_wheel_tf.header.frame_id = 'base_link'
        right_wheel_tf.child_frame_id = 'right_wheel_link'
        right_wheel_tf.transform.translation.x = 0.0
        right_wheel_tf.transform.translation.y = -0.15
        right_wheel_tf.transform.translation.z = -0.05
        q = quaternion_from_euler(0, 0, 0)
        right_wheel_tf.transform.rotation.x = q[0]
        right_wheel_tf.transform.rotation.y = q[1]
        right_wheel_tf.transform.rotation.z = q[2]
        right_wheel_tf.transform.rotation.w = q[3]
        static_transforms.append(right_wheel_tf)
        
        self.tf_static_broadcaster.sendTransform(static_transforms)
    
    def broadcast_timer_callback(self):
        current_time = self.get_clock().now().to_msg()
        
        map_to_odom = TransformStamped()
        map_to_odom.header.stamp = current_time
        map_to_odom.header.frame_id = 'map'
        map_to_odom.child_frame_id = 'odom'
        map_to_odom.transform.translation.x = 0.0
        map_to_odom.transform.translation.y = 0.0
        map_to_odom.transform.translation.z = 0.0
        q = quaternion_from_euler(0, 0, 0)
        map_to_odom.transform.rotation.x = q[0]
        map_to_odom.transform.rotation.y = q[1]
        map_to_odom.transform.rotation.z = q[2]
        map_to_odom.transform.rotation.w = q[3]
        
        self.x += 0.01 * math.cos(self.theta)
        self.y += 0.01 * math.sin(self.theta)
        self.theta += 0.01
        
        odom_to_base_footprint = TransformStamped()
        odom_to_base_footprint.header.stamp = current_time
        odom_to_base_footprint.header.frame_id = 'odom'
        odom_to_base_footprint.child_frame_id = 'base_footprint'
        odom_to_base_footprint.transform.translation.x = self.x
        odom_to_base_footprint.transform.translation.y = self.y
        odom_to_base_footprint.transform.translation.z = 0.0
        q = quaternion_from_euler(0, 0, self.theta)
        odom_to_base_footprint.transform.rotation.x = q[0]
        odom_to_base_footprint.transform.rotation.y = q[1]
        odom_to_base_footprint.transform.rotation.z = q[2]
        odom_to_base_footprint.transform.rotation.w = q[3]
        
        self.tf_broadcaster.sendTransform([map_to_odom, odom_to_base_footprint])


def main(args=None):
    rclpy.init(args=args)
    node = RobotTFTree()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
