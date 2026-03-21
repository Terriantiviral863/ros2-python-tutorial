#!/usr/bin/env python3

import os
from launch import LaunchDescription
from launch.actions import (
    IncludeLaunchDescription,
    DeclareLaunchArgument,
    LogInfo,
    TimerAction,
    RegisterEventHandler
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, ThisLaunchFileDir
from launch.event_handlers import OnProcessStart, OnProcessExit
from launch_ros.actions import Node


def generate_launch_description():
    """
    组合Launch文件示例
    包含其他Launch文件并添加事件处理
    """
    
    # 获取当前目录
    launch_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 声明参数
    namespace_arg = DeclareLaunchArgument(
        'namespace',
        default_value='',
        description='节点命名空间'
    )
    
    # 包含简单Launch文件
    include_simple = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(launch_dir, 'simple_launch.py')
        )
    )
    
    # 包含多节点Launch文件（延迟5秒启动）
    include_multi_delayed = TimerAction(
        period=5.0,
        actions=[
            LogInfo(msg='5秒后启动多节点系统...'),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(launch_dir, 'multi_node_launch.py')
                )
            )
        ]
    )
    
    # 监控节点
    monitor_node = Node(
        package='demo_nodes_cpp',
        executable='listener',
        name='system_monitor',
        output='screen',
        namespace=LaunchConfiguration('namespace')
    )
    
    # 事件处理：当监控节点启动时
    on_monitor_start = RegisterEventHandler(
        OnProcessStart(
            target_action=monitor_node,
            on_start=[
                LogInfo(msg='系统监控节点已启动')
            ]
        )
    )
    
    # 事件处理：当监控节点退出时
    on_monitor_exit = RegisterEventHandler(
        OnProcessExit(
            target_action=monitor_node,
            on_exit=[
                LogInfo(msg='警告：系统监控节点已退出！')
            ]
        )
    )
    
    return LaunchDescription([
        # 参数
        namespace_arg,
        
        # 启动信息
        LogInfo(msg='='*60),
        LogInfo(msg='组合Launch系统启动'),
        LogInfo(msg='='*60),
        
        # 包含其他Launch文件
        include_simple,
        include_multi_delayed,
        
        # 监控节点
        monitor_node,
        
        # 事件处理
        on_monitor_start,
        on_monitor_exit,
        
        # 结束信息
        LogInfo(msg='所有组件已配置完成')
    ])
