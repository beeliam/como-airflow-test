from sensirion_shdlc_sensorbridge import SensorBridgePort
from sensirion_shdlc_driver import ShdlcSerialPort
from utils.sensors import find_sensor_bridges, initialize_sensorbridge, initialize_sensor, flow_rate, temperature
from src.SensorData import SensorData

duration = 2
bridge_ports = find_sensor_bridges()

for i, bridge_port  in enumerate(bridge_ports):
    # print(" ")
    # print(f"Using bridge {i+1} on port {bridge_port}")

    with ShdlcSerialPort(port=bridge_port, baudrate=460800) as port:

        bridge = initialize_sensorbridge(port)

        for sensor_port in [SensorBridgePort.ONE, SensorBridgePort.TWO]:
            sensor = initialize_sensor(bridge, sensor_port)
            if sensor:
                print(" ")
                print(f"Starting port: {sensor_port+1} on Sensor Bridge: {bridge_port}")
                flow = flow_rate(sensor, duration)
                # temp = temperature(sensor, duration)
                print(" ")
               
            else:
                print(f"Skipped port: {sensor_port+1} on Sensor Bridge: {bridge_port}")
                print(" ")
              

data = SensorData(duration, flow)

avg_flow_rate = SensorData.get_average_flow_rate(data)

print(avg_flow_rate)