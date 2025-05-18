# Using the [GY-33 color sensor](http://wiki.sunfounder.cc/index.php?title=GY-33_Color_Recognition_Sensor_Module) with the [LMS-ESP32 board](https://www.antonsmindstorms.com/product/wifi-python-esp32-board-for-mindstorms/) from Antons Mindstorms and LEGO&reg; Spike running [Pybricks](https://pybricks.com/)

The TCS3472 based color sensor GY-33 comes only with minimal public documentation, luckily [QuirkyCort](https://github.com/QuirkyCort) created the [micropython-gy33](https://github.com/QuirkyCort/micropython-gy33) library from some chinese documentation.

## LMS-ESP32 code:
```python
from pupremote import PUPRemoteSensor
from machine import Pin, UART
from neopixel import NeoPixel
from gy33_uart import GY33_UART # copy from https://github.com/QuirkyCort/micropython-gy33/blob/main/gy33-uart/gy33_uart.py

np = NeoPixel(Pin(25), 1) # onboard neopixel
np[0] = (255, 255, 0); np.write() # yellow = int

# connect GY-33 DR pin to LMS-ESP32 tx, CT pin to rx, VCC to 5V or 3.3V
gy33 = GY33_UART(UART(1, baudrate=115200, rx=Pin(20), tx=Pin(19))) # or pin 4,5 or ...
# initially connect with baudrate=9600 and execute gy33.set_baudrate(115200) once. 
# this switches the baud rate _permanently_ to 115k2 on next power on
#gy33.set_baudrate(115200)
gy33.set_integration_time(100) # raw values are proportional to integration time
gy33.set_output(raw=True, lcc=False, processed=False) # speed up by disabling other responses
gy33.set_led(10)
if not gy33.update(wait=1000): # connection check
    np[0] = (255, 0, 0); np.write() # red = error
    raise RuntimeError('gy33 not responding')

def gyGet():
    return tuple(gy33.get_raw())

def gyLed(v):
    gy33.set_led(v)

def gyTim(v):
    gy33.set_integration_time(v)

rs = PUPRemoteSensor(power=True)
rs.add_command('gyGet', 'HHHH') # values 0~6000
rs.add_command('gyLed', '', 'B') # value 0-10
rs.add_command('gyTim', '', 'B') # value 24,100,...

np[0] = (0, 0, 255); np.write() # blue = wait for spike
rs.process()

np[0] = (0, 255, 0); np.write() # green = ready
while True:
    rs.process()
    gy33.update() # read raw value
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
rh.add_command('gyTim', '', 'B')
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

- The GY-33 automatically sends new values over the serial line after the integration time. Reasonable integration times are 100 and 24msec. Reading more frequently from Spike side does not make sense.
- The GY-33 supports UART and I2C communication modes. I2C mode has faster transfer speed, but each get_raw() includes a communication roundtrip. Only serial mode can change the integration time and has automatic sending of new values.
- The Lego sensor returns a new value each 9~10msec.
- The Lego sensor is best places 1 beam from the ground, the GY33 sensor nearest to ground as possible.
- With the lens mount the GY-33 is protected against ambient light, for other TCS3472 based sensors you would have to 3D print yourself.
- the sharpness off black & white separation is comparable. I would have expected a significant advantage for the Lego sensor due to its integrated optics and the LEDs outside the optics. Values look better but not significant: ![grafik](https://github.com/user-attachments/assets/10cb9b68-1c06-4907-8140-c1736c47744f).

## Todo
- Compare linefollower with both sensors and different integration time
- The code above uses the library from `QuirkyCort`. This first communicates with the microcontroller on the back of the board which then communicates with the TCS3472. Could try the other pins to directly communicate with the TCS3472 with a different library

