import smbus
import time

def set_pwm_frequency(frequency, PCA9685_ADDRESS):
    # Set PWM frequency
    prescale_value = int(25000000.0 / (4096.0 * frequency) - 1.0)
    old_mode = bus.read_byte_data(PCA9685_ADDRESS, MODE1)
    new_mode = (old_mode & 0x7F) | 0x10  # Set sleep bit to allow writing to prescale
    bus.write_byte_data(PCA9685_ADDRESS, MODE1, new_mode)
    bus.write_byte_data(PCA9685_ADDRESS, PRESCALE, prescale_value)
    bus.write_byte_data(PCA9685_ADDRESS, MODE1, old_mode)
    time.sleep(0.005)
    bus.write_byte_data(PCA9685_ADDRESS, MODE1, old_mode | 0x80)  # Restart

def set_pwm(channel, on, off, PCA9685_ADDRESS):
    # Set PWM on and off values for the specified channel
    bus.write_byte_data(PCA9685_ADDRESS, LED0_ON_L + 4 * channel, on & 0xFF)
    bus.write_byte_data(PCA9685_ADDRESS, LED0_ON_L + 4 * channel + 1, on >> 8)
    bus.write_byte_data(PCA9685_ADDRESS, LED0_ON_L + 4 * channel + 2, off & 0xFF)
    bus.write_byte_data(PCA9685_ADDRESS, LED0_ON_L + 4 * channel + 3, off >> 8)

def turn_on_led(channel, address):
    set_pwm(channel, 0, 4095, address)  # Full brightness


def turn_off_led(channel, address):
    set_pwm(channel, 0, 0, address)  # Off
def init_pca_chip(address):
    bus.write_byte_data(address, MODE1, 0x00)
    set_pwm_frequency(1000, address) 

# I2C address of PCA9685
PCA9685_ADDRESS_1 = 0x40
PCA9685_ADDRESS_2 = 0x41

# Register addresses
MODE1 = 0x00
PRESCALE = 0xFE
LED0_ON_L = 0x06

# Open I2C bus
bus = smbus.SMBus(1)  # Use 0 for older Raspberry Pi boards

try:
    init_pca_chip(PCA9685_ADDRESS_1)
    init_pca_chip(PCA9685_ADDRESS_2)
    set_pwm_frequency(1000, PCA9685_ADDRESS_1)  # Set PWM frequency to 1000 Hz
    set_pwm_frequency(1000, PCA9685_ADDRESS_2)  # Set PWM frequency to 1000 Hz

    led_channel = 0

    while True:
        turn_on_led(led_channel, PCA9685_ADDRESS_1)
        turn_on_led(led_channel, PCA9685_ADDRESS_2)
        input("Press ENTER key to turn off...")
        turn_off_led(led_channel, PCA9685_ADDRESS_1)
        turn_off_led(led_channel, PCA9685_ADDRESS_2)
        input("Press ENTER key to turn on...")

except KeyboardInterrupt:
    # Handle Ctrl+C gracefully
    turn_off_led(led_channel, PCA9685_ADDRESS_1)
    turn_off_led(led_channel, PCA9685_ADDRESS_2)
    print("Script terminated by user.")

