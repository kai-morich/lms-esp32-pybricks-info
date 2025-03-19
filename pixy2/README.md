Using the [Pixy2](https://pixycam.com/pixy2/) camera with [kai-morich/micropython-cmucam5](https://github.com/kai-morich/micropython-cmucam5) library.

Example program for LMS-ESP32:
```python
from neopixel import NeoPixel 
from machine import Pin, SoftI2C
import time
from pixy import CMUcam5 # https://github.com/kai-morich/micropython-cmucam5/blob/main/pixy.py
import pixy_color # from current repo

np = NeoPixel(Pin(25), 1) # onboard neopixel
np[0] = (255, 255, 0)
np.write()

# PixyMon->Configure->Interface=I2C + 0x54
pixy = CMUcam5(SoftI2C(freq=1000000, scl=Pin(32), sda=Pin(33))) # with 3k3 pullup each to 3.3V
pixy.init(2000)
pixy.set_lamp(1,0)
resx, resy = pixy.get_resolution()
pixy.set_brightness(64)

while True:
    r,g,b = pixy.get_rgb(resx//2, resy//2, 0)
    h,s,v = pixy_color.rgb_to_hsv(r,g,b)
    c = pixy_color.hsv_to_color(h,s,v)
    cn = pixy_color.color_name(c)
    print(f'rgb : {r:3} {g:3} {b:3}    hsv : {int(h*360):3} {int(s*100):3} {v:3}    color : {cn}')
    np[0] = (r,g,b)
    np.write()

while False:
    blocks = pixy.get_blocks()
    print('blocks', len(blocks))
    for b in blocks:
        print(b.toJSON())
```

The camera can be connected with different [interfaces](interfaces.md). Use I2C with 3k3 pullup for SDA and SCL to 3.3V or connect in parallel with another I2C device already having integrated pullups.

![](wiring.jpg)


