Using grey 3x3x5 sized _Geekservo_ 360° servos with [Antons servo module](https://docs.antonsmindstorms.com/en/latest/Software/mpy_robot_tools.html#mpy-robot-tools-servo-module).

[Here](https://shop.pimoroni.com/products/geekservo-building-bricks-360-degree-servo) the best data sheet I could find for the servo. Takes ~1 second for 360° degrees.

LMS-ESP32 code:

```python
from pupremote import PUPRemoteSensor
from servo import Servo

def servo(v): # value range [0,360]
    print(v)
    sv.angle(v/2-180) # value range [-90,+90]
    
sv = Servo(21)
sv.ccw90 = 482
sv.cw90 = 2472

rs = PUPRemoteSensor(power=True)
rs.add_command('servo', '', 'h')
rs.process()
while True:
    rs.process()
```

Pybricks code:
```python
from pybricks.pupdevices import ForceSensor
from pybricks.parameters import Port
from pybricks.tools import wait
from pupremote_hub import PUPRemoteHub # copy from https://github.com/antonvh/PUPRemote/blob/main/src/pupremote_hub.py

fs = ForceSensor(Port.A)
rh = PUPRemoteHub(Port.B)
rh.add_command('servo', '', 'h')
while True:
    v = min(360, int(fs.force()*36.0)) # map from [0,10.xx] to [0,360]
    print(v)
    rh.call('servo', v)
    wait(100)
```
