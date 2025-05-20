from utils.sensors import initialize_sensorbridge, initialize_sensor, print_values
from utils.sensors import port

bridge = initialize_sensorbridge(port)
sensor = initialize_sensor(bridge)

print_values(sensor)

