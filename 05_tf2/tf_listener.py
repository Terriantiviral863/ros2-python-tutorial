#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from tf2_ros import TransformListener, Buffer
from tf2_ros import LookupException, ConnectivityException, ExtrapolationException
from geometry_msgs.msg import PointStamped
import tf2_geometry_msgs
from tf_transformations import euler_from_quaternion
import math


class TFListener(Node):
    def __init__(self):
        super().__init__('tf_listener')
        
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        
        self.timer = self.create_timer(1.0, self.on_timer)
        
        self.get_logger().info('TF监听器已启动')
        self.get_logger().info('监听 world -> base_link 的变换')
    
    def on_timer(self):
        try:
            trans = self.tf_buffer.lookup_transform(
                'world',
                'base_link',
                rclpy.time.Time()
            )
            
            x = trans.transform.translation.x
            y = trans.transform.translation.y
            z = trans.transform.translation.z
            
            q = [
                trans.transform.rotation.x,
                trans.transform.rotation.y,
                trans.transform.rotation.z,
                trans.transform.rotation.w
            ]
            roll, pitch, yaw = euler_from_quaternion(q)
            
            self.get_logger().info(
                f'位置: x={x:.3f}, y={y:.3f}, z={z:.3f}'
            )
            self.get_logger().info(
                f'姿态: roll={math.degrees(roll):.1f}°, '
                f'pitch={math.degrees(pitch):.1f}°, '
                f'yaw={math.degrees(yaw):.1f}°'
            )
            
            self.transform_point()
            
        except (LookupException, ConnectivityException, ExtrapolationException) as e:
            self.get_logger().warn(f'TF查询失败: {e}')
    
    def transform_point(self):
        try:
            point_in_base = PointStamped()
            point_in_base.header.frame_id = 'base_link'
            point_in_base.header.stamp = self.get_clock().now().to_msg()
            point_in_base.point.x = 1.0
            point_in_base.point.y = 0.0
            point_in_base.point.z = 0.0
            
            point_in_world = self.tf_buffer.transform(
                point_in_base,
                'world',
                timeout=rclpy.duration.Duration(seconds=1.0)
            )
            
            self.get_logger().info(
                f'点变换: base_link(1,0,0) -> '
                f'world({point_in_world.point.x:.3f}, '
                f'{point_in_world.point.y:.3f}, '
                f'{point_in_world.point.z:.3f})'
            )
            
        except Exception as ex:
            self.get_logger().error(f'点变换失败: {ex}')


def main(args=None):
    rclpy.init(args=args)
    node = TFListener()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
