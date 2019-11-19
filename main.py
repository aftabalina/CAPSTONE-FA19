import logging
import sys
import time
import RPi.GPIO as IO

from Adafruit_BNO055 import BNO055

bno = BNO055.BNO055(serial_port='/dev/serial0', rst=18)

# Enable verbose debug logging if -v is passed as a parameter.
if len(sys.argv) == 2 and sys.argv[1].lower() == '-v':
    logging.basicConfig(level=logging.DEBUG)

# Initialize the BNO055 and stop if something went wrong.
if not bno.begin():
    raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

# Print system status and self test result.
status, self_test, error = bno.get_system_status()
print('System status: {0}'.format(status))
print('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
# Print out an error if system status is in error mode.
if status == 0x01:
    print('System error: {0}'.format(error))
    print('See datasheet section 4.3.59 for the meaning.')

# Print BNO055 software revision and other diagnostic data.
sw, bl, accel, mag, gyro = bno.get_revision()
print('Software version:   {0}'.format(sw))
print('Bootloader version: {0}'.format(bl))
print('Accelerometer ID:   0x{0:02X}'.format(accel))
print('Magnetometer ID:    0x{0:02X}'.format(mag))
print('Gyroscope ID:       0x{0:02X}\n'.format(gyro))

print('Reading BNO055 data, press Ctrl-C to quit...')

#VARIBALES
CALIBRATION_PIN = 19
NORTH = 20
SOUTH = 26
EAST = 21
WEST = 16
PINS = [CALIBRATION_PIN, NORTH, SOUTH, EAST, WEST] #Calibration_pin, NSEW

def calibrate_system():
    while True:
        sys, gyro, accel, mag = bno.get_calibration_status()
        if(sys == 3):
            print("System calibrated")
            IO.output(CALIBRATION_PIN, True)
            break;
        
def setup_GPIO():
    IO.setmode(IO.BOARD)
    for pin in PINS:
        IO.setup(pin, IO.OUT)
    

setup_GPIO()
calibrate_system()
    
while True:
    command = raw_input("enter q to quit")
    if(command == "q"):
        break;

IO.cleanup()    
    

