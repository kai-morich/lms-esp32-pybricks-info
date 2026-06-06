# Comparison of different light sensor arrays

Light sensor arrays only measure brightness, which is sufficient for line followers.  
If you need the actual color you should use a [color sensor](../color-sensors/README.md).

# Devices

## Antons Mindstorms / 8-Channel Line Tracking Sensor

Will be available [here](https://www.antonsmindstorms.com/product/8-channel-line-sensor-for-spike-mindstorms/) but is not available yet. 

## Yahboom / 8 channel tracking module

Available [here](https://category.yahboom.net/products/8-lp) and on AliExpress.

Needs a 3D printed enclosure to protect against ambient light, and to protect from neighbor IR diodes that would oversaturate the inner sensors.

The I2C interface only provides binary data, so I implemented the [yahboom-8lp-uart](https://github.com/kai-morich/yahboom-8lp-uart) library to efficiently read the analog data via UART interface.
