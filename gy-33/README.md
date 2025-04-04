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
import gy33_color # copy from example folder

sw = StopWatch()
cs = ColorSensor(Port.F)
rh = PUPRemoteHub(Port.E)
rh.add_command('gyGet', 'HHHH')
rh.add_command('gyLed', '', 'B')
rh.call('gyLed', 10)

while True:
    gyRaw = rh.call('gyGet') # GY-33 color sensor
    csHsv = cs.hsv()         # Lego color sensor
    csCol = cs.color()
    gyHsv = gy33_color.rgbc_to_hsv_Color(*gyRaw)
    gyCol = gy33_color.hsv_to_standard_Color(gyHsv)
    print(sw.time(), csHsv, csCol, '--', gyRaw, gyHsv, gyCol, sep=', ')
```

and create `gy33_color.py` with content from this repo.

## Mounting the GY-33

t.b.d.

## Comparison

- A call to the GY-33 typically takes 13.5msec, a new value is returned each ~100msec, which is the default integration time for the TCS3472.
- A call to the Lego sensor takes 0.04msec, a new value is returned each ~10msec.
- The Lego sensor is best places 1 beam from the ground, the GY33 sensor basically at the ground.
- With the lens mount the GY-33 is protected against ambient light, for other TCS3472 based sensors you would have to 3D print yourself.
- the sharpness off black & white separation is comparable. I would have expected a significant advantage for the Lego sensor due to its integrated optics and the LEDs outside the optics. Values look better but not significant: ![grafik](https://github.com/user-attachments/assets/10cb9b68-1c06-4907-8140-c1736c47744f).

## Todo
- Compare linefollower with both sensors. Is 10Hz sample rate enough?
- The code above uses the library from `QuirkyCort`. This first communicates with the microcontroller on the back of the board which then communicates with the TCS3472.
  - Try serial instead of I2C communication as only this can set integration time and gain.
  - Try a different library and the other pins to directly communicate with the TCS3472.

