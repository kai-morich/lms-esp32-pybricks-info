# Thonny

Start simple with [Thonny](https://thonny.org/). Thonny typically edits files directly on the device, so you have no local copy.

# VS code + Pymakr

To have a local copy, git integration, ... use VS code with Pymakr extension. The extension is not updated for 3 years, but works ok.
Usage is a bit obscure, you basically need these 3 underlined buttons in the Explorer tree that are only shown when hovering over the line.

For syntax highlighting add the micropython-esp32-stubs to your `typings` folder as described [here](https://micropython-stubs.readthedocs.io/en/main/).
Neopixel and other functionality is already included in the standard MicroPython distribution, but some features are LMS-ESP32 specific,
like the [servo module](https://docs.antonsmindstorms.com/en/latest/Software/mpy_robot_tools.html#mpy-robot-tools-servo-module).
Copy [servo.py](https://github.com/antonvh/mpy-robot-tools/blob/master/mpy_robot_tools/servo.py) into your `typings` folder.
