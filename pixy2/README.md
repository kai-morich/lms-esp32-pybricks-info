Using the [Pixy2](https://pixycam.com/pixy2/) camera with [kai-morich/micropython-cmucam5](https://github.com/kai-morich/micropython-cmucam5) library.

Example program for LMS-ESP32:
```python
from neopixel import NeoPixel 
from machine import Pin, SoftI2C
import time
from pixy import CMUcam5 # https://github.com/kai-morich/micropython-cmucam5/blob/main/pixy.py

np = NeoPixel(Pin(25), 1) # onboard neopixel
np[0] = (255, 255, 0)
np.write()

# PixyMon->Configure->Interface=I2C + 0x54
pixy = CMUcam5(SoftI2C(freq=1000000, scl=Pin(32), sda=Pin(33))) # with 3k3 pullup each to 3.3V
pixy.init(2000)
pixy.set_lamp(1,0)

while True:
    # communication fails very often if mixing rgb and blocks!
    if True:
        try:
            rgb = pixy.get_rgb(158,104,0)
            print('rgb',rgb)
            np[0] = rgb
            np.write()
        except Exception as exc:
            print('rgb exc', exc)
    if False:
        try:
            blocks = pixy.get_blocks()
            print('blocks', len(blocks))
            for b in blocks:
                print(b.toJSON())
        except Exception as exc:
            print('block exc', exc)
        time.sleep_ms(200)
```

The camera can be connected with different [interfaces](interfaces.md). Use I2C with 3k3 pullup for SDA and SCL to 3.3V.

![](wiring.jpg)


