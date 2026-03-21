#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from tf2_ros import TransformBroadcaster, StaticTransformBroadcaster
from geometry_msgs.msg import TransformStamped
from tf_transformations import quaternion_from_euler
import math


class TFBroadcaster(Node):
    def __init__(self):
        super().__init__('tf_broadcaster')
        
        self.tf_broadcaster = TransformBroadcaster(self)
        self.tf_static_broadcaster = StaticTransformBroadcaster(self)
        
        self.publish_static_transforms()
        
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        
        self.timer = self.create_timer(0.05, self.broadcast_timer_callback)
        
        self.get_logger().info('完整TF广播器已启动')
        self.get_logger().info('TF树结构:')
        self.get_logger().info('  map -> odom -> base_link -> [sensors]')
    
    def publish_static_transforms(self):
        static_transforms = []
        
        laser_tf = TransformStamped()
        laser_tf.header.stamp = self.get_clock().now().to_msg()
        laser_tf.header.frame_id = 'base_link'
        laser_tf.child_frame_id = 'laser_link'
        laser_tf.transform.translation.x = 0.1
        laser_tf.transform.translation.y = 0.0
        laser_tf.transform.translation.z = 0.2
        q = quaternion_from_euler(0, 0, 0)
        laser_tf.transform.rotation.x = q[0]
        laser_tf.transform.rotation.y = q[1]
        laser_tf.transform.rotation.z = q[2]
        laser_tf.transform.rotation.w = q[3]
        static_transforms.append(laser_tf)
        
        camera_tf = TransformStamped()
        camera_tf.header.stamp = self.get_clock().now().to_msg()
        camera_tf.header.frame_id = 'base_link'
        camera_tf.child_frame_id = 'camera_link'
        camera_tf.transform.translation.x = 0.05
        camera_tf.transform.translation.y = 0.0
        camera_tf.transform.translation.z = 0.3
        q = quaternion_from_euler(0, 0.1, 0)
        camera_tf.transform.rotation.x = q[0]
        camera_tf.transform.rotation.y = q[1]
        camera_tf.transform.rotation.z = q[2]
        camera_tf.transform.rotation.w = q[3]
        static_transforms.append(camera_tf)
        
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
        
        odom_to_base = TransformStamped()
        odom_to_base.header.stamp = current_time
        odom_to_base.header.frame_id = 'odom'
        odom_to_base.child_frame_id = 'base_link'
        odom_to_base.transform.translation.x = self.x
        odom_to_base.transform.translation.y = self.y
        odom_to_base.transform.translation.z = 0.0
        q = quaternion_from_euler(0, 0, self.theta)
        odom_to_base.transform.rotation.x = q[0]
        odom_to_base.transform.rotation.y = q[1]
        odom_to_base.transform.rotation.z = q[2]
        odom_to_base.transform.rotation.w = q[3]
        
        self.tf_broadcaster.sendTransform([map_to_odom, odom_to_base])


def main(args=None):
    rclpy.init(args=args)
    node = TFBroadcaster()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
