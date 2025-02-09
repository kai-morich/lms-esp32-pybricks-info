# Thonny

Start simple with [Thonny](https://thonny.org/). Thonny typically edits files directly on the device, so you have no local copy.

# VS Code + Pymakr

To have a local copy, git integration, ... use VS Code with _Pymakr Preview_ extension. The extension is not updated since late 2022, but works ok.
Usage is a bit obscure, after configured you basically need these 3 underlined buttons in the Explorer tree that are only shown when hovering over the line.\
![](pymakr.png)

For syntax highlighting add the micropython-esp32-stubs to your `typings` folder as described [here](https://micropython-stubs.readthedocs.io/en/main/) and
add this folder to `py_ignore` in your `pymakr.conf` file.

Neopixel and other functionality is already included in the standard MicroPython distribution, but some features are LMS-ESP32 specific,
like the [servo module](https://docs.antonsmindstorms.com/en/latest/Software/mpy_robot_tools.html#mpy-robot-tools-servo-module).
Copy [servo.py](https://github.com/antonvh/mpy-robot-tools/blob/master/mpy_robot_tools/servo.py) into your `typings` folder.
