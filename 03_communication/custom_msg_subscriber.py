#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from custom_interfaces.msg import RobotStatus, SensorData


class CustomMessageSubscriber(Node):
    """订阅自定义消息的节点"""
    
    def __init__(self):
        super().__init__('custom_msg_subscriber')
        
        # 创建订阅者
        self.robot_status_sub = self.create_subscription(
            RobotStatus,
            'robot_status',
            self.robot_status_callback,
            10
        )
        
        self.sensor_data_sub = self.create_subscription(
            SensorData,
            'sensor_data',
            self.sensor_data_callback,
            10
        )
        
        # 统计信息
        self.status_count = 0
        self.sensor_count = 0
        
        self.get_logger().info('自定义消息订阅者已启动')
        self.get_logger().info('等待接收消息...')
    
    def robot_status_callback(self, msg):
        """处理机器人状态消息"""
        self.status_count += 1
        
        # 显示状态信息
        self.get_logger().info(
            f'\n===== 机器人状态 #{self.status_count} ====='
            f'\n  ID: {msg.robot_id}'
            f'\n  状态: {msg.status}'
            f'\n  电池: {msg.battery_level:.1f}%'
            f'\n  位置: ({msg.position.x:.2f}, {msg.position.y:.2f}, {msg.position.z:.2f})'
            f'\n  速度: {msg.velocity:.2f} m/s'
            f'\n  忙碌: {"是" if msg.is_busy else "否"}'
            f'\n  错误码: {msg.error_code}'
            f'\n  消息: {msg.message}'
        )
        
        # 检查警告条件
        if msg.battery_level < 20.0:
            self.get_logger().warn(f'⚠️  电池电量低: {msg.battery_level:.1f}%')
        
        if msg.error_code != 0:
            self.get_logger().error(f'❌ 错误代码: {msg.error_code}')
        
        if msg.status == 'CHARGING':
            self.get_logger().info('🔋 机器人正在充电')
    
    def sensor_data_callback(self, msg):
        """处理传感器数据消息"""
        self.sensor_count += 1
        
        # 计算统计信息
        if len(msg.values) > 0:
            min_val = min(msg.values)
            max_val = max(msg.values)
            avg_val = sum(msg.values) / len(msg.values)
        else:
            min_val = max_val = avg_val = 0.0
        
        # 显示传感器信息
        self.get_logger().debug(
            f'\n----- 传感器数据 #{self.sensor_count} -----'
            f'\n  类型: {msg.sensor_type}'
            f'\n  ID: {msg.sensor_id}'
            f'\n  数据点数: {len(msg.values)}'
            f'\n  最小值: {min_val:.2f}'
            f'\n  最大值: {max_val:.2f}'
            f'\n  平均值: {avg_val:.2f}'
            f'\n  质量: {msg.quality:.2f}'
            f'\n  有效: {"是" if msg.is_valid else "否"}'
        )
        
        # 检查数据质量
        if not msg.is_valid:
            self.get_logger().warn(f'⚠️  传感器数据质量低: {msg.quality:.2f}')
        
        # 检查异常值
        if min_val < 0.3:
            self.get_logger().warn(f'⚠️  检测到障碍物过近: {min_val:.2f}m')


def main(args=None):
    rclpy.init(args=args)
    
    node = CustomMessageSubscriber()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info(
            f'\n节点被用户中断'
            f'\n总共接收: {node.status_count} 条状态消息, '
            f'{node.sensor_count} 条传感器消息'
        )
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
