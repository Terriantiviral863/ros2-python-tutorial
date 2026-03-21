#!/usr/bin/env python3

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node


def generate_launch_description():
    """
    条件启动Launch文件示例
    根据参数决定启动哪些节点
    """
    
    # 声明Launch参数
    use_sim_arg = DeclareLaunchArgument(
        'use_sim',
        default_value='false',
        description='是否使用仿真模式'
    )
    
    enable_camera_arg = DeclareLaunchArgument(
        'enable_camera',
        default_value='true',
        description='是否启用摄像头'
    )
    
    robot_name_arg = DeclareLaunchArgument(
        'robot_name',
        default_value='robot_default',
        description='机器人名称'
    )
    
    # 仿真模式节点（仅在use_sim=true时启动）
    sim_node = Node(
        package='demo_nodes_cpp',
        executable='talker',
        name='simulator',
        output='screen',
        condition=IfCondition(LaunchConfiguration('use_sim')),
        parameters=[{
            'use_sim_time': True
        }]
    )
    
    # 真实硬件节点（仅在use_sim=false时启动）
    hardware_node = Node(
        package='demo_nodes_cpp',
        executable='talker',
        name='hardware_driver',
        output='screen',
        condition=UnlessCondition(LaunchConfiguration('use_sim')),
        parameters=[{
            'use_sim_time': False
        }]
    )
    
    # 摄像头节点（根据enable_camera参数）
    camera_node = Node(
        package='demo_nodes_cpp',
        executable='talker',
        name='camera_driver',
        output='screen',
        condition=IfCondition(LaunchConfiguration('enable_camera')),
        remappings=[
            ('chatter', 'camera/image_raw')
        ]
    )
    
    # 总是启动的核心节点
    core_node = Node(
        package='demo_nodes_cpp',
        executable='listener',
        name='core_controller',
        output='screen'
    )
    
    # 日志信息
    log_sim_mode = LogInfo(
        msg=['启动模式: 仿真'],
        condition=IfCondition(LaunchConfiguration('use_sim'))
    )
    
    log_real_mode = LogInfo(
        msg=['启动模式: 真实硬件'],
        condition=UnlessCondition(LaunchConfiguration('use_sim'))
    )
    
    log_camera = LogInfo(
        msg=['摄像头: 已启用'],
        condition=IfCondition(LaunchConfiguration('enable_camera'))
    )
    
    return LaunchDescription([
        # 参数声明
        use_sim_arg,
        enable_camera_arg,
        robot_name_arg,
        
        # 日志
        log_sim_mode,
        log_real_mode,
        log_camera,
        
        # 节点
        sim_node,
        hardware_node,
        camera_node,
        core_node
    ])
