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
import joblib

folder_for_CSV = "/data"


obstacle_1 = [0.9, 1.85]
obstacle_2 = [1.5, 1.7]
obstacle_3 = [2.1, 1.85]

fullPath = os.getcwd() + folder_for_CSV

if not os.path.isdir("." + folder_for_CSV):
    os.mkdir(fullPath)

x = 0.171
y = 0.171

x_sample = 30
y_sample = 20

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

angular_orientation = []
for i in range(24):
    angular_orientation.append(math.pi * i/12)

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
    return values

def hitting_obstacle(t_x, t_y):
    if t_x > (obstacle_1[0] - 0.2) and t_x < (obstacle_1[0] + 0.2) and t_y > obstacle_1[1] - 0.2:
        return True
    if t_x > (obstacle_2[0] - 0.2) and t_x < (obstacle_2[0] + 0.2) and t_y > obstacle_2[1] - 0.2:
        return True
    if t_x > (obstacle_3[0] - 0.2) and t_x < (obstacle_3[0] + 0.2) and t_y > obstacle_3[1] - 0.2:
        return True
    return False

def remove_gobelets():
    for i in range(1,51):
        gob = robot.getFromDef(f'GOB{i}')
        gob.remove()

def acquire_data():
    translationtion_field.setSFVec3f([x, 0.17, y])

    for orien in range(0,4):
        for sector in range(1,5):
            with open(f'data/sector{sector}_orient{orien}.csv', 'w') as f:
                writer = csv.writer(f, delimiter=',')
                for j in range(13):
                    for k in range(8):
                        for i in range(int(len(full_turn)/4)):
                            if sector == 1:
                                tr_x = x + (j/10)
                                tr_y = y + (k/10)
                            if sector == 2:
                                tr_x = x + (j/10)
                                tr_y = 2.0 - y - (k/10)
                                if hitting_obstacle(tr_x, tr_y):
                                    tr_x = x
                                    tr_y = 2.0 - y
                            if sector == 3:
                                tr_x = 3.0 - x - (j/10)
                                tr_y = 2.0 - y - (k/10)
                                if hitting_obstacle(tr_x, tr_y):
                                    tr_x = 3.0 - x
                                    tr_y = 2.0 - y
                            if sector == 4:
                                tr_x = 3.0 - x - (j/10)
                                tr_y = y + (k/10)
                            rotation_field.setSFRotation(full_turn[orien*int(len(full_turn)/4) + i])
                            translationtion_field.setSFVec3f([tr_x, 0.17, tr_y])
                            robot.step(1)
                            time.sleep(0.0005)
                            values = get_vlx_values()
                            position = [asterix.getPosition()[0], 2 - asterix.getPosition()[2]]
                            writer.writerow(np.concatenate([position, [angular_orientation[orien*int(len(full_turn)/4) + i]], values]))

def right_first_diag(x,y):
    if x > 1.5 * y:
        return True
    return False

def right_second_diag(x,y):
    if x > 1.5 * (2- y):
        return True
    return False

def check_for_sample(sector, x, y):
    if sector in [1,6]:
        return right_first_diag(x,y)
    if sector in [2,5]:
        return not right_first_diag(x,y)
    if sector in [3,8]:
        return not right_second_diag(x,y)
    if sector in [4,7]:
        return right_second_diag(x,y)


def acquire_data_rework():
    translationtion_field.setSFVec3f([x, 0.17, y])

    for sector in range(1,9):
        with open(f'data/sector{sector}.csv', 'w') as f:
            writer = csv.writer(f, delimiter=',')
            for k in range(y_sample):
                for j in range(x_sample):
                    hit = False
                    angle = False
                    if sector in [1,2]:
                        tr_x = x + j*((1.5-x)/x_sample)
                        tr_y = y + k*((1.0-y)/y_sample)
                        if tr_x < 0.3 and tr_y < 0.3:
                            angle = True
                    if sector in [3,4]:
                        tr_x = x + j*((1.5-x)/x_sample)
                        tr_y = 2.0 - y - k*((1.0-y)/y_sample)
                        if hitting_obstacle(tr_x, tr_y):
                            hit = True
                        if tr_x < 0.3 and tr_y > 1.7:
                            angle = True
                    if sector in [5,6]:
                        tr_x = 3.0 - x - j*((1.5-x)/x_sample)
                        tr_y = 2.0 - y - k*((1.0-y)/y_sample)
                        if hitting_obstacle(tr_x, tr_y):
                            hit = True
                        if tr_x > 1.7 and tr_y > 1.7:
                            angle = True
                    if sector in [7,8]:
                        tr_x = 3.0 - x - j*((1.5-x)/x_sample)
                        tr_y = y + k*((1.0-y)/y_sample)
                        if tr_x > 1.7 and tr_y < 0.3:
                            angle = True
                    if check_for_sample(sector, tr_x, tr_y) and not hit and not angle:
                        translationtion_field.setSFVec3f([tr_x, 0.17, tr_y])
                        for i in range(len(full_turn)):
                            rotation_field.setSFRotation(full_turn[i])
                            robot.step(1)
                            time.sleep(0.0005)
                            values = get_vlx_values()
                            position = [asterix.getPosition()[0], 2 - asterix.getPosition()[2]]
                            writer.writerow(np.concatenate([position, [angular_orientation[i]], values]))

def test_regression():
    regr = joblib.load('test.sav')
    difftot = 0
    nb = 0
    max = 0
    nbmax = -1

    for j in range(13):
        for k in range(8):
            for i in range(int(len(full_turn)/4)):
                tr_x = x + (j/10)
                tr_y = y + (k/10)
                rotation_field.setSFRotation(full_turn[i])
                translationtion_field.setSFVec3f([tr_x, 0.17, tr_y])
                robot.step(1)
                time.sleep(0.0005)
                values = get_vlx_values()
                predicted_position = regr.predict([values])
                position = [asterix.getPosition()[0], 2 - asterix.getPosition()[2]]
                difftot += abs(predicted_position-position[0])
                nb += 1
                if abs(predicted_position-position[0])>max:
                    nbmax += 1
                    max = abs(predicted_position-position[0])
    print(difftot/nb)
    print(max)
    print(nbmax)
