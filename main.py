from sensirion_shdlc_sensorbridge import SensorBridgePort, SensorBridgeShdlcDevice
from sensirion_shdlc_driver import ShdlcSerialPort
from utils.sensors import find_bridges, initialize_bridge, initialize_sensor, flow_rate, temperature
from src.SensorData import SensorData
import sys

duration = 2
sensor_data_instances = []

lower_bridge = None
upper_bridge = None

intake_sensor = None
exhaust_sensor_1 = None
exhuast_sensor_2 = None

bridge_addresses = find_bridges()
if len(bridge_addresses) != 2:
    print("ERROR: Bridge(s) is not attached!")
    sys.exit(1)


for i, bridge_address in enumerate(bridge_addresses):

    with ShdlcSerialPort(port=bridge_address, baudrate=460800) as serial_port:
        bridge = initialize_bridge(serial_port)

        for bridge_port in [SensorBridgePort.TWO, SensorBridgePort.ONE]: # Start with port #2 to determine which bridge we're on in first iteration of loop
            sensor = initialize_sensor(bridge, bridge_port)

            if sensor: # Sensor is plugged into port
                if bridge_port == SensorBridgePort.TWO: # Port #2 on bridge has sensor connected - assume this is upper_bridge
                    upper_bridge = bridge
                    exhaust_sensor_1 = sensor
                else: # If we're on port #1 then we should have already determined what bridge we're on
                    if lower_bridge:
                        exhaust_sensor_2 = sensor
                    else:
                        intake_sensor = sensor
            
                # print(f"\nstarting bridge port #{bridge_port+1} on bridge @ {bridge_address}\n")
                # flow = flow_rate(sensor, duration) #TODO: move to thread
                # temp = temperature(sensor, duration) #don't care about temp
                # sensor_data_instances.append(SensorData(duration, flow)) #Create SensorData object with duration and flow data then save into list
            else: # Sensor not plugged into port
                if bridge_port == SensorBridgePort.TWO: # Port #2 on bridge has no sensor - assume this is lower_bridge
                    lower_bridge = bridge
                else: # Should not hit this - means sensors are not connected properly
                    print("ERROR: Sensor not detected in Port #1 for bridge(s)!")
                    sys.exit(1)
                # print(f"skipped bridge port #{bridge_port+1} on bridge @ {bridge_address}\n")
              

for i, data in enumerate(sensor_data_instances):
    print(f'bridge port #{i+1} average flow: ({data.get_average_flow_rate()}) SLM')

# avg_flow_rate = SensorData.get_average_flow_rate(data)

# print(avg_flow_rate)