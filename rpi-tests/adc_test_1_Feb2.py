import spidev
import time

# SPI Configuration
SPI_BUS = 0  # SPI bus (0 or 1)
SPI_DEVICE = 1  # SPI device (0 or 1)
SPI_SPEED = 1000000  # SPI speed in Hz

# MCP3008 configuration
CHANNEL = 0  # ADC channel to read (0 to 7)

# Open SPI bus
spi = spidev.SpiDev()
spi.open(SPI_BUS, SPI_DEVICE)
spi.max_speed_hz = SPI_SPEED

def read_adc(channel):
    # MCP3008 command format: 0b1 | single-ended | channel (3 bits)
    command = 0b11000000 | (channel << 4)
    adc_data = spi.xfer2([command, 0x00, 0x00])

    # Extract ADC value from received data
    adc_value = ((adc_data[0] & 0x03) << 8) + adc_data[1]
    return adc_value

try:
    outs = [0.0]*7
    while True:
        for chan in range(0,7):
            outs[chan] = read_adc(chan)
        print("Outputs: \n", outs)
        # print(f"ADC Value on Channel {CHANNEL}: {adc_value}")
        time.sleep(1)

except KeyboardInterrupt:
    # Handle Ctrl+C gracefully
    spi.close()
    print("Script terminated by user.")

