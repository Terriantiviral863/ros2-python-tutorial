#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from geometry_msgs.msg import TransformStamped
from std_msgs.msg import Header
from tf2_ros import TransformBroadcaster
from tf_transformations import quaternion_from_euler
import math


class RobotStatePublisher(Node):
    def __init__(self):
        super().__init__('robot_state_publisher')
        
        self.joint_pub = self.create_publisher(JointState, 'joint_states', 10)
        self.tf_broadcaster = TransformBroadcaster(self)
        
        self.timer = self.create_timer(0.05, self.timer_callback)
        
        self.left_wheel_angle = 0.0
        self.right_wheel_angle = 0.0
        self.robot_x = 0.0
        self.robot_y = 0.0
        self.robot_theta = 0.0
        
        self.linear_velocity = 0.1
        self.angular_velocity = 0.1
        
        self.get_logger().info('机器人状态发布器已启动')
        self.get_logger().info('发布关节状态和TF变换')
    
    def timer_callback(self):
        current_time = self.get_clock().now()
        
        self.publish_joint_states(current_time)
        
        self.publish_base_transform(current_time)
        
        self.update_robot_pose()
    
    def publish_joint_states(self, current_time):
        joint_state = JointState()
        joint_state.header = Header()
        joint_state.header.stamp = current_time.to_msg()
        
        joint_state.name = ['left_wheel_joint', 'right_wheel_joint']
        joint_state.position = [self.left_wheel_angle, self.right_wheel_angle]
        joint_state.velocity = [1.0, 1.0]
        joint_state.effort = []
        
        self.joint_pub.publish(joint_state)
        
        self.left_wheel_angle += 0.05
        self.right_wheel_angle += 0.05
    
    def publish_base_transform(self, current_time):
        t = TransformStamped()
        
        t.header.stamp = current_time.to_msg()
        t.header.frame_id = 'odom'
        t.child_frame_id = 'base_footprint'
        
        t.transform.translation.x = self.robot_x
        t.transform.translation.y = self.robot_y
        t.transform.translation.z = 0.0
        
        q = quaternion_from_euler(0, 0, self.robot_theta)
        t.transform.rotation.x = q[0]
        t.transform.rotation.y = q[1]
        t.transform.rotation.z = q[2]
        t.transform.rotation.w = q[3]
        
        self.tf_broadcaster.sendTransform(t)
    
    def update_robot_pose(self):
        dt = 0.05
        
        self.robot_x += self.linear_velocity * math.cos(self.robot_theta) * dt
        self.robot_y += self.linear_velocity * math.sin(self.robot_theta) * dt
        self.robot_theta += self.angular_velocity * dt
        
        if self.robot_theta > math.pi:
            self.robot_theta -= 2 * math.pi
        elif self.robot_theta < -math.pi:
            self.robot_theta += 2 * math.pi


def main(args=None):
    rclpy.init(args=args)
    node = RobotStatePublisher()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
