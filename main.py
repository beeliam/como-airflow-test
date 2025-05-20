from utils.sensors import initialize_sensorbridge, initialize_sensor, print_values
from utils.testing import flow_rate, temperature, average, read_sensor_data
from sensirion_shdlc_driver import ShdlcSerialPort

from utils.bridge_detect import find_sensor_bridge

bridge_port = find_sensor_bridge()

with ShdlcSerialPort(port=bridge_port, baudrate=460800) as port:

    bridge = initialize_sensorbridge(port)
    sensor = initialize_sensor(bridge)
    # flow = flow_rate(sensor, 1)
    # temp = temperature(sensor, 1)
    # average_flow = average(flow)
    # average_temp = average(temp)

    data = read_sensor_data(sensor, 10)
    average_sensor_flow = data.get_average_flow_rate()
    average_sensor_temp = data.get_average_temp()
    

print(average_sensor_flow)
print(average_sensor_temp)
