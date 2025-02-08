# Minimal Example

Minimalistic example for Lego Spike with Pybricks + LMS-ESP32 board using the onboard neopixel.

Depending on the value of the LEGO force sensor, the led will vary from green to red.

# Prerequisites

- Lego Spike with Pybricks firmware
- LMS-ESP32v2 board from [https://www.antonsmindstorms.com/] with MicroPython firmware

# Steps

## LMS-ESP32
Upload this snippet with Thonny as `main.py`:
```python
from neopixel import NeoPixel
from pupremote import PUPRemoteSensor

def led(v):
    print(v)
    np[0]=(v, 255-v, 0) # green to red
    np.write()
    
np = NeoPixel(Pin(25), 1) # onboard neopixel
np[0] = (0, 0, 255) # blue
np.write()
rs = PUPRemoteSensor(power=True)
rs.add_command('led', '', 'B')
rs.process()
while True:
    rs.process()
```

# Lego Spike
Insert this snippet into Pybricks Code IDE as `main.py`:
```python
from pybricks.pupdevices import ForceSensor
from pybricks.parameters import Port
from pybricks.tools import wait
from pupremote_hub import PUPRemoteHub # copy from https://github.com/antonvh/PUPRemote/blob/main/src/pupremote_hub.py

fs = ForceSensor(Port.A)
rh = PUPRemoteHub(Port.B)
rh.add_command('led', '', 'B')
while True:
    v = min(255, int(fs.force()*25.0)) # map from 0-10.xx to 0-255
    print(v)
    rh.call('led', v)
    wait(100)
```

Add a file `pupremote_hub.py` with content from [antonvh/PUPRemote](https://github.com/antonvh/PUPRemote/blob/main/src/pupremote_hub.py) 
