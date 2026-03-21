#!/usr/bin/env python3

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    """
    简单Launch文件示例
    启动单个talker节点
    """
    
    return LaunchDescription([
        Node(
            package='demo_nodes_cpp',
            executable='talker',
            name='simple_talker',
            output='screen',
            parameters=[{
                'use_sim_time': False
            }]
        )
    ])
