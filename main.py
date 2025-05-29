from utils.sensors import initialize_sensorbridge, initialize_sensor_one, initialize_sensor_two, print_values
from utils.testing import flow_rate, temperature, average, read_sensor_data
from sensirion_shdlc_driver import ShdlcSerialPort

from utils.bridge_detect import find_sensor_bridge

bridge_port = find_sensor_bridge()

with ShdlcSerialPort(port=bridge_port, baudrate=460800) as port:

    bridge = initialize_sensorbridge(port)

    # sensorOne = initialize_sensor_one(bridge)
    # flowOne = flow_rate(sensorOne)
    # print_values(sensorOne)
    # dataOne = read_sensor_data(sensorOne, 10)
    # print(dataOne)

    sensorTwo = initialize_sensor_two(bridge)
    flowTwo = flow_rate(sensorTwo)
    print_values(sensorTwo)
    # dataTwo = read_sensor_data(sensorTwo, 10)
    # print(dataTwo)


    # temp = temperature(sensor, 1)
    # average_flow = average(flow)
    # average_temp = average(temp)
    
    
    # average_sensor_flow = data.get_average_flow_rate()
    # average_sensor_temp = data.get_average_temp()
  

# print(average_sensor_flow)
# print(average_sensor_temp)
# print(flow)
# print(flowTwo)
