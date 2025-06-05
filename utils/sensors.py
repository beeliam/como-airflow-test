import datetime
import logging
import time
import serial.tools.list_ports

from src.SensorData import SensorData

from sensirion_shdlc_driver import ShdlcConnection
from sensirion_shdlc_driver.errors import ShdlcDeviceError, ShdlcTimeoutError
from sensirion_shdlc_sensorbridge import SensorBridgePort, SensorBridgeShdlcDevice

from sensirion_sensorbridge_i2c_sfm.sfm3019 import Sfm3019I2cSensorBridgeDevice, MeasurementMode
from sensirion_sensorbridge_i2c_sfm.sfm3019.sfm3019_constants import SFM3019_DEFAULT_I2C_FREQUENCY, \
    SFM3019_DEFAULT_VOLTAGE

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', level=logging.ERROR)

#check device data to identify sensor bridges
def find_bridges():
    """check serial port data to identify sensirion sensor bridges"""
    bridges=[]
    for port in serial.tools.list_ports.comports():
        # print(f"Checking {port}")
        if port.manufacturer == 'Sensirion' and port.description == 'EKS2':
            print(f"Found Sensirion Bridge: {port.device}")
            bridges.append(port.device)
    return bridges

# initialize Sensorbridge
def initialize_bridge(serial_port):
    """initialize sensirion sensor bridge"""
    try:
        logging.info(f"Attempting to open bridge at {serial_port}")
        bridge = SensorBridgeShdlcDevice(ShdlcConnection(serial_port), slave_address=0)
        logging.info("Initializing SensorBridge {}".format(bridge.get_serial_number()))
        # print("setting i2c frequency")
        bridge.set_i2c_frequency(SensorBridgePort.ALL, frequency=SFM3019_DEFAULT_I2C_FREQUENCY)
        # print("setting supply voltage")
        bridge.set_supply_voltage(SensorBridgePort.ALL, voltage=SFM3019_DEFAULT_VOLTAGE)
        # print("setting switch supply on")
        bridge.switch_supply_on(SensorBridgePort.ALL)
        return bridge # sensirion bridge object !!!
    except Exception as e:
        logging.warning(f"Failed to initialize bridge at {serial_port}: {e}")
        return None, None

# initialize sensor and start measurement
def initialize_sensor(bridge, bridge_port, measure_mode=MeasurementMode.Air, permille = 200): #port=SensorBridgePort.ONE
    """initialize individual sensors connected to sensor bridge ports"""
    try:
        logging.info(f"Attempting to initialize sensor on {bridge_port}")
        sensor = Sfm3019I2cSensorBridgeDevice(bridge, bridge_port, slave_address=0x2E)
        sensor.initialize_sensor(measure_mode)
        sensor.start_continuous_measurement(measure_mode, air_o2_mix_fraction_permille=permille)
        logging.info(f"initialized sensor {bridge_port}")
        return sensor
    except (ShdlcDeviceError, ShdlcTimeoutError, AttributeError, OSError) as e:
        logging.warning(f"No sensor found on {bridge_port} or failed to initialize -- skipping. ({type(e).__name__}")

#start flow_rate measurement
def flow_rate(sensor, seconds=30): # sensirion sensor object
    """begin collecting flow rate data over a specified time interval"""
    print(f"collecting flow rate data for {seconds} seconds")
    flow_data = []
    endTime = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
    while datetime.datetime.now() <= endTime:
        flow_data.append(sensor.read_continuous_measurement()[0])
    # print(flow_data)
    return flow_data

#start temperature measurement
def temperature(sensor: Sfm3019I2cSensorBridgeDevice, seconds=30):
    """begin collecting temperature data over a specified time interval"""
    print(f"collecting temperature data for {seconds} seconds")
    temperature_data = []
    endTime = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
    while datetime.datetime.now() <= endTime:
        temperature_data.append(sensor.read_continuous_measurement()[1])
    # print(temperature_data)
    return temperature_data

def sync_measurement(sensor: Sfm3019I2cSensorBridgeDevice, seconds: int, result_queue, sensor_label=None):
    print(f"collecting flow rate data for {seconds} seconds on {sensor_label}")
    flow_data = []
    sample_interval = 0.1 #100ms
    # print(f"[{sensor_label}] Flow: {flow_data}")
    endTime = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
    while datetime.datetime.now() <= endTime:
        flow_data.append(sensor.read_continuous_measurement()[0])
        # print(f"[{sensor_label}] Flow: {sensor.read_continuous_measurement()[0]}")
        time.sleep(sample_interval)
    # print(flow_data)
    result_queue.put((sensor_label, flow_data))
    # return sn
    
# print out product information
def get_product_info(pid, sn, sensor):
    """read out product information for sensors"""
    pid, sn = sensor.read_product_identifier_and_serial_number()
    print("SFM3019 SN: {}".format(sn))
    print("Flow unit of sensor: {} (Volume at temperature in degree Centigrade)".format(sensor.flow_unit))

# print sensor data continuously
def print_values(sensor: Sfm3019I2cSensorBridgeDevice):
    """continuously print sensor values to terminal"""
    while True:
        time.sleep(0.1)
        # print("Flow: {}, Temperature{}".format(*sensor.read_continuous_measurement()))
        print(sensor.read_continuous_measurement())