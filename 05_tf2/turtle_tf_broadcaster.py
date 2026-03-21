#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped
from turtlesim.msg import Pose
from tf_transformations import quaternion_from_euler


class TurtleTFBroadcaster(Node):
    def __init__(self):
        super().__init__('turtle_tf_broadcaster')
        
        self.declare_parameter('turtle_name', 'turtle1')
        self.turtle_name = self.get_parameter('turtle_name').value
        
        self.tf_broadcaster = TransformBroadcaster(self)
        
        self.subscription = self.create_subscription(
            Pose,
            f'/{self.turtle_name}/pose',
            self.pose_callback,
            10
        )
        
        self.get_logger().info(f'海龟TF广播器已启动: {self.turtle_name}')
    
    def pose_callback(self, msg):
        t = TransformStamped()
        
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'world'
        t.child_frame_id = self.turtle_name
        
        t.transform.translation.x = msg.x
        t.transform.translation.y = msg.y
        t.transform.translation.z = 0.0
        
        q = quaternion_from_euler(0, 0, msg.theta)
        t.transform.rotation.x = q[0]
        t.transform.rotation.y = q[1]
        t.transform.rotation.z = q[2]
        t.transform.rotation.w = q[3]
        
        self.tf_broadcaster.sendTransform(t)


def main(args=None):
    rclpy.init(args=args)
    node = TurtleTFBroadcaster()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
