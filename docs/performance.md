Duration for a loop executing 1000 x [rgb_to_hsv](https://github.com/kai-morich/lms-esp32-pybricks-info/blob/main/gy-33/gycolor.py#L4):

| Hardware | Duration [msec] |
| --------- | --------- |
| typical PC | &nbsp;&nbsp;&nbsp;&nbsp;0.4 |
| LMS-ESP32 | 280 |
| Spike with Pybricks | 640 |

It's slower by orders of magnitude!

You should be aware that a `rh.call(...)` already takes ~10 msec.
