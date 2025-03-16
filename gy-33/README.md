The TCS3472 based color sensor GY-33 comes only with minimal public documentation [here](http://wiki.sunfounder.cc/index.php?title=GY-33_Color_Recognition_Sensor_Module).

Luckily [QuirkyCort](https://github.com/QuirkyCort) created the [micropython-gy33](https://github.com/QuirkyCort/micropython-gy33) library from some chinese documentation.

## LMS-ESP32 code:
```python
from pupremote import PUPRemoteSensor
from machine import Pin, SoftI2C
from neopixel import NeoPixel
from gy33_i2c import GY33_I2C # copy from https://github.com/QuirkyCort/micropython-gy33/blob/main/gy33-i2c/gy33_i2c.py

np = NeoPixel(Pin(25), 1) # onboard neopixel
np[0] = (255, 255, 0); np.write() # yellow = int

# connect GY-33 DR pin to LMS-ESP32 sda, CT pin to LMS-ESP32 scl
# to enable I2C mode, join solder pads near G+S0 pins or close pins with jumper
gy33 = GY33_I2C(i2c = SoftI2C(scl=Pin(4), sda=Pin(5), freq=100000))

def gyGet():
    return gy33.read_raw()

def gyLed(v):
    gy33.set_led(v)

rs = PUPRemoteSensor(power=False)
rs.add_command('gyGet', 'HHHH') # values 0~6000
rs.add_command('gyLed', '', 'B') # value 0-10
rs.process()

np[0] = (0, 255, 0); np.write() # green = ready

while True:
    rs.process()
```

## Pybricks code:

```python
from pybricks.pupdevices import ColorSensor
from pybricks.parameters import Port
from pybricks.tools import wait, StopWatch
from pupremote_hub import PUPRemoteHub # copy from https://github.com/antonvh/PUPRemote/blob/main/src/pupremote_hub.py
import gycolor

sw = StopWatch()
cs = ColorSensor(Port.F)
rh = PUPRemoteHub(Port.E)
rh.add_command('gyGet', 'HHHH')
rh.add_command('gyLed', '', 'B')
rh.call('gyLed', 10)

while True:
    gyRaw = rh.call('gyGet') # GY-33 color sensor. takes 13.5msec, dominated by communication with LMS-ESP32
    csHsv = cs.hsv()         # Lego color sensor. takes 0.04msec, but new value only each ~10msec
    csCol = cs.color()
    gyHsv = gycolor.rgbc_to_hsv_Color(*gyRaw)
    gyCol = gycolor.hsv_to_standard_Color(gyHsv)
    print(sw.time(), csHsv, csCol, '--', gyRaw, gyHsv, gyCol, sep=', ')
```

and create `gycolor.py` with content from this repo.

## Mounting the GY-33

The GY-33 sensor can be hot-glued into a Lego 87408 U connector, with 1/2 mm distance to ground. For better fit in the side rails, cut off the overhang on the upper side.

## Comparison

- Communication with the LMS-ESP32 is slow, but the effective sample rate is nearly comparable to the Lego color sensor.
- When using LMS-ESP32 attached sensors, e.g. in a PID based line follower, you can remove the usual `wait(10)` as the communication already takes that time.
