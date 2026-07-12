# Comparison of different light sensor arrays

Light sensor arrays only measure brightness, which is sufficient for line followers.  
If you need the actual color you should use a [color sensor](../color-sensors/README.md).

# Devices

All devices need a housing to protect against the infrared component of sunlight.

## Antons Mindstorms / 8-Channel Line Tracking Sensor

Will be available [here](https://www.antonsmindstorms.com/product/8-channel-line-sensor-for-spike-mindstorms/). 

## Yahboom / 8 channel infrared tracking sensor module

Available [here](https://category.yahboom.net/products/8-lp) and on AliExpress.

Don't use V1.0 that does not compensate the nonuniform lighting of inner vs. outer sensors.

The I2C interface only provides binary data, so I implemented the [yahboom-8lp-uart](https://github.com/kai-morich/yahboom-8lp-uart) library to efficiently read the analog data from the UART interface.

# Usage

Those devices are best used with _centroid_ functions that return the position of the black line. Either it is integrated into the sensor or you can use something like below with 0 for white and larger values for black.

```python
def centroid(values):
    '''
    Calculate the centroid of a list of values.

    E.g. for 8 non-negative input values the result is in [-3.5, 3.5].
    '''
    a = sum(i*s for i, s in enumerate(values))
    b = sum(values)
    c = (len(values) - 1) / 2
    return a / b - c if b else 0.0
```
