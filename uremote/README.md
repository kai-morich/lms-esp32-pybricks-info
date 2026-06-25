# PUPRemote vs. uRemote

As of PyBricks 4.0 the Spike ports can be used as [UARTDevice](https://docs.pybricks.com/en/latest/iodevices/uartdevice.html) with custom protocol. Before they could only be used as [PUPDevice](https://docs.pybricks.com/en/latest/iodevices/pupdevice.html) and had to use the Lego specific [LPF2  protocol](https://github.com/pybricks/technical-info/blob/master/uart-protocol.md).

Each variant is supported with a different library by Anton:
- https://github.com/AntonsMindstorms/PUPRemote based on PUPDevice
- https://github.com/AntonsMindstorms/uRemote based on UARTDevice

| Performance                                   | PUPRemote | uRemote      |
| --------------------------------------------- | ----------| -------------|
| call with single `0` as parameter or response |   12 msec | 7 - 7.5 msec |
| call with tuple of 8 * `255` as response      |   13 msec |      20 msec |

Each variant has its pros and cons:

## PUPRemote

+ better performance for larger data as it is send binary
+ better performance when using [channels](../channel/README.md) as data is received by PyBricks in the background

## uRemote

+ simpler, no `add_command(...)` needed, no parameter specification needed
+ better error handling
+ no `wait_ms` parameter needed to wait for the call response


