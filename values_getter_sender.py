#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64, Int32
from jetson_stm32_poc_msgs.msg import DataVector
import serial

class ArduinoInterface(Node):
    def __init__(self):
        super().__init__('values_getter_sender')
        
        # Declare parameters
        self.declare_parameter('port', '/dev/ttyUSB0')
        self.declare_parameter('baud_rate', 115200)
        
        port = self.get_parameter('port').value
        baud_rate = self.get_parameter('baud_rate').value
        
        self.num = DataVector()
        self.serial_port = None
        
        # Track last sent values to avoid logging duplicate sends
        self.last_sent = DataVector()
        self.last_sent.position_x = 0.0
        self.last_sent.position_y = 0.0
        self.last_sent.twist_z = 0.0
        
        try:
            # Initialize serial connection
            self.serial_port = serial.Serial(port, baud_rate, timeout=1)
            self.get_logger().info(f'Connected to Arduino on {port}')
            
            # Subscribers
            self.reader = self.create_subscription(
                DataVector,
                'sender',
                self.read_data,
                10)
                
        except serial.SerialException as e:
            self.get_logger().error(f'Failed to connect to Arduino: {e}')
    
    def data_callback(self):
        """Send servo command to Arduino"""
        if self.serial_port is None or not self.serial_port.is_open:
            self.get_logger().warn('Serial port not available')
            return
        
        command = f'{self.num.position_x},{self.num.position_y},{self.num.twist_z}\n'
        
        try:
            self.serial_port.write(command.encode())
            
            # Only log when values actually change
            if (self.last_sent.position_x != self.num.position_x or 
                self.last_sent.position_y != self.num.position_y or 
                self.last_sent.twist_z != self.num.twist_z):
                
                self.get_logger().info(f'Sent: {self.num.position_x}, {self.num.position_y}, {self.num.twist_z}')
                
                # Update last sent values
                self.last_sent.position_x = self.num.position_x
                self.last_sent.position_y = self.num.position_y
                self.last_sent.twist_z = self.num.twist_z
                
        except Exception as e:
            self.get_logger().error(f'Serial write failed: {e}')
    
    def read_data(self, msg):
        self.num.position_x = msg.position_x
        self.num.position_y = msg.position_y
        self.num.twist_z = msg.twist_z
        
        # Only log when values change (not every message at 10Hz)
        if (self.last_sent.position_x != msg.position_x or 
            self.last_sent.position_y != msg.position_y or 
            self.last_sent.twist_z != msg.twist_z):
            
            self.get_logger().info(f'Received: {self.num.position_x}, {self.num.position_y}, {self.num.twist_z}')
        
        self.data_callback()
    
    def __del__(self):
        if self.serial_port is not None and self.serial_port.is_open:
            self.serial_port.close()


def main(args=None):
    rclpy.init(args=args)
    node = ArduinoInterface()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()