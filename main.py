from utils.sensors import initialize_sensorbridge, initialize_sensor, print_values
from utils.testing import flow_rate, temperature, average, read_sensor_data
from sensirion_shdlc_driver import ShdlcSerialPort
from sensirion_shdlc_sensorbridge import SensorBridgePort

from utils.bridge_detect import find_sensor_bridge

bridge_port = find_sensor_bridge()

with ShdlcSerialPort(port=bridge_port, baudrate=460800) as port:

    bridge = initialize_sensorbridge(port)

    sensor = initialize_sensor(bridge, SensorBridgePort.ONE)
    flow = flow_rate(sensor,10)
    # print_values(sensorOne)
    # dataOne = read_sensor_data(sensorOne, 10)
    print(f'Sensor one flow data: {flow}')

    sensor = initialize_sensor(bridge, SensorBridgePort.TWO)
    flow = flow_rate(sensor,10)
    # print_values(sensorTwo)
    # dataTwo = read_sensor_data(sensorTwo, 10)
    print(f'Sensor two flow data: {flow}')

    # temp = temperature(sensor, 1)
    # average_flow = average(flow)
    # average_temp = average(temp)
    
    # average_sensor_flow = data.get_average_flow_rate()
    # average_sensor_temp = data.get_average_temp()