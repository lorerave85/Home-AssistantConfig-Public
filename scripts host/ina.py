import logging
import json
from ina219 import INA219
from ina219 import DeviceRangeError

SHUNT_OHMS = 0.1

ina = INA219(SHUNT_OHMS, address=0x40, log_level=logging.ERROR)
ina.configure()

try:
    #print("Bus Voltage: %.3f V" % ina.voltage())
    #print("Bus Current: %.3f mA" % ina.current())
    #print("Power: %.3f mW" % ina.power())
    #print("Shunt voltage: %.3f mV" % ina.shunt_voltage())
    x = {
        "Bus_Voltage": ina.voltage(),
        "Bus_Current": ina.current(),
        "Power": ina.power(),
        "Shunt_voltage": ina.shunt_voltage()  
    }
    y = json.dumps(x)
    print(y)
except DeviceRangeError as e:
    # Current out of device range with specified shunt resistor
    print(e)

