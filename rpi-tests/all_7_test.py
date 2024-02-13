import RPi.GPIO as GPIO
import time

# Set GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Set GPIO pin 22 as input

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

try:
    while True:
        for i in range(7):
            input_states[i] = GPIO.input(input_pins[i])
        print(f"Input \n{input_pins} \n{input_states}")
        time.sleep(0.5)
except KeyboardInterrupt:
    pass

finally:
    # Clean up GPIO settings
    GPIO.cleanup()

