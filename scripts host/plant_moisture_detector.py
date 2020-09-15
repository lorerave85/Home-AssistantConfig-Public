import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import time
import json

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
chan0 = AnalogIn(mcp, MCP.P0)

chan1 = AnalogIn(mcp, MCP.P1)
chan2 = AnalogIn(mcp, MCP.P2)
chan3 = AnalogIn(mcp, MCP.P3)
chan4 = AnalogIn(mcp, MCP.P4)
chan5 = AnalogIn(mcp, MCP.P5)
chan6 = AnalogIn(mcp, MCP.P6)
chan7 = AnalogIn(mcp, MCP.P7)

def remap_range(value, left_min, left_max, right_min, right_max):
    # this remaps a value from original (left) range to new (right) range
    # Figure out how 'wide' each range is
    left_span = left_max - left_min
    right_span = right_max - right_min
 
    # Convert the left range into a 0-1 range (int)
    valueScaled = int(value - left_min) / int(left_span)
 
    # Convert the 0-1 range into a value in the right range.
    return int(right_min + (valueScaled * right_span))

data = {}

data["ch0"]= remap_range(chan0.value, 0, 65535, 0, 100)
data["ch1"]= remap_range(chan1.value, 0, 65535, 0, 100)
data["ch2"]= remap_range(chan2.value, 0, 65535, 0, 100)
data["ch3"]= remap_range(chan3.value, 0, 65535, 0, 100)
data["ch4"]= remap_range(chan4.value, 0, 65535, 0, 100)
data["ch5"]= remap_range(chan5.value, 0, 65535, 0, 100)
data["ch6"]= remap_range(chan6.value, 0, 65535, 0, 100)
data["ch7"]= remap_range(chan7.value, 0, 65535, 0, 100)
json_data = json.dumps(data) # Convert the dictionary to a JSON string
print(json_data)

