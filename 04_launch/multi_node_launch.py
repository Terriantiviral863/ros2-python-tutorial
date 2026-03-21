#!/usr/bin/env python3

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    """
    多节点Launch文件示例
    同时启动talker和listener节点
    """
    
    # Talker节点
    talker_node = Node(
        package='demo_nodes_cpp',
        executable='talker',
        name='my_talker',
        output='screen',
        parameters=[{
            'use_sim_time': False
        }]
    )
    
    # Listener节点
    listener_node = Node(
        package='demo_nodes_cpp',
        executable='listener',
        name='my_listener',
        output='screen',
        parameters=[{
            'use_sim_time': False
        }]
    )
    
    # 第二个Talker节点（不同配置）
    talker2_node = Node(
        package='demo_nodes_cpp',
        executable='talker',
        name='talker_slow',
        output='screen',
        remappings=[
            ('chatter', 'chatter_slow')
        ]
    )
    
    return LaunchDescription([
        talker_node,
        listener_node,
        talker2_node
    ])
