# Channel vs. Command

Communication variants between the [LMS-ESP32 board](https://www.antonsmindstorms.com/product/wifi-python-esp32-board-for-mindstorms/) from Antons Mindstorms and LEGO&reg; Spike running [Pybricks](https://pybricks.com/)

# Command
As beginner you typically use commands. With Pybricks side like:

```python
from pupremote_hub import PUPRemoteHub

rh = PUPRemoteHub(Port.D)
rh.add_command('my_set', '', 'B')
rh.add_command('my_get', 'B')

rh.call('my_set',1)
value = rh.call('my_get')
```

and LMS-ESP32 side like:

```python
import ...
device = ...

def my_set(value):
    device.set(value)

def my_get():
    return device.get()

rs = PUPRemoteSensor(power=True)
rs.add_command('my_set', '', 'B')
rs.add_command('my_get', 'B')

while True:
    rs.process()
```

Each call takes roughly 12 msec + your command duration on LMS-ESP32 side.

### Command duration > 8 msec

The `call` function has a `wait_ms` parameter with default value 0. The effective wait time is `wait_ms` + roughly 8 msec. If the command on the LMS-ESP32 side takes longer, the previous value is returned without any notice or error!

For longer running commands you have to provide an appropriate wait time, e.g. `rh.call('tof', wait_ms=30)` when using [`vl53l0x.read()`](https://github.com/antonvh/PUPRemote/blob/main/examples/emulate_dist_sensor/VL53L0X.py) in your command. Don't be to generous with the wait time as `call` will always wait for the full specified time.

## Channel

Using `command` is ok for setting values to servo, LED, ... and getting values from sensors occasionaly, but if you want to repeatedly read sensors in a fast interval with low latency you should use `channel` instead, e.g. for using a [color sensor](../color-sensors/README.md) as line follower or [distance sensor](../distance-sensors/README.md) as wall follower.

On the Pybricks side the program looks nearly identical, you only replace `add_command` with `add_channel`.

On the LMS-ESP32 side you use `update_channel(...)` in the main loop instead of providing callback functions, as shown here for a hypothetic sensor:

```python
import ...
device = ...

def my_set(value):
    if value:
        device.start()
    else:
        device.stop()

rs = PUPRemoteSensor(power=True)
rs.add_command('my_set', '', 'B')
rs.add_channel('my_get', 'B')

while True:
    rs.process()
    if device.has_data():
        value = device.get_data()
        rs.update_channel('my_get', value)
```

The first `call` to a channel calls the LMS-ESP32, returns data from the latest `update_channel` and activates the channel. While active the LMS-ESP32 sends new data proactively with `update_channel`. Subsequent `call` immediately return the latest available data in less than 1 msec without calling the LMS-ESP32. Calling a different command or channel deactivates it. If not active, the value is only stored on LMS-ESP32 side, but not send.

As data is send proactively by the LMS-ESP32, it is available on Spike side significantly earlier. With commands it is available 12 msec + measurement duration after call begin. For a VL53L0X this was 5msec vs. 40msec latency.

Keep the run time of your code in the main loop short, to keep the LMS-ESP32 responsive. E.g. do not perform a blocking ToF measurement for 30msec or more in the main loop. Instead the device should run in continues mode, either start before as drafted in `my_set` or a new measurement should be triggered after `update_channel`.

The Lego color sensor provides new data each 9-10 msec. You should not update the channel faster, as this will make the Spike unresponsive.

If only a blocking library is available, you can run that in a separate thread like:
```python
import _thread

import ...
device = ...

class MyDeviceThread:
    def __init__(self, device):
        self.device = device
        self.enabled = False

    def _run(self):
        self.device.start()
        while self.enabled:
            rs.update_channel('my_get', self.device.read())
        self.device.stop()

    def start(self):
        self.enabled = True
        _thread.start_new_thread(self._run, ())

    def stop(self):
        self.enabled = False

deviceThread = MyDeviceThread(device)

def my_set(value):
    if value:
        deviceThread.start()
    else:
        deviceThread.stop()

rs = PUPRemoteSensor(power=True)
rs.add_command('my_set', '', 'B')
rs.add_channel('my_get', 'B')

while True:
    rs.process()
```

## Multiple commands or channels

If you use multiple commands or channels, the first `call` to a different command/channel takes roughly 50 msec instead of 12 msec.

If you want to switch fast between multiple sensors, better use one channel.

## Interval > 500 msec between rs.process() invocations

As mentioned in the [protocol analysis](https://github.com/pybricks/technical-info/blob/master/uart-protocol.md#uart-device-synchronization) the Spike sends a heartbeat each 100 msec which is answered by `rs.process()`. If this does not happen in time, the LMS-ESP32 is marked as dead, `call` aborts with `ENODEV error` and if your LMS-ESP32 is 5V powered by Spike (`PUPRemoteSensor(power=True)`) the power is turned off.  
Looks like the Spike does some retries before marking the LMS-ESP32 as dead. In my tests the actual limit was 500 msec. 

__Command__: The duration of your commands must be shorter.

__Channel__: The duration of your code in the main loop must be shorter- Preferably it is non-blocking.

__Program startup__: If initializing devices during program startup after the first `rs.process()` you also have to take care that `rs.process()` is called often enough.
E.g. if using `PUPRemoteSensor(power=True)` and afterwards initialize a Spike 5V powered [Pixy2](https://pixycam.com/pixy2/) camera, you can use `pixy.init(callback=rs.process)` as shown [here](../pixy2/README.md).  
If initializing devices before the first `rs.process()` there is no such issue.
