#!/usr/bin/env python3


"""Actuator definition for robot Obelix."""


from actuators.actuators import DYNA_DOWN, DYNA_UP, NC, NO, Actuators

# Pumps and valves adresses
PUMPS = {
    1: {'pump': 0, 'valve': 1, 'type': NC},
    2: {'pump': 2, 'valve': 3, 'type': NC},
    3: {'pump': 4, 'valve': 9, 'type': NC},
    4: {'pump': 10, 'valve': 11, 'type': NC},
    5: {'pump': 0, 'valve': 1, 'type': NO},
    6: {'pump': 2, 'valve': 3, 'type': NO},
    7: {'pump': 4, 'valve': 9, 'type': NO},
    8: {'pump': 10, 'valve': 11, 'type': NO},
    9: {'pump': 12, 'valve': 13, 'type': NO},
}

# Fans addresses
FANS = [7, 15]

# Servo
SERVOS = {
    'flags': {'addr': 1, 'low': 1000, 'high': 2000}
}

# Dynamixels
DYNAMIXELS = {
    1: {},
    2: {},
    3: {},
    4: {},
}

actuators = Actuators(
    i2c_bus=5,
    pump_addr=[0x40, 0x41],
    FANS=FANS,
    PUMPS=PUMPS,
    SERVOS=SERVOS,
    DYNAMIXELS=DYNAMIXELS
)
