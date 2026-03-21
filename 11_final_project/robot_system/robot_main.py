#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from enum import Enum
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import threading


class RobotState(Enum):
    IDLE = 0
    NAVIGATING = 1
    AVOIDING = 2
    TASK_EXECUTING = 3
    ERROR = 4


class RobotMain(Node):
    def __init__(self):
        super().__init__('robot_main')
        
        self.state = RobotState.IDLE
        self.state_lock = threading.Lock()
        
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.status_pub = self.create_publisher(String, 'robot_status', 10)
        
        self.task_sub = self.create_subscription(
            String,
            'task_command',
            self.task_callback,
            10
        )
        
        self.timer = self.create_timer(0.1, self.main_loop)
        
        self.current_task = None
        
        self.get_logger().info('机器人主控制节点已启动')
        self.get_logger().info(f'初始状态: {self.state.name}')
    
    def task_callback(self, msg):
        self.get_logger().info(f'收到任务命令: {msg.data}')
        self.current_task = msg.data
        self.transition_state(RobotState.TASK_EXECUTING)
    
    def main_loop(self):
        with self.state_lock:
            if self.state == RobotState.IDLE:
                self.handle_idle_state()
            elif self.state == RobotState.NAVIGATING:
                self.handle_navigating_state()
            elif self.state == RobotState.AVOIDING:
                self.handle_avoiding_state()
            elif self.state == RobotState.TASK_EXECUTING:
                self.handle_task_executing_state()
            elif self.state == RobotState.ERROR:
                self.handle_error_state()
        
        self.publish_status()
    
    def handle_idle_state(self):
        pass
    
    def handle_navigating_state(self):
        pass
    
    def handle_avoiding_state(self):
        cmd = Twist()
        cmd.linear.x = 0.0
        cmd.angular.z = 0.5
        self.cmd_vel_pub.publish(cmd)
    
    def handle_task_executing_state(self):
        if self.current_task:
            self.get_logger().info(f'执行任务: {self.current_task}')
            
            if self.current_task == 'patrol':
                self.execute_patrol_task()
            elif self.current_task == 'stop':
                self.stop_robot()
                self.transition_state(RobotState.IDLE)
                self.current_task = None
    
    def handle_error_state(self):
        self.get_logger().error('机器人处于错误状态')
        self.stop_robot()
    
    def execute_patrol_task(self):
        self.get_logger().info('执行巡逻任务')
    
    def transition_state(self, new_state):
        old_state = self.state
        self.state = new_state
        self.get_logger().info(f'状态转换: {old_state.name} -> {new_state.name}')
    
    def stop_robot(self):
        cmd = Twist()
        cmd.linear.x = 0.0
        cmd.angular.z = 0.0
        self.cmd_vel_pub.publish(cmd)
    
    def publish_status(self):
        msg = String()
        msg.data = f'State: {self.state.name}, Task: {self.current_task}'
        self.status_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    
    node = RobotMain()
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
