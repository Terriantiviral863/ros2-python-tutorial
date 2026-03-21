#!/usr/bin/env python3

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    """
    参数配置Launch文件示例
    从YAML文件加载参数
    """
    
    # 获取配置文件路径
    # 注意：这里使用绝对路径，因为这不是一个正式的ROS2包
    config_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'config'
    )
    
    params_file = os.path.join(config_dir, 'params.yaml')
    robot_config_file = os.path.join(config_dir, 'robot_config.yaml')
    
    # 声明Launch参数
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='使用仿真时间'
    )
    
    config_file_arg = DeclareLaunchArgument(
        'config_file',
        default_value=params_file,
        description='参数配置文件路径'
    )
    
    # 从YAML文件加载参数的节点
    talker_with_params = Node(
        package='demo_nodes_cpp',
        executable='talker',
        name='talker',
        output='screen',
        parameters=[
            params_file,
            {'use_sim_time': LaunchConfiguration('use_sim_time')}
        ]
    )
    
    listener_with_params = Node(
        package='demo_nodes_cpp',
        executable='listener',
        name='listener',
        output='screen',
        parameters=[
            params_file,
            {'use_sim_time': LaunchConfiguration('use_sim_time')}
        ]
    )
    
    # 使用机器人配置的节点
    robot_node = Node(
        package='demo_nodes_cpp',
        executable='talker',
        name='robot_controller',
        output='screen',
        parameters=[robot_config_file]
    )
    
    return LaunchDescription([
        use_sim_time_arg,
        config_file_arg,
        talker_with_params,
        listener_with_params,
        robot_node
    ])
