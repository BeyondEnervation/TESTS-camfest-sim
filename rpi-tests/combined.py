from gpiozero import MCP3008
import RPi.GPIO as GPIO
from time import sleep
import smbus
from itertools import chain 

def set_pwm_frequency(frequency, PCA9685_ADDRESS):
    # Set PWM frequency
    prescale_value = int(25000000.0 / (4096.0 * frequency) - 1.0)
    old_mode = bus.read_byte_data(PCA9685_ADDRESS, MODE1)
    new_mode = (old_mode & 0x7F) | 0x10  # Set sleep bit to allow writing to prescale
    bus.write_byte_data(PCA9685_ADDRESS, MODE1, new_mode)
    bus.write_byte_data(PCA9685_ADDRESS, PRESCALE, prescale_value)
    bus.write_byte_data(PCA9685_ADDRESS, MODE1, old_mode)
    sleep(0.005)
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

## ========   I2C    ======================
# I2C address of PCA9685
PCA9685_ADDRESS_1 = 0x40
PCA9685_ADDRESS_2 = 0x41
# Register addresses
MODE1 = 0x00
PRESCALE = 0xFE
LED0_ON_L = 0x06
# Open I2C bus
bus = smbus.SMBus(1)  # Use 0 for older Raspberry Pi boards

## ========   ADC    ======================
# Define the ADC channel (0 to 7 for MCP3008)
adc_channels = [0, 1, 2]
voltages = [0.0] * len(adc_channels)
# Create MCP3008 object using SPI1 pins
## adc = MCP3008(channel=adc_channel, clock_pin=21, miso_pin=19, select_pin=16)
adc = [MCP3008(channel=chan, clock_pin=21, mosi_pin=20, miso_pin=19, select_pin=16) 
       for chan in adc_channels]

## ========== SWITCHES AND BUTTONS =========
# Set GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

## Switch 1 = GPIO 4
GPIO.setup(4, GPIO.IN)
## Switch 2 = GPIO 17
GPIO.setup(17, GPIO.IN)
## Switch 3 = GPIO 27
GPIO.setup(27, GPIO.IN)
## Switch 4 = GPIO 22
GPIO.setup(22, GPIO.IN)
## Switch 5 = GPIO 10 
GPIO.setup(10, GPIO.IN)
## Button 1 = GPIO 9
GPIO.setup(9, GPIO.IN)
## Button 2 = GPIO 11
GPIO.setup(11, GPIO.IN)
input_pins = [4, 17, 27, 22, 10, 9, 11]
input_states = [0, 0, 0, 0, 0, 0, 0]

## ========== LEDS =========
## Create groups 
lever_leds = [1, 2, 3, 4, 5, 6, 19, 20, 21]
top_reactor_leds = [7, 8, 9] 
left_button_leds = [13, 14, 15]
right_button_leds = [16, 17, 18]
top_switch = [12, 11, 10]
top_middle_switch = [24, 23, 22]
middle_switch = [25, 26, 27]
bottom_middle_switch = [28, 29, 30]
bottom_switch = [31, 32]
## ========================================

board_no = 1
try:
    init_pca_chip(PCA9685_ADDRESS_1)
    init_pca_chip(PCA9685_ADDRESS_2)
    set_pwm_frequency(1000, PCA9685_ADDRESS_1)  # Set PWM frequency to 1000 Hz
    set_pwm_frequency(1000, PCA9685_ADDRESS_2)  # Set PWM frequency to 1000 Hz

    while True:
        ## I2C 
        for led in chain(lever_leds, top_reactor_leds, left_button_leds, right_button_leds, 
                       top_switch, top_middle_switch, middle_switch, bottom_middle_switch, bottom_switch ):
            print(f"LED No. {led}")
            led -= 1
            try:
                if led >= 16:
                    board_no = 2 
                    turn_on_led(led-16, PCA9685_ADDRESS_2)
                    sleep(0.05)
                    # input("Cont?:")
                    turn_off_led(led-16, PCA9685_ADDRESS_2)
                    
                elif (led >= 0 or led <= 15):
                    board_no = 1 
                    turn_on_led(led, PCA9685_ADDRESS_1)
                    sleep(0.05)
                    # input("Cont?:")
                    turn_off_led(led, PCA9685_ADDRESS_1)
                else:
                    print("WE'VE FUCKED IT???!?!??!")
            except KeyboardInterrupt: 
                if board_no == 1:
                    turn_off_led(led, PCA9685_ADDRESS_1)
                elif board_no ==2: 
                    turn_off_led(led, PCA9685_ADDRESS_2)
                exit()
            except:
                print(f"Error in LED {led}")
                continue
        """
        for led in [17, 18, 20, 21, 
            print(f"LED No. {led}")
            led -= 1
            if led >= 16:
                turn_on_led(led, PCA9685_ADDRESS_2)
                sleep(1.1)
                input("Enter to cont...")
                turn_off_led(led, PCA9685_ADDRESS_2)
            elif (led >= 0 or led <= 15):
                turn_on_led(led, PCA9685_ADDRESS_1)
                sleep(1.1)
                input("Enter to cont...")
                turn_off_led(led, PCA9685_ADDRESS_1)
            else:
                print("WE'VE FUCKED IT???!?!??!")
        """
        ##---------------------------------------
        ## ADC
        for i in range(len(adc_channels)):
            # Read the analog value
            adc_raw_value = adc[i].value
            # Convert the raw value to voltage (assuming VREF=3.3V)
            voltages[i] = adc_raw_value * 5.0
        # Print the results
        print(f"Voltage: {voltages} V")

        ## SWITCHES AND BUTTON
        for i in range(7):
            input_states[i] = GPIO.input(input_pins[i])
        print(f"Input \n{input_pins} \n{input_states}")

        ## Sleep for a short duration
        sleep(1)

except KeyboardInterrupt:
    print("Program terminated by user.")
    turn_off_led(led_channel, PCA9685_ADDRESS_1)
    turn_off_led(led_channel, PCA9685_ADDRESS_2)
finally:
    # Clean up GPIO resources
    for adc_chan in adc:
        adc_chan.close()
    # Clean up GPIO settings
    GPIO.cleanup()
