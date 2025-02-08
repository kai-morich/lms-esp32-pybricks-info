If you only want to connect a single VL53L0X and expose it as a LEGO compatible sensor, follow [Antons Article](https://www.antonsmindstorms.com/2024/05/02/lego-with-a-laser-distance-sensor/).

If you want to connect multiple sensors and expose them with PUPRemote framework, start with below example that compares LEGO ultrasonic distance sensor with VL53L0X laser distance sensor.

LMS-ESP32 code:
```python
from machine import SoftI2C
from pupremote import PUPRemoteSensor
from VL53L0X import VL53L0X # https://github.com/antonvh/PUPRemote/blob/main/examples/emulate_dist_sensor/VL53L0X.py

i2c = SoftI2C(scl=Pin(4), sda=Pin(5), freq=100000)
tof = VL53L0X(i2c)

rs = PUPRemoteSensor(power=True)
rs.add_channel('tof', 'H')
rs.process()

while True:
    tof.start()
    v = tof.read()
    print(v)
    rs.update_channel('tof', v)
    rs.process()
```
Pybricks code:
```python
from pybricks.pupdevices import UltrasonicSensor
from pybricks.parameters import Port
from pybricks.tools import wait
from pupremote_hub import PUPRemoteHub # https://github.com/antonvh/PUPRemote/blob/main/src/pupremote_hub.py

us = UltrasonicSensor(Port.A)
rh = PUPRemoteHub(Port.B)
rh.add_channel('tof', 'H')

while True:
    a = us.distance()
    b = rh.call('tof')
    print('uls',a,'\ttof',b)
```
