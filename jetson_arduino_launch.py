from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # Input Node - gets user input and publishes to 'sender' topic
        Node(
            package='jetson_stm32_poc',
            executable='input_node',
            name='values_giver',
            output='screen',
            emulate_tty=True,
        ),
        
        # Arduino Interface Node - subscribes to 'sender' and sends to Arduino via serial
        Node(
            package='jetson_stm32_poc',
            executable='arduino_interface',
            name='values_getter_sender',
            output='screen',
            parameters=[
                {'port': '/dev/ttyUSB0'},
                {'baud_rate': 115200}
            ]
        ),
    ])