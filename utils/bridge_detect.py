import serial.tools.list_ports

def get_port_information():
    for port in serial.tools.list_ports.comports():
        print(f'{port.device}')
        print(f'{port.manufacturer}')
        print(f'{port.description}')
        print(f'{port.serial_number}')

def find_sensor_bridge():
    for port in serial.tools.list_ports.comports():
        if port.manufacturer == 'Sensirion' and port.description == 'EKS2':
            return port.device

sensor_bridge = find_sensor_bridge()
# print(sensor_bridge)
