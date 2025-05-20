from sensors import initialize_sensorbridge, initialize_sensor, print_values
from sensors import port
import datetime

bridge = initialize_sensorbridge(port)
sensor = initialize_sensor(bridge)

def flow_rate(seconds):
    flow_data = []
    endTime = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
    while datetime.datetime.now() <= endTime:
        flow_data.append(sensor.read_continuous_measurement()[0])
    # print(flow_data)
    return flow_data

def temperature(seconds):
    temperature_data = []
    endTime = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
    while datetime.datetime.now() <= endTime:
        temperature_data.append(sensor.read_continuous_measurement()[1])
    # print(temperature_data)
    return temperature_data

def average(data):
    average = sum(data)/len(data)
    return average

# print(f"Average Flow Rate: {average_flow}")
# print(f"Average Temperature: {average_temp}")

# Crumb catcher leak rate: (intake flow rate * time = total volume in) - (exhaust flow rate * time = total volume out) = difference
# % = (difference / total air volume moved) * 100 
# + leak rate is unwanted air getting in the system
# - leak rate is air getting out of the system
