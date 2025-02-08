The [Pixy2](https://pixycam.com/pixy2/) camera can be connected with different interfaces to the [LMS-ESP32](https://www.antonsmindstorms.com/product/wifi-python-esp32-board-for-mindstorms/) board.

Below examples read the version info.

# SPI

```python
from machine import Pin, SoftSPI
pixy = SoftSPI(baudrate=1000000, sck=Pin(13), mosi=Pin(14), miso=Pin(12))
pixy.write(bytes.fromhex('aec10e00'))
print(pixy.read(32))
```
- configuration: PixyMon->Configure->Interface=Arduino ICSP SPI
- returns 0x01 bytes ~ each millisecond. response starts after 7 to 8 0x01 bytes. 

# I2C

```python
from machine import Pin, SoftI2C
pixy = SoftI2C(freq=1000000, scl=Pin(13), sda=Pin(14))
print(pixy.scan())
pixy.writeto(84, bytes.fromhex('aec10e00'))
print(pixy.readfrom(84, 22))
```
- configuration: PixyMon->Configure->Interface=I2C + default adress=0x54
- SDA and SCL need a 3k3 pullup each to 3.3V 

# Serial

```python
from machine import Pin, UART
pixy = UART(1, baudrate=115200, rx=Pin(13), tx=Pin(14), timeout=20)
pixy.write(bytes.fromhex('aec10e00'))
print(pixy.read(22)) # min timeout=10, no response before
```
- configuration: PixyMon->Configure->Interface=UART + 115200
- slowest solution

