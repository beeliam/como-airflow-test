from sensirion_shdlc_sensorbridge import SensorBridgePort 
from sensirion_shdlc_driver import ShdlcSerialPort
from utils.sensors import find_bridges, initialize_bridge, initialize_sensor, async_measurement, flow_rate
from src.SensorData import SensorData
import threading
import queue
import sys

duration = 5

lower_bridge = None
upper_bridge = None

intake_sensor = None
exhaust_sensor_1 = None
exhaust_sensor_2 = None

bridge_addresses = find_bridges()
if len(bridge_addresses) != 2:
    print("ERROR: Bridge(s) is not attached!")
    if len(bridge_addresses) < 1:
        sys.exit(1)

serial_ports = []
threads = []
result_queue = queue.Queue()

for i, bridge_address in enumerate(bridge_addresses):

    serial_port = ShdlcSerialPort(port=bridge_address, baudrate=460800)
    serial_ports.append(serial_port)  # prevent GC + store for cleanup
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
        else: # Sensor not plugged into port
            if bridge_port == SensorBridgePort.TWO: # Port #2 on bridge has no sensor - assume this is lower_bridge
                lower_bridge = bridge
            else: # Should not hit this - means sensors are not connected properly
                print("ERROR: Sensor not detected in Port #1 for bridge(s)!")
                sys.exit(1)
            # print(f"skipped bridge port #{bridge_port+1} on bridge @ {bridge_address}\n")

# ------THREADING-------

# Start threads for all sensors in sensor list
for sensor in [intake_sensor, exhaust_sensor_1, exhaust_sensor_2]:
    if sensor:
        thread = threading.Thread(target=async_measurement, args=(sensor, duration, result_queue))
        thread.start()
        threads.append(thread)

# Wait for threads to finish
for thread in threads:
    thread.join()

sensor_data_list = []
while not result_queue.empty():
    flow_data = result_queue.get()
    sensor_data = SensorData(flow_data, duration)
    sensor_data_list.append(sensor_data)

# Print averaged results
for i, data in enumerate(sensor_data_list):
    print(f"Sensor #{i+1} average flow: {data.get_average_flow_rate():.2f} SLM")

# Clean up ports
for port in serial_ports:
    port.close()