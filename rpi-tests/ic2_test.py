from gpiozero import OutputDevice
from time import sleep
import smbus

# I2C address of the PWM driver (PCA9685)
pwm_address = 0x40

# Initialize the I2C bus (0 on older Pi models, 1 on Pi 2 and later)
i2c_bus = smbus.SMBus(1)

# def read_byte_from_register(register):
#     # Read a byte from the specified register
#     return i2c_bus.read_byte_data(pwm_address, register)
#
# try:
#     # Read and print some key registers
#     mode_register = read_byte_from_register(0x00)
#     prescale_register = read_byte_from_register(0xFE)
#     on_l_register = read_byte_from_register(0x06)
#
#     print(f'Mode Register (MODE1): 0x{mode_register:02X}')
#     print(f'Prescale Register (PRE_SCALE): 0x{prescale_register:02X}')
#     print(f'LED0_ON_L Register: 0x{on_l_register:02X}')
#
# except Exception as e:
#     print(f"Error: {e}")
#
#
# PCA9685 registers
MODE1 = 0x00
PRESCALE = 0xFE
LED0_ON_L = 0x06

# Configure PCA9685
i2c_bus.write_byte_data(pwm_address, MODE1, 0x00)  # Reset MODE1 (turn off auto-increment)

# Set the PWM frequency (40 Hz is a common choice)
prescale_value = int(25e6 / (4096 * 40) - 1)
i2c_bus.write_byte_data(pwm_address, PRESCALE, prescale_value)

# Enable the PCA9685 oscillator
i2c_bus.write_byte_data(pwm_address, MODE1, 0x80)
i2c_bus.write_byte_data(pwm_address, 0x06, 0x80)  # Set ON time to 50% duty cycle
# Create an OutputDevice object for the LED connected to channel 0
led_channel = 0
led = OutputDevice(led_channel)

try:
    while True:
        # Turn on the LED
        print('LED on')
        led.on()
        sleep(2)
        input("Press Enter to turn off...")
        # Turn off the LED
        print('turning off')
        led.off()
        sleep(2)

except KeyboardInterrupt:
    pass

finally:
    # Clean up resources
    led.close()
    i2c_bus.close()
