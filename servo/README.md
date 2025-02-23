Using grey 3x3x5 sized _Geekservo_ 360° servos with [Antons servo module](https://docs.antonsmindstorms.com/en/latest/Software/mpy_robot_tools.html#mpy-robot-tools-servo-module).

[Here](https://shop.pimoroni.com/products/geekservo-building-bricks-360-degree-servo) the best data sheet I could find for the servo. Takes ~1 second for 360° degrees.

## LMS-ESP32 code:

```python
from pupremote import PUPRemoteSensor
from servo import Servo

def servo(v):
    print(v)
    sv.angle(v)

sv = Servo(21, min_pulse = 518, max_pulse = 2510, min_angle=0, max_angle=360)
rs = PUPRemoteSensor(power=True)
rs.add_command('servo', '', 'h')
rs.process()
while True:
    rs.process()
```
If the code above fails with `TypeError: unexpected keyword argument 'min_pulse'` add a _servo.py_ file with latest content from [antonvh:mpy_robot_tools/servo.py](https://github.com/antonvh/mpy-robot-tools/blob/master/mpy_robot_tools/servo.py).

The pulse values have to be adjusted for each servo individually

## Pybricks code:

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
