#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
import sys


class TaskExecutor(Node):
    def __init__(self):
        super().__init__('task_executor')
        
        self.task_cmd_pub = self.create_publisher(String, 'task_command', 10)
        self.goal_pub = self.create_publisher(PoseStamped, 'goal_pose', 10)
        
        self.status_sub = self.create_subscription(
            String,
            'robot_status',
            self.status_callback,
            10
        )
        
        self.patrol_waypoints = [
            (2.0, 0.0),
            (2.0, 2.0),
            (0.0, 2.0),
            (0.0, 0.0)
        ]
        
        self.current_waypoint = 0
        
        self.get_logger().info('任务执行器已启动')
    
    def status_callback(self, msg):
        self.get_logger().info(f'机器人状态: {msg.data}')
    
    def execute_patrol_task(self):
        self.get_logger().info('开始执行巡逻任务')
        
        task_msg = String()
        task_msg.data = 'patrol'
        self.task_cmd_pub.publish(task_msg)
        
        for i, waypoint in enumerate(self.patrol_waypoints):
            self.get_logger().info(f'发送航点 {i+1}/{len(self.patrol_waypoints)}: {waypoint}')
            self.send_goal(waypoint[0], waypoint[1])
            rclpy.spin_once(self, timeout_sec=5.0)
    
    def execute_goto_task(self, x, y):
        self.get_logger().info(f'前往目标点: ({x}, {y})')
        self.send_goal(x, y)
    
    def execute_stop_task(self):
        self.get_logger().info('停止任务')
        task_msg = String()
        task_msg.data = 'stop'
        self.task_cmd_pub.publish(task_msg)
    
    def send_goal(self, x, y):
        goal = PoseStamped()
        goal.header.frame_id = "map"
        goal.header.stamp = self.get_clock().now().to_msg()
        goal.pose.position.x = x
        goal.pose.position.y = y
        goal.pose.orientation.w = 1.0
        
        self.goal_pub.publish(goal)


def main(args=None):
    rclpy.init(args=args)
    node = TaskExecutor()
    
    if len(sys.argv) > 1:
        task = sys.argv[1]
        
        if task == 'patrol':
            node.execute_patrol_task()
        elif task == 'stop':
            node.execute_stop_task()
        elif task == 'goto' and len(sys.argv) >= 4:
            x = float(sys.argv[2])
            y = float(sys.argv[3])
            node.execute_goto_task(x, y)
        else:
            node.get_logger().info('用法:')
            node.get_logger().info('  patrol - 执行巡逻任务')
            node.get_logger().info('  goto <x> <y> - 前往指定位置')
            node.get_logger().info('  stop - 停止任务')
    else:
        node.get_logger().info('请指定任务类型')
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
