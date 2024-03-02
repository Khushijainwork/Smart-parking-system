"""
A library to interface Arduino through serial connection
(adapted from: https://github.com/lekum/pyduino)
"""

import serial

class Arduino():
    """
    Models an Arduino connection
    """

    def __init__(self, serial_port='/dev/ttyACM0', baud_rate=9600, read_timeout=5):
        """
        Initializes the serial connection to the Arduino board
        """
        self.conn = serial.Serial(serial_port, baud_rate)
        self.conn.timeout = read_timeout

    def set_pin_mode(self, pin_number, mode):
        """
        Performs a pinMode() operation on pin_number
        Internally sends b'M{mode}{pin_number} where mode could be:
        - I for INPUT
        - O for OUTPUT
        - P for INPUT_PULLUP
        """
        command = ('M{}{}\n'.format(mode, pin_number)).encode()
        self.conn.write(command)

    def digital_read(self, pin_number):
        """
        Performs a digital read on pin_number and returns the value (1 or 0)
        Internally sends b'RD{pin_number}' over the serial connection
        """
        command = ('RD{}\n'.format(pin_number)).encode()
        self.conn.write(command)
        line_received = self.conn.readline().decode().strip()
        header, value = line_received.split(':')
        if header == ('D' + str(pin_number)):
            # If header matches
            return int(value)

    def digital_write(self, pin_number, digital_value):
        """
        Writes the digital_value on pin_number
        Internally sends b'WD{pin_number}:{digital_value}' over the serial connection
        """
        command = f'WD{pin_number}:{digital_value}'.encode()
        self.conn.write(command)

    def ultrasonic_read(self, pin_number):
        """
        Performs a read on the ultrasonic ranger and returns the value (0 to 1023)
        Internally sends b'RU{pin_number}' over the serial connection
        """
        command = f'RU{pin_number}'.encode()
        self.conn.write(command)
        line_received = self.conn.readline().decode().strip()
        header, value = line_received.split(':')
        if header == f'U{pin_number}':
            # If header matches
            return int(value)

    def analog_read(self, pin_number):
        """
        Performs an analog read on pin_number and returns the value (0 to 1023)
        Internally sends b'RA{pin_number}' over the serial connection
        """
        command = (''.join(('RA', str(pin_number)))).encode()
        self.conn.write(command)
        line_received = self.conn.readline().decode().strip()
        header, value = line_received.split(':')
        if header == ('A' + str(pin_number)):
            # If header matches
            return int(value)

    def analog_write(self, pin_number, analog_value):
        """
        Writes the analog value (0 to 255) on pin_number
        Internally sends b'WA{pin_number}:{analog_value}' over the serial connection
        """
        command = f'WA{pin_number}:{analog_value}'.encode()
        self.conn.write(command)

    def servo_write(self, pin_number, servo_pos):
        """
        Write the servo position to servo motor at pin_number
        Internally sends b'WS{pin_number}:{servo_pos}' over the serial connection
        """
        command = f'WS{pin_number}:{servo_pos}'.encode()
        print(command)
        self.conn.write(command)

    def close(self):
        """
        Terminate the connection to the Arduino device
        """
        self.conn.close()
        print('Connection to Arduino closed')