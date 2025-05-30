# from sensors import initialize_sensorbridge, initialize_sensor, print_values
import datetime
from src.SensorData import SensorData

# bridge = initialize_sensorbridge(port)
# sensor = initialize_sensor(bridge)

def flow_rate(sensor, seconds=30):
    print(f"Collecting flow rate data for {seconds} seconds")
    flow_data = []
    endTime = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
    while datetime.datetime.now() <= endTime:
        flow_data.append(sensor.read_continuous_measurement()[0])
    # print(flow_data)
    return flow_data

def temperature(sensor, seconds=30):
    print(f"Collecting temperature data for {seconds} seconds")
    temperature_data = []
    endTime = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
    while datetime.datetime.now() <= endTime:
        temperature_data.append(sensor.read_continuous_measurement()[1])
    # print(temperature_data)
    return temperature_data

def read_sensor_data(sensor, seconds=30):
    print(f"Collecting flow and temperature data for {seconds} seconds")
    flow_data = []
    temp_data = []
    endTime = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
    while datetime.datetime.now() <= endTime:
        flow_data.append(sensor.read_continuous_measurement()[0])
        temp_data.append(sensor.read_continuous_measurement()[1])
    return SensorData(seconds, flow_data, temp_data)

def average(data):
    average = sum(data)/len(data)
    return average

# print(f"Average Flow Rate: {average_flow}")
# print(f"Average Temperature: {average_temp}")

# Crumb catcher leak rate: (intake flow rate * time = total volume in) - (exhaust flow rate * time = total volume out) = difference
# % = (difference / total air volume moved) * 100 
# + leak rate is unwanted air getting in the system
# - leak rate is air getting out of the system
