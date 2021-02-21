"""
Need export PYTHONPATH=${WEBOTS_HOME}/lib/controller/python38
"""

from controller import Supervisor
from controller import Field
from os import environ

import numpy as np
import math
import time
import os
import csv

folder_for_CSV = "/data"


fullPath = os.getcwd() + folder_for_CSV

if not os.path.isdir("." + folder_for_CSV):
    os.mkdir(fullPath)

x = 0.171
y = 0.171

full_turn = [
    [1.0, 0.0, 0.0, -1.57],
    [0.982902, -0.130198, -0.130198, -1.58804],
    [-0.934738, 0.251261, 0.251261, 1.63823],
    [-0.862359, 0.358006, 0.358006, 1.71834],
    [0.775, -0.447, -0.447, -1.82],
    [0.678, -0.52, -0.52, -1.95],
    [0.577, -0.577, -0.577, -2.09],
    [0.477, -0.622, -0.622, -2.25],
    [0.378, -0.655, -0.655, -2.42],
    [0.281, -0.679, -0.679, -2.59],
    [0.186, -0.695, -0.695, -2.77],
    [0.0927, -0.704, -0.704, -2.96],
    [0.0, -0.707, -0.707, -3.14],
    [0.0927, 0.704, 0.704, -2.96],
    [0.186, 0.695, 0.695, -2.77],
    [0.281, 0.679, 0.679, -2.59],
    [0.378, 0.655, 0.655, -2.42],
    [0.477, 0.622, 0.622, -2.25],
    [0.577, 0.577, 0.577, -2.09],
    [0.678, 0.52, 0.52, -1.95],
    [0.775, 0.447, 0.447, -1.82],
    [0.863, 0.357, 0.357, -1.72],
    [0.935, 0.251, 0.251, -1.64],
    [0.983, 0.129, 0.129, -1.59]
]

environ["WEBOTS_ROBOT_NAME"] = "asterix"
robot = Supervisor()

vlx_array = []
for i in range(6):
    vlx = robot.getDevice(f'vlx_0x3{i}')
    vlx.enable(1)
    vlx_array.append(vlx)

asterix = robot.getFromDef('ASTERIX')
translationtion_field = asterix.getField('translation')
rotation_field = asterix.getField('rotation')

def get_vlx_values():
    values = []
    for i in vlx_array:
        values.append(round(i.getValue(), 1))
