import time
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685

# Initialize I2C
i2c = busio.I2C(SCL, SDA)

# Initialize PCA9685
pca = PCA9685(i2c)
pca.frequency = 1000  # Set PWM frequency (in Hz)

# LED channel on PCA9685
led_channel = 0

def turn_on_led(channel):
    pca.channels[channel].duty_cycle = 0xFFFF  # Full brightness

def turn_off_led(channel):
    pca.channels[channel].duty_cycle = 0x0000  # Off

try:
    while True:
        turn_on_led(led_channel)
        time.sleep(2)
        turn_off_led(led_channel)
        time.sleep(2)

except KeyboardInterrupt:
    # Handle Ctrl+C gracefully
    turn_off_led(led_channel)
    print("Script terminated by user.")
