import RPi.GPIO as GPIO
import time

# Set GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Set GPIO pin 22 as input
GPIO.setup(22, GPIO.IN)
# Set GPIO pin 27 as another input
GPIO.setup(27, GPIO.IN)

try:
    # Set GPIO 17 as output and set it to HIGH
    GPIO.setup(17, GPIO.OUT)  # GPIO 17 as an example
    GPIO.output(17, GPIO.HIGH)

    # Read the input from GPIO 22
    while True:
        input_state_22 = GPIO.input(22)
        input_state_27 = GPIO.input(27)
        print(f"GPIO 22 state: {input_state_22}, GPIO 27 state: {input_state_27}")
        time.sleep(0.1)

except KeyboardInterrupt:
    pass

finally:
    # Clean up GPIO settings
    GPIO.cleanup()
