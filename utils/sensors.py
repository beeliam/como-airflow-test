import logging
import time

from sensirion_shdlc_driver import ShdlcSerialPort, ShdlcConnection
from sensirion_shdlc_sensorbridge import SensorBridgePort, SensorBridgeShdlcDevice

from sensirion_sensorbridge_i2c_sfm.sfm3019 import Sfm3019I2cSensorBridgeDevice, MeasurementMode
from sensirion_sensorbridge_i2c_sfm.sfm3019.sfm3019_constants import SFM3019_DEFAULT_I2C_FREQUENCY, \
    SFM3019_DEFAULT_VOLTAGE

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', level=logging.ERROR)

# Connect to the SensorBridge with default settings:
#  - baudrate:      460800
#  - slave address: 0
port = ShdlcSerialPort(port='/dev/tty.usbserial-EKS2713NFH', baudrate=460800)

# Initialize Sensorbridge
def initialize_sensorbridge(port):
    bridge = SensorBridgeShdlcDevice(ShdlcConnection(port), slave_address=0)
    # print("SensorBridge SN: {}".format(bridge.get_serial_number()))
    bridge.set_i2c_frequency(SensorBridgePort.ONE, frequency=SFM3019_DEFAULT_I2C_FREQUENCY)
    bridge.set_supply_voltage(SensorBridgePort.ONE, voltage=SFM3019_DEFAULT_VOLTAGE)
    bridge.switch_supply_on(SensorBridgePort.ONE)
    return bridge

# Define gas (or gas mixes)
def define_measurement_mode():
    measure_mode = MeasurementMode.Air
    return measure_mode

def define_permille():
    permille = 200  # only applies for gas mixes
    return permille

# Initialize sensor:
# 1.) Stop any running measurement
# 2.) Request scale factors and unit set on sensor
# 3.) Start measurement
def initialize_sensor(bridge, measure_mode=MeasurementMode.Air, permille = 200):
    sensor = Sfm3019I2cSensorBridgeDevice(bridge, SensorBridgePort.ONE, slave_address=0x2E)
    measure_mode = MeasurementMode.Air
    permille = 200
    sensor.initialize_sensor(measure_mode)
    sensor.start_continuous_measurement(measure_mode, air_o2_mix_fraction_permille=permille)
    return sensor

# Read out product information
def get_product_info(pid, sn, sensor):
    pid, sn = sensor.read_product_identifier_and_serial_number()
    print("SFM3019 SN: {}".format(sn))
    print("Flow unit of sensor: {} (Volume at temperature in degree Centigrade)".format(sensor.flow_unit))

# Read them out continuously
def print_values(sensor):
    while True:
        time.sleep(0.1)
        # print("Flow: {}, Temperature{}".format(*sensor.read_continuous_measurement()))
        print(sensor.read_continuous_measurement())