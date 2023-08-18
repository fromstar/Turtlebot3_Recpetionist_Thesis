from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
                package='turtlebot3_navigation_povo',
                executable='set_initial_pose',
                name='set_pose'
            ),
        # Node(
        #     ),
    ])