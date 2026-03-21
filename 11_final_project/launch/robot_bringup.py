#!/usr/bin/env python3

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
import os


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim',
            default_value='true',
            description='Use simulation'
        ),
        
        Node(
            package='11_final_project',
            executable='robot_main.py',
            name='robot_main',
            output='screen',
            parameters=[{
                'use_sim_time': LaunchConfiguration('use_sim')
            }]
        ),
        
        Node(
            package='11_final_project',
            executable='sensor_manager.py',
            name='sensor_manager',
            output='screen'
        ),
        
        Node(
            package='11_final_project',
            executable='navigation_controller.py',
            name='navigation_controller',
            output='screen'
        ),
    ])
