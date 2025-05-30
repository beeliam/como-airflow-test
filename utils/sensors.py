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
# port = ShdlcSerialPort(port='/dev/tty.usbserial-EKS2713NFH', baudrate=460800)

# Initialize Sensorbridge
def initialize_sensorbridge(port):
    bridge = SensorBridgeShdlcDevice(ShdlcConnection(port), slave_address=0)
    print("Initializing SensorBridge {}".format(bridge.get_serial_number()))
    print("setting i2c frequency")
    bridge.set_i2c_frequency(SensorBridgePort.ALL, frequency=SFM3019_DEFAULT_I2C_FREQUENCY)
    print("setting supply voltage")
    bridge.set_supply_voltage(SensorBridgePort.ALL, voltage=SFM3019_DEFAULT_VOLTAGE)
    print("setting switch supply on")
    bridge.switch_supply_on(SensorBridgePort.ALL)
    # print("sleeping...")
    # time.sleep(0.2)
    return bridge

# Initialize sensor:
# 1.) Stop any running measurement
# 2.) Request scale factors and unit set on sensor
# 3.) Start measurement
def initialize_sensor(bridge, port, measure_mode=MeasurementMode.Air, permille = 200): #port=SensorBridgePort.ONE
    print(f"initialize sensor {port}")
    sensor = Sfm3019I2cSensorBridgeDevice(bridge, port, slave_address=0x2E)
    sensor.initialize_sensor(measure_mode)
    sensor.start_continuous_measurement(measure_mode, air_o2_mix_fraction_permille=permille)
    print(f"initialized sensor {port}")
    return sensor

# Read out product information
def get_product_info(pid, sn, sensor):
    pid, sn = sensor.read_product_identifier_and_serial_number()
    print("SFM3019 SN: {}".format(sn))
    print("Flow unit of sensor: {} (Volume at temperature in degree Centigrade)".format(sensor.flow_unit))

# Read data out continuously
def print_values(sensor):
    while True:
        time.sleep(0.1)
        # print("Flow: {}, Temperature{}".format(*sensor.read_continuous_measurement()))
        print(sensor.read_continuous_measurement())


# # Define gas (or gas mixes)
# def define_measurement_mode():
#     measure_mode = MeasurementMode.Air
#     return measure_mode

# def define_permille():
#     permille = 200  # only applies for gas mixes
#     return permille