Using the [Pixy2](https://pixycam.com/pixy2/) camera with [kai-morich/micropython-cmucam5](https://github.com/kai-morich/micropython-cmucam5) library.

## LMS-ESP32 code:
with full error handling:
```python
from neopixel import NeoPixel 
from machine import Pin, SoftI2C
from pupremote import PUPRemoteSensor
from pixy import CMUcam5 # copy from https://github.com/kai-morich/micropython-cmucam5/blob/main/pixy.py
import sys, time

def pxLmp(a, b):
    pixy.set_lamp(a, b)

def pxBrt(v):
    pixy.set_brightness(v)

def pxRGB(x, y):
    return pixy.get_rgb(x, y, 0)

np = NeoPixel(Pin(25), 1) # onboard neopixel
np[0] = (255, 255, 0); np.write() # yellow = initialize
try:
    rs = PUPRemoteSensor(power=True)
    rs.add_command('pxLmp', '', 'bb')
    rs.add_command('pxBrt', '', 'B')
    rs.add_command('pxRGB', 'BBB', 'HB')
    rs.process()

    # PixyMon->Configure->Interface=I2C + 0x54
    pixy = CMUcam5(SoftI2C(freq=1000000, scl=Pin(32), sda=Pin(33))) # with 3k3 pullup each to 3.3V
    t = time.ticks_ms()
    while True:
        try:
            rs.process() # power turned off after some time w/o heartbeat
            pixy.get_version()
            break
        except:
            if time.ticks_ms() - t > 5000: raise
except Exception as e:
    np[0] = (255, 0, 0); np.write() # red = error
    raise


np[0] = (0, 255, 0); np.write() # green = ready
while True:
    try:
        rs.process()
    except Exception as e:
        if isinstance(e, KeyboardInterrupt):
            break
        sys.print_exception(e)
        np[0] = (255, 0, 0); np.write() # red = failed
        time.sleep_ms(100)
        np[0] = (0, 255, 0); np.write() # green = retry
```

## Pybricks code:
```python
from pybricks.pupdevices import ColorSensor
from pybricks.parameters import Port
from pybricks.tools import wait, StopWatch
from pupremote_hub import PUPRemoteHub # copy from https://github.com/antonvh/PUPRemote/blob/main/src/pupremote_hub.py
import pixy_color # copy from example folder

sw = StopWatch()
rh = PUPRemoteHub(Port.F)
rh.add_command('pxLmp', '', 'bb')
rh.add_command('pxBrt', '', 'B')
rh.add_command('pxRGB', 'BBB', 'HB')

rh.call('pxLmp', 1, 1)
rh.call('pxBrt', 60)

while True:
    r,g,b = rh.call('pxRGB', 150, 100)
    h,s,v = pixy_color.rgb_to_hsv(r,g,b)
    c = pixy_color.hsv_to_color(h,s,v)
    print(f'rgb : {r:3} {g:3} {b:3}    hsv : {int(h*360):3} {int(s*100):3} {v:3}    color : {c}')
```

The camera can be connected with different [interfaces](interfaces.md). Use I2C with 3k3 pullup for SDA and SCL to 3.3V or connect in parallel with another I2C device already having integrated pullups.

![](wiring.jpg)


