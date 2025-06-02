import datetime

class SensorData:
    def __init__(self, flow_rate, duration, sensor_label=None, temperature=None)-> None:
        self.duration = duration # duration of readings - seconds
        self.flow_rate: list[float] = flow_rate # list of readings - SLM
        self.sensor_label = sensor_label
        self.temperature: list[float] = temperature if temperature is not None else [] # list of reading - Celsius
       
    def get_average_temp(self) -> float:
        return sum(self.temperature)/len(self.temperature)
    
    def get_average_flow_rate(self) -> float:
        return sum(self.flow_rate)/len(self.flow_rate)

