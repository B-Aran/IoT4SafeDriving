"""
This example demonstrates how to instantiate the
Adafruit BNO055 Sensor using this library and just
the I2C bus number.
This example will only work on a Raspberry Pi
and does require the i2c-gpio kernel module to be
installed and enabled. Most Raspberry Pis will
already have it installed, however most do not
have it enabled. You will have to manually enable it
"""

import time
from adafruit_extended_bus import ExtendedI2C as I2C
import adafruit_bno055

# To enable i2c-gpio, add the line `dtoverlay=i2c-gpio` to /boot/config.txt
# Then reboot the pi

# Create library object using our Extended Bus I2C port
# Use `ls /dev/i2c*` to find out what i2c devices are connected
i2c = I2C(3)  # Device is /dev/i2c-3, try command: i2cdetect -y -r <port number> in order to know the port number
sensor = adafruit_bno055.BNO055_I2C(i2c)

while True:
    # print("Temperature: {} degrees C".format(sensor.temperature))
    # print("Accelerometer (m/s^2): {}".format(sensor.acceleration))
    # print("Magnetometer (microteslas): {}".format(sensor.magnetic))
    # print("Gyroscope (rad/sec): {}".format(sensor.gyro))
    print("Euler angle: {}".format(sensor.euler)) # list with (yaw, roll, pitch) angles
    # print("Quaternion: {}".format(sensor.quaternion))
    # print("Linear acceleration (m/s^2): {}".format(sensor.linear_acceleration))
    # print("Gravity (m/s^2): {}".format(sensor.gravity))
    print()

    time.sleep(0.1) # Set time in seconds to set frequency Hz
