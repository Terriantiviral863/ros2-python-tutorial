#!/usr/bin/env python3

from launch import LaunchDescription
from launch_ros.actions import Node, PushRosNamespace
from launch.actions import GroupAction


def generate_launch_description():
    """
    命名空间Launch文件示例
    启动多个机器人，每个机器人有独立的命名空间
    """
    
    # 机器人1
    robot1_group = GroupAction([
        PushRosNamespace('robot1'),
        Node(
            package='demo_nodes_cpp',
            executable='talker',
            name='talker',
            output='screen',
            parameters=[{
                'use_sim_time': False
            }]
        ),
        Node(
            package='demo_nodes_cpp',
            executable='listener',
            name='listener',
            output='screen'
        )
    ])
    
    # 机器人2
    robot2_group = GroupAction([
        PushRosNamespace('robot2'),
        Node(
            package='demo_nodes_cpp',
            executable='talker',
            name='talker',
            output='screen',
            parameters=[{
                'use_sim_time': False
            }]
        ),
        Node(
            package='demo_nodes_cpp',
            executable='listener',
            name='listener',
            output='screen'
        )
    ])
    
    # 机器人3 - 使用不同的方法（直接在Node中指定namespace）
    robot3_talker = Node(
        package='demo_nodes_cpp',
        executable='talker',
        name='talker',
        namespace='robot3',
        output='screen'
    )
    
    robot3_listener = Node(
        package='demo_nodes_cpp',
        executable='listener',
        name='listener',
        namespace='robot3',
        output='screen'
    )
    
    return LaunchDescription([
        robot1_group,
        robot2_group,
        robot3_talker,
        robot3_listener
    ])
