from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='duo_image_publisher',
            executable='camera_node',
            name='camera_1',
            parameters=[
                {'camera_id': '/dev/video0'},
                {'image_topic': '/camera1/image_raw'}
            ],
        ),
        Node(
            package='duo_image_publisher',
            executable='camera_node',
            name='camera_2',
            parameters=[
                {'camera_id': '/dev/video2'},
                {'image_topic': '/camera2/image_raw'}
            ],
        ),
    ])
