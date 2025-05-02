# Power Supply with voltage monitoring

Pybricks can report the Lego spike battery voltage with `hub.battery.voltage()`.  
A similar solution is possible for the *LMS-ESP32* by using the *18650 Shield V3*.

The battery voltage is connected thru a 1MOhm voltage divider to an ADC capable pin of the *LMS-ESP32*.  
![schematic](https://github.com/user-attachments/assets/7cdb19a9-d499-48e7-983a-e0d9e425bdae)
I cut some traces and soldered SMD resistors to the bottom of the shield and repurposed one of the three 5V soldering points to provide this signal.  
![board](https://github.com/user-attachments/assets/66934cf7-4d4d-452d-a522-fb2da0873ef7)

## LMS-ESP32 code
```python
from machine import ADC, Pin

adcBat = ADC(Pin(13), atten=ADC.ATTN_11DB) # 11DB = 0-2.45V

def vBat() -> int:
    '''returns battery voltage in millivolt'''
    return adcBat.read_uv()//500
```
