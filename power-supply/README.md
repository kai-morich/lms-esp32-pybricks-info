# Power Supply with voltage monitoring for the [LMS-ESP32 board](https://www.antonsmindstorms.com/product/wifi-python-esp32-board-for-mindstorms/) from Antons Mindstorms

Pybricks can report the Lego spike battery voltage with `hub.battery.voltage()`.  
A similar solution is possible for the *LMS-ESP32* by using the *18650 Shield V3*.

The battery voltage is connected thru a 1MOhm voltage divider to an ADC capable pin of the LMS-ESP32. The support capacitor stabilizes the voltage while charging the ESP32's internal sampling capacitor.
![schematic](https://github.com/user-attachments/assets/59899f4a-1886-41c1-8cce-2818cc42ad88)
I cut some traces, scraped off the solder mask and soldered SMD resistors to the bottom of the shield and repurposed one of the three 5V pin headers to provide this signal.  
![board](https://github.com/user-attachments/assets/818af329-7c86-45e6-8632-c3aa5984f478)

## LMS-ESP32 code
```python
from machine import ADC, Pin

adcBat = ADC(Pin(13), atten=ADC.ATTN_11DB) # 11DB = 0-2.45V

def vBat() -> int:
    '''returns battery voltage in millivolt'''
    return adcBat.read_uv()//500
```
