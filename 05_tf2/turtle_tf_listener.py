#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from tf2_ros import TransformListener, Buffer
from tf2_ros import LookupException, ConnectivityException, ExtrapolationException
from geometry_msgs.msg import Twist
from turtlesim.srv import Spawn
import math


class TurtleTFListener(Node):
    def __init__(self):
        super().__init__('turtle_tf_listener')
        
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        
        self.spawner = self.create_client(Spawn, 'spawn')
        self.turtle_spawning_service_ready = False
        
        self.publisher = self.create_publisher(Twist, '/turtle2/cmd_vel', 10)
        
        self.timer = self.create_timer(0.1, self.on_timer)
        
        self.get_logger().info('海龟TF监听器已启动')
        self.get_logger().info('turtle2将跟随turtle1')
    
    def on_timer(self):
        if not self.turtle_spawning_service_ready:
            if self.spawner.service_is_ready():
                request = Spawn.Request()
                request.x = 4.0
                request.y = 2.0
                request.theta = 0.0
                request.name = 'turtle2'
                
                future = self.spawner.call_async(request)
                future.add_done_callback(self.spawn_callback)
                
                self.turtle_spawning_service_ready = True
            return
        
        try:
            trans = self.tf_buffer.lookup_transform(
                'turtle2',
                'turtle1',
                rclpy.time.Time()
            )
            
            msg = Twist()
            
            scale_rotation_rate = 1.0
            msg.angular.z = scale_rotation_rate * math.atan2(
                trans.transform.translation.y,
                trans.transform.translation.x
            )
            
            scale_forward_speed = 0.5
            msg.linear.x = scale_forward_speed * math.sqrt(
                trans.transform.translation.x ** 2 +
                trans.transform.translation.y ** 2
            )
            
            self.publisher.publish(msg)
            
        except (LookupException, ConnectivityException, ExtrapolationException) as e:
            self.get_logger().debug(f'TF查询失败: {e}')
    
    def spawn_callback(self, future):
        try:
            response = future.result()
            self.get_logger().info(f'成功生成turtle2: {response.name}')
        except Exception as e:
            self.get_logger().error(f'生成turtle2失败: {e}')


def main(args=None):
    rclpy.init(args=args)
    node = TurtleTFListener()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
