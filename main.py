from sensirion_shdlc_sensorbridge import SensorBridgePort
from sensirion_shdlc_driver import ShdlcSerialPort
from utils.sensors import find_bridges, initialize_bridge, initialize_sensor, flow_rate, temperature
from src.SensorData import SensorData

duration = 2
bridge_addresses = find_bridges()
sensor_data_instances = []

for i, bridge_address in enumerate(bridge_addresses):
    # print(" ")
    # print(f"Using bridge {i+1} on port {bridge_address}")

    with ShdlcSerialPort(port=bridge_address, baudrate=460800) as serial_port:

        bridge = initialize_bridge(serial_port)

        for bridge_port in [SensorBridgePort.ONE, SensorBridgePort.TWO]:
            sensor = initialize_sensor(bridge, bridge_port)
            if sensor:
                print(f"\nstarting bridge port #{bridge_port+1} on bridge @ {bridge_address}\n")
                flow = flow_rate(sensor, duration)
                # temp = temperature(sensor, duration) #don't care about temp
                sensor_data_instances.append(SensorData(duration, flow)) #Create SensorData object with duration and flow data then save into list
               
            else:
                print(f"skipped bridge port #{bridge_port+1} on bridge @ {bridge_address}\n")
              

for i, data in enumerate(sensor_data_instances):
    print(f'bridge port #{i+1} average flow: ({data.get_average_flow_rate()}) SLM')

# avg_flow_rate = SensorData.get_average_flow_rate(data)

# print(avg_flow_rate)