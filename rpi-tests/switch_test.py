import RPi.GPIO as GPIO
import time

# Set GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Set GPIO pin 22 as input
GPIO.setup(4, GPIO.IN)

try:
    # Set 3.3V pin as output and set it to HIGH
    # GPIO.setup(1, GPIO.OUT)  # GPIO 1 corresponds to the 3.3V pin
    # GPIO.output(1, GPIO.HIGH)

    # Read the input from GPIO 4
    while True:
        input_state = GPIO.input(4)
        print("GPIO 4 state:", input_state)
        time.sleep(0.1)

except KeyboardInterrupt:
    pass

finally:
    # Clean up GPIO settings
    GPIO.cleanup()

