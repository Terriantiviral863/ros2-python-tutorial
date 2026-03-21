#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped


class UIInterface(Node):
    def __init__(self):
        super().__init__('ui_interface')
        
        self.goal_pub = self.create_publisher(PoseStamped, 'goal_pose', 10)
        self.task_pub = self.create_publisher(String, 'task_command', 10)
        
        self.status_sub = self.create_subscription(
            String,
            'robot_status',
            self.status_callback,
            10
        )
        
        self.get_logger().info('用户界面已启动')
        self.show_menu()
    
    def status_callback(self, msg):
        pass
    
    def show_menu(self):
        print("\n" + "="*50)
        print("机器人控制界面")
        print("="*50)
        print("1. 发送目标点")
        print("2. 执行巡逻任务")
        print("3. 停止任务")
        print("4. 查看状态")
        print("5. 退出")
        print("="*50)
    
    def send_goal(self, x, y):
        goal = PoseStamped()
        goal.header.frame_id = "map"
        goal.header.stamp = self.get_clock().now().to_msg()
        goal.pose.position.x = x
        goal.pose.position.y = y
        goal.pose.orientation.w = 1.0
        
        self.goal_pub.publish(goal)
        self.get_logger().info(f'已发送目标点: ({x}, {y})')
    
    def send_task(self, task_name):
        msg = String()
        msg.data = task_name
        self.task_pub.publish(msg)
        self.get_logger().info(f'已发送任务: {task_name}')
    
    def run_interactive(self):
        while rclpy.ok():
            try:
                choice = input("\n请选择操作 (1-5): ")
                
                if choice == '1':
                    x = float(input("输入X坐标: "))
                    y = float(input("输入Y坐标: "))
                    self.send_goal(x, y)
                
                elif choice == '2':
                    self.send_task('patrol')
                    print("已启动巡逻任务")
                
                elif choice == '3':
                    self.send_task('stop')
                    print("已发送停止命令")
                
                elif choice == '4':
                    print("查看ROS2话题获取状态信息")
                    print("运行: ros2 topic echo /robot_status")
                
                elif choice == '5':
                    print("退出界面")
                    break
                
                else:
                    print("无效选择，请重试")
                
                rclpy.spin_once(self, timeout_sec=0.1)
                
            except KeyboardInterrupt:
                break
            except ValueError:
                print("输入错误，请重试")


def main(args=None):
    rclpy.init(args=args)
    node = UIInterface()
    
    try:
        node.run_interactive()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
