from gpiozero import MCP3008
from time import sleep

## ========   ADC    ======================
# Define the ADC channel (0 to 7 for MCP3008)
adc_channels = [0, 1, 2]
voltages = [0.0] * len(adc_channels)
# Create MCP3008 object using SPI1 pins
## adc = MCP3008(channel=adc_channel, clock_pin=21, miso_pin=19, select_pin=16)
adc = [MCP3008(channel=chan, clock_pin=21, mosi_pin=20, miso_pin=19, select_pin=16) 
       for chan in adc_channels]


try:
    while True:
        ## ADC
        for i in range(len(adc_channels)):
            # Read the analog value
            adc_raw_value = adc[i].value
            # Convert the raw value to voltage (assuming VREF=3.3V)
            voltages[i] = adc_raw_value * 5.0
        # Print the results
        print(f"Voltage: {voltages} V")

        # Sleep for a short duration
        sleep(1)

except KeyboardInterrupt:
    print("Program terminated by user.")
finally:
    # Clean up GPIO resources
    [adc_chan.close() for adc_chan in adc ] 
